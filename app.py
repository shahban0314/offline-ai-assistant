from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
from datetime import datetime
import time
import os

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

# Always use a database inside this project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE = os.path.join(DATABASE_DIR, "chat_history.db")

os.makedirs(DATABASE_DIR, exist_ok=True)


def get_db():
    conn = sqlite3.connect(DATABASE, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(DATABASE_DIR, exist_ok=True)

    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        columns = [
            row["name"]
            for row in conn.execute("PRAGMA table_info(chat_history)").fetchall()
        ]

        if "token_count" not in columns:
            conn.execute(
                "ALTER TABLE chat_history ADD COLUMN token_count INTEGER DEFAULT 0"
            )

        if "response_time" not in columns:
            conn.execute(
                "ALTER TABLE chat_history ADD COLUMN response_time REAL"
            )

        if "model" not in columns:
            conn.execute(
                "ALTER TABLE chat_history ADD COLUMN model TEXT"
            )

        if "response_length" not in columns:
            conn.execute(
                "ALTER TABLE chat_history ADD COLUMN response_length INTEGER"
            )

        if "quality_score" not in columns:
            conn.execute(
                "ALTER TABLE chat_history ADD COLUMN quality_score REAL"
            )

        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_chat_history_model ON chat_history(model)"
        )

        conn.commit()
    finally:
        conn.close()


def calculate_quality_score(user_message, ai_response):
    score = 0

    prompt = user_message.lower().strip()
    response = ai_response.strip().lower()

    if response:
        score += 20

    error_words = [
        "error",
        "could not connect",
        "failed",
        "exception"
    ]

    if not any(word in response for word in error_words):
        score += 20

    prompt_words = set(prompt.split())
    response_words = set(response.split())
    common_words = prompt_words.intersection(response_words)

    if len(common_words) >= 3:
        score += 30
    elif len(common_words) >= 1:
        score += 15

    short_request = any(
        phrase in prompt
        for phrase in [
            "2 line",
            "2 lines",
            "one line",
            "1 line",
            "short answer",
            "briefly",
            "in short"
        ]
    )

    response_length = len(response)

    if short_request:
        if response_length <= 250:
            score += 30
        elif response_length <= 500:
            score += 15
    else:
        if 50 <= response_length <= 2000:
            score += 30
        elif response_length > 0:
            score += 15

    return min(score, 100)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "error": True,
            "response": "Invalid JSON request body. Expected a JSON object.",
            "message": "Invalid JSON request body. Expected a JSON object."
        }), 400

    user_message = data.get("message", "")
    model = data.get("model", "phi3")

    if not isinstance(user_message, str):
        return jsonify({
            "error": True,
            "response": "Invalid message format.",
            "message": "Invalid message format."
        }), 400

    user_message = user_message.strip()

    allowed_models = ["phi3", "llama3.2:3b"]

    if model not in allowed_models:
        return jsonify({
            "error": True,
            "response": "Invalid model selected.",
            "message": "Invalid model selected."
        }), 400

    if not user_message:
        return jsonify({
            "error": True,
            "response": "Please enter a message.",
            "message": "Please enter a message.",
            "model": model,
            "response_time": 0.0
        }), 400

    if len(user_message) > 10000:
        return jsonify({
            "error": True,
            "response": "Message exceeds maximum allowed length of 10,000 characters.",
            "message": "Message exceeds maximum allowed length of 10,000 characters.",
            "model": model,
            "response_time": 0.0
        }), 400

    start_time = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": user_message,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        error_msg = "Could not connect to Ollama. Please make sure Ollama is running."
        return jsonify({
            "error": True,
            "response": error_msg,
            "message": error_msg,
            "model": model,
            "response_time": round(time.time() - start_time, 2)
        }), 503

    except requests.exceptions.Timeout:
        error_msg = "Ollama request timed out. Please try again."
        return jsonify({
            "error": True,
            "response": error_msg,
            "message": error_msg,
            "model": model,
            "response_time": round(time.time() - start_time, 2)
        }), 504

    except requests.exceptions.HTTPError:
        error_msg = f"Ollama returned HTTP status {response.status_code}. Check whether the selected model is installed."
        return jsonify({
            "error": True,
            "response": error_msg,
            "message": error_msg,
            "model": model,
            "response_time": round(time.time() - start_time, 2)
        }), 502

    except requests.exceptions.RequestException as e:
        app.logger.exception("Network error communicating with Ollama: %s", str(e))
        error_msg = "A network error occurred while communicating with Ollama."
        return jsonify({
            "error": True,
            "response": error_msg,
            "message": error_msg,
            "model": model,
            "response_time": round(time.time() - start_time, 2)
        }), 502

    response_time = round(time.time() - start_time, 2)

    try:
        result = response.json()
    except ValueError:
        error_msg = "Received invalid JSON from Ollama."
        return jsonify({
            "error": True,
            "response": error_msg,
            "message": error_msg,
            "model": model,
            "response_time": response_time
        }), 502

    ai_response = result.get("response")

    if not isinstance(ai_response, str) or not ai_response.strip():
        error_msg = "AI returned an empty response. Please try again."
        return jsonify({
            "error": True,
            "response": error_msg,
            "message": error_msg,
            "model": model,
            "response_time": response_time
        }), 502

    ai_response = ai_response.strip()
    response_length = len(ai_response)

    eval_count = result.get("eval_count")

    if isinstance(eval_count, (int, float)) and eval_count > 0:
        token_count = int(eval_count)
    else:
        words = ai_response.split()
        token_count = max(len(words), 1)

    quality_score = calculate_quality_score(user_message, ai_response)

    # Save every successful chat
    conn = None

    try:
        conn = get_db()

        conn.execute(
            """
            INSERT INTO chat_history
            (
                user_message,
                ai_response,
                model,
                response_time,
                response_length,
                token_count,
                quality_score,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_message,
                ai_response,
                model,
                response_time,
                response_length,
                token_count,
                quality_score,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        conn.commit()

        print("CHAT SAVED TO DATABASE")

    except sqlite3.Error as e:
        if conn:
            conn.rollback()

        app.logger.exception("Failed to save chat history: %s", str(e))

        error_msg = "AI generated a response, but it could not be saved to chat history due to a database error."
        return jsonify({
            "error": True,
            "response": error_msg,
            "message": error_msg,
            "model": model,
            "response_time": response_time
        }), 500

    finally:
        if conn:
            conn.close()

    return jsonify({
        "response": ai_response,
        "model": model,
        "response_time": response_time,
        "response_length": response_length,
        "token_count": token_count,
        "quality_score": quality_score,
        "error": False
    })


# API used by history.html and benchmark
@app.route("/history")
def history():
    conn = None

    try:
        conn = get_db()

        model = request.args.get("model")
        search = request.args.get("search")
        order = request.args.get("order", "desc").lower()

        query = """
            SELECT
                id,
                user_message,
                ai_response,
                model,
                response_time,
                response_length,
                token_count,
                quality_score,
                created_at
            FROM chat_history
            WHERE 1=1
        """
        params = []

        if model and model != "all":
            if model == "other":
                query += " AND (model IS NULL OR model NOT IN ('phi3', 'llama3.2:3b'))"
            else:
                query += " AND model = ?"
                params.append(model)

        if search:
            query += " AND (user_message LIKE ? OR ai_response LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term])

        if order == "asc":
            query += " ORDER BY id ASC"
        else:
            query += " ORDER BY id DESC"

        chats = conn.execute(query, params).fetchall()

        return jsonify([dict(chat) for chat in chats])

    except sqlite3.Error as e:
        app.logger.exception("Failed to retrieve chat history: %s", str(e))
        return jsonify({
            "error": True,
            "message": "A database error occurred while retrieving chat history."
        }), 500

    finally:
        if conn:
            conn.close()


# Page shown in your screenshot
@app.route("/history-page")
def history_page():
    return render_template("history.html")


@app.route("/benchmark")
def benchmark():
    return render_template("benchmark.html")


@app.route("/delete-chat/<int:chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    conn = None

    try:
        conn = get_db()

        cursor = conn.execute(
            "DELETE FROM chat_history WHERE id = ?",
            (chat_id,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "success": False,
                "message": "Chat not found."
            }), 404

        return jsonify({
            "success": True
        })

    except sqlite3.Error as e:
        if conn:
            conn.rollback()

        app.logger.exception("Failed to delete chat: %s", str(e))
        return jsonify({
            "success": False,
            "message": "A database error occurred while deleting the chat."
        }), 500

    finally:
        if conn:
            conn.close()


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.exception("Unhandled server error: %s", str(e))
    return jsonify({
        "error": True,
        "response": "An internal server error occurred.",
        "message": "An internal server error occurred."
    }), 500


if __name__ == "__main__":
    init_db()
    print("Database:", DATABASE)
    print("History page: http://127.0.0.1:5000/history-page")
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")
    app.run(debug=debug_mode)
