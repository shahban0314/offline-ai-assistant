# offline-ai-assistant
An offline AI assistant built with Flask and Ollama, featuring local LLM chat, chat history, and model performance benchmarking.
> **A 100% Private, Local Conversational AI & Empirical Benchmarking Dashboard for Windows 11**

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-000000)
![Ollama](https://img.shields.io/badge/Ollama-Offline%20LLM-black)
![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57)

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Objectives](#-objectives)
4. [Key Features](#-key-features)
5. [Technologies Used](#-technologies-used)
6. [System Requirements](#-system-requirements)
7. [Installation Guide (Windows 11)](#-installation-guide-windows-11)
   - [Step 1: Install Ollama & Pull Models](#step-1-install-ollama--pull-models)
   - [Step 2: Clone or Download the Project](#step-2-clone-or-download-the-project)
   - [Step 3: Setup Python Virtual Environment](#step-3-setup-python-virtual-environment)
   - [Step 4: Install Dependencies](#step-4-install-dependencies)
   - [Step 5: Run the Application](#step-5-run-the-application)
8. [Project Folder Structure](#-project-folder-structure)
9. [Database Architecture & Schema](#-database-architecture--schema)
10. [REST API Documentation](#-rest-api-documentation)
11. [Benchmark Metrics Explained](#-benchmark-metrics-explained)
12. [Heuristic Quality Score & Limitations](#-heuristic-quality-score--limitations)
13. [UI Screenshots & Interface Walkthrough](#-ui-screenshots--interface-walkthrough)
14. [Troubleshooting & FAQ](#-troubleshooting--faq)
15. [Security & Privacy Posture](#-security--privacy-posture)
16. [Future Roadmap](#-future-roadmap)

---

## 🌟 Project Overview

The **Offline AI Assistant** is a self-hosted, air-gapped web application that provides conversational artificial intelligence directly on your personal computer without internet access, third-party cloud APIs, or recurring subscription fees.

Built on top of **Flask**, **SQLite**, and **Ollama**, the assistant enables instant switching between leading local open-weight language models—**Microsoft Phi-3 (3.8B)** and **Meta Llama 3.2 (3B)**. In addition to responsive chatting, code syntax highlighting, and conversation history management, the application features an integrated **Benchmark Dashboard** that measures real-world inference latency, token output, and response length on your local hardware.

---

## 🎯 Problem Statement

Modern cloud-based AI services (e.g., ChatGPT, Claude, Gemini) present significant tradeoffs for developers, enterprises, and privacy-conscious users:

- **Privacy & Security Risks:** Sensitive codebases, personal data, and proprietary intellectual property are transmitted over the public internet to third-party servers.
- **Internet Dependency:** AI productivity grinds to a halt during network outages, air-gapped environments, or travel.
- **Subscription Costs & Rate Limits:** Recurring fees and restrictive API token quotas limit continuous development.
- **Lack of Local Benchmarking:** Users have little transparency into how different open-source models perform on their specific CPU/GPU configurations.

---

## 🎯 Objectives

1. **Complete Data Sovereignty:** Guarantee that 100% of prompts, completions, and logs stay on the local machine.
2. **Multi-Model Comparison:** Provide seamless switching between **Phi-3** and **Llama 3.2 3B** within a single interface.
3. **Empirical Telemetry:** Record response time, character count, token generation speed, and heuristic response quality on every turn.
4. **Offline Visualizations:** Offer a dedicated, local Chart.js dashboard to visually contrast model speed and throughput.
5. **Robust Usability:** Deliver a polished, responsive blue-themed UI with code block formatting, one-click clipboard copying, and searchable history.

---

## 🚀 Key Features

### 💬 Modern Chat Experience
- **Blue-Themed Responsive Interface:** Optimized for desktop monitors, laptops, tablets, and smartphones.
- **Distinct Message Bubbles:** Clear visual hierarchy between user prompts (blue badge, soft blue container) and assistant responses (white card, blue accent border).
- **Code Block Formatting:** Automatic syntax styling with dark-themed monospaced blocks, language headers, and dedicated **📋 Copy Code** buttons.
- **1-Click Copy Response:** Easily copy complete answers to the clipboard with visual confirmation feedback.
- **Auto-Resizing Textarea:** Type naturally with `Enter` to send and `Shift+Enter` for multi-line formatting.
- **Interactive Suggestions:** Four pre-configured prompt cards on the empty welcome screen for rapid testing.
- **Duplicate Request Guard:** Active submission locking prevents duplicate button clicks or repeated network requests.

### 🕘 Searchable Chat History
- **Instant Search:** Client-side, real-time filtering across all user prompts and AI responses.
- **Model Categorization:** Filter history by `Phi-3`, `Llama 3.2 3B`, or `Legacy / Other`.
- **Chronological Sorting:** Switch instantly between `Newest First` and `Oldest First`.
- **Safe Chat Deletion:** Confirm deletions with prompt previews; remove records without page reloads.

### 📊 Offline Benchmark Dashboard
- **Empirical Summary Cards:** Compare total responses, average latency, average length, tokens, and heuristic quality.
- **Four Local Comparison Charts:**
  1. ⚡ *Response Time Comparison* (Average seconds per model)
  2. 📏 *Response Length Comparison* (Average characters per model)
  3. 🔢 *Token Usage Comparison* (Average tokens per response)
  4. ⭐ *Heuristic Quality Score Comparison* (0–100 heuristic scale)
- **100% Offline Visualizations:** Rendered using a bundled local copy of Chart.js (`static/js/chart.umd.min.js`) with zero CDN dependencies.
- **Safe Null Handling:** Accurately calculates true mathematical averages solely over valid records, excluding missing or legacy unmetered rows.

---

## 🛠️ Technologies Used

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.10+ / Flask 3.x | Lightweight WSGI web server and RESTful routing |
| **LLM Inference Engine** | Ollama (Windows) | High-performance local GGUF/llama.cpp inference engine |
| **Primary Language Models** | Microsoft Phi-3 Mini (3.8B) & Meta Llama 3.2 (3B) | State-of-the-art compact open-weights models |
| **Database** | SQLite 3 (Standard Library) | Embedded zero-configuration ACID relational storage |
| **Data Visualizations** | Chart.js 4.x (Local UMD) | Offline canvas-rendered interactive bar charts |
| **Frontend UI** | HTML5 / CSS3 / Vanilla JavaScript | Fast, zero-dependency modern client interface |

---

## 💻 System Requirements

- **Operating System:** Windows 11 (64-bit) or Windows 10 (Version 21H2+ / Build 19044+)
- **Processor (CPU):** Intel Core i5 / AMD Ryzen 5 or higher (x86_64 architecture with AVX2 support)
- **Memory (RAM):** 8 GB minimum (16 GB strongly recommended for smooth model switching)
- **Storage:** At least 10 GB of available SSD space (for Ollama model weights and database)
- **GPU (Optional):** NVIDIA GPU with CUDA or AMD/Intel GPU supported by Ollama for GPU acceleration

---

## 📦 Installation Guide (Windows 11)

Follow these step-by-step instructions using **Windows PowerShell**.

### Step 1: Install Ollama & Pull Models

1. Download and run the Windows installer from [ollama.com/download/windows](https://ollama.com/download/windows) (or run `winget install Ollama.Ollama`).
2. After installation, launch Ollama from your Start Menu (it will sit in your Windows system tray).
3. Open **Windows PowerShell** and download the two required language models:

```powershell
# Pull Microsoft Phi-3 Mini (approx. 2.2 GB)
ollama pull phi3

# Pull Meta Llama 3.2 3B (approx. 2.0 GB)
ollama pull llama3.2:3b
```

4. Verify that both models are installed and recognized:

```powershell
ollama list
```

*Expected output:*
```
NAME            ID              SIZE      MODIFIED
llama3.2:3b     a80c4f17acd5    2.0 GB    ...
phi3:latest     4f2222927938    2.2 GB    ...
```

---

### Step 2: Navigate to Project Directory

In PowerShell, navigate to the folder containing the project:

```powershell
cd "C:\Users\shaban\OneDrive\Desktop\AI Project\offline-ai-assistant"
```

---

### Step 3: Setup Python Virtual Environment

Create an isolated virtual environment to avoid package conflicts:

```powershell
# Create virtual environment named 'venv'
python -m venv venv

# If PowerShell script execution is restricted, temporarily permit it:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

*(Your terminal prompt will now show `(venv)` at the beginning).*

---

### Step 4: Install Dependencies

Install the required Python libraries using `pip`:

```powershell
pip install -r requirements.txt
```

*Contents of `requirements.txt`:*
```
flask
requests
```

---

### Step 5: Run the Application

Start the local Flask development server:

```powershell
python app.py
```

*Terminal output:*
```
Database: C:\Users\shaban\OneDrive\Desktop\AI Project\offline-ai-assistant\database\chat_history.db
History page: http://127.0.0.1:5000/history-page
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Open your web browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📁 Project Folder Structure

```text
offline-ai-assistant/
│
├── app.py                      # Main Flask application and REST routes
├── capture_screenshots.py      # Automated screenshot capture utility (Edge CDP)
├── requirements.txt            # Python dependencies (flask, requests)
├── README.md                   # Complete project documentation
├── ARCHITECTURE.md             # System architecture & component design
│
├── database/
│   └── chat_history.db         # Persistent SQLite database file
│
├── screenshots/
│   ├── 01_chat_interface.png      # Real chat UI with code blocks & metadata chips
│   ├── 02_chat_history.png         # Stored history view with search, filter & delete
│   └── 03_benchmark_dashboard.png  # Performance analytics with 4 comparison charts
│
├── static/
│   └── js/
│       └── chart.umd.min.js    # Local offline Chart.js bundle (v4.4.4)
│
└── templates/
    ├── index.html              # Modern blue-themed chat UI
    ├── history.html            # Searchable, filterable chat history page
    └── benchmark.html          # Performance telemetry & comparison dashboard
```

---

## 🗄️ Database Architecture & Schema

The application uses an embedded **SQLite 3** relational database located at `database/chat_history.db`. Database creation and column migrations run automatically upon startup in `init_db()`.

### Table: `chat_history`

| Column | Type | Nullable | Default | Description |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INTEGER` | No | Auto | Primary Key (auto-incrementing unique identifier) |
| `user_message` | `TEXT` | No | — | The verbatim input prompt submitted by the user |
| `ai_response` | `TEXT` | No | — | The verbatim text completion returned by the model |
| `model` | `TEXT` | Yes | `NULL` | Model identifier used (e.g., `phi3` or `llama3.2:3b`) |
| `response_time`| `REAL` | Yes | `NULL` | Total round-trip latency in seconds (rounded to 2 decimal places) |
| `response_length`| `INTEGER` | Yes | `NULL` | Length of the completion text in characters |
| `token_count` | `INTEGER` | Yes | `0` | Number of tokens evaluated by Ollama (or word count fallback) |
| `quality_score`| `REAL` | Yes | `NULL` | Heuristic evaluation score (0 to 100) |
| `created_at` | `TEXT` | No | — | Timestamp in `YYYY-MM-DD HH:MM:SS` format |

### Indexes

- **`idx_chat_history_model`**: Indexed on `chat_history(model)` to ensure fast filtering on the History and Benchmark pages as records grow.

---

## 🌐 REST API Documentation

### 1. Web Pages

| Route | Method | Description |
| :--- | :---: | :--- |
| `/` | `GET` | Renders the primary chat interface (`templates/index.html`). |
| `/history-page` | `GET` | Renders the searchable chat history view (`templates/history.html`). |
| `/benchmark` | `GET` | Renders the empirical performance dashboard (`templates/benchmark.html`). |

---

### 2. Chat Completion API: `POST /chat`

Submits a prompt to the local Ollama instance and logs results to SQLite.

#### Request Body (`application/json`):
```json
{
  "message": "Write a Python function to check for prime numbers.",
  "model": "phi3"
}
```

#### Success Response (`200 OK`):
```json
{
  "error": false,
  "model": "phi3",
  "response": "Here is a Python function to check for prime numbers:\n\n```python\ndef is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n```",
  "response_length": 218,
  "response_time": 4.12,
  "token_count": 68,
  "quality_score": 85.0
}
```

#### Error Responses:
- `400 Bad Request`: Empty message, message exceeding 10,000 characters, or invalid model name.
- `502 Bad Gateway`: Ollama returned an empty answer, invalid JSON, or HTTP error.
- `503 Service Unavailable`: Cannot connect to Ollama (Ollama daemon is not running).
- `504 Gateway Timeout`: Ollama inference exceeded the 120-second timeout.
- `500 Internal Server Error`: SQLite persistence failure.

---

### 3. History Retrieval API: `GET /history`

Retrieves conversation records from the database. Supports optional URL query parameters for backend filtering.

#### Query Parameters:
- `model` *(optional)*: Filter by model (`phi3`, `llama3.2:3b`, `other`, or `all`).
- `search` *(optional)*: Case-insensitive substring search in prompt or response.
- `order` *(optional)*: Sort order (`desc` for newest-first, `asc` for oldest-first).

#### Example Request:
```http
GET /history?model=phi3&search=python&order=desc
```

#### Success Response (`200 OK`):
```json
[
  {
    "id": 41,
    "user_message": "how are u",
    "ai_response": "I'm just a text-based AI developed by Microsoft...",
    "model": "phi3",
    "response_time": 21.18,
    "response_length": 118,
    "token_count": 37,
    "quality_score": 85.0,
    "created_at": "2026-10-04 16:21:56"
  }
]
```

---

### 4. Delete Chat API: `DELETE /delete-chat/<int:chat_id>`

Permanently removes a specific chat record from the SQLite database.

#### Example Request:
```http
DELETE /delete-chat/41
```

#### Success Response (`200 OK`):
```json
{
  "success": true
}
```

#### Error Response (`404 Not Found`):
```json
{
  "success": false,
  "message": "Chat not found."
}
```

---

## 📈 Benchmark Metrics Explained

The Benchmark Dashboard calculates four core performance dimensions across models:

1. **Response Time (Seconds):** Measures total elapsed wall-clock latency from the moment the user clicks "Send" until the complete response is generated and parsed.
2. **Response Length (Characters):** Measures total character count of the completion, illustrating conciseness vs. verbosity between models.
3. **Token Count (Tokens):** Represents the number of generation tokens reported by Ollama (`eval_count`). If `eval_count` is absent, the system approximates tokens using word count.
4. **Heuristic Quality Score (0–100):** An automated algorithmic heuristic evaluating formatting, keyword relevance, and absence of error indicators.

---

## ⚠️ Heuristic Quality Score & Limitations

> [!IMPORTANT]
> The **Heuristic Quality Score** is an automated proxy metric and **DOES NOT measure true factual accuracy, reasoning correctness, or truthfulness**.

### Scoring Formula:
The score is calculated in `app.py` via `calculate_quality_score()` out of 100 points:

1. **Non-Empty Response (+20 points):** The AI produced text.
2. **Absence of Error Patterns (+20 points):** The completion does not contain words like `"error"`, `"could not connect"`, `"failed"`, or `"exception"`.
3. **Keyword Overlap (+15 to +30 points):**
   - 3 or more shared words between prompt and completion: **+30 points**
   - 1 or 2 shared words: **+15 points**
4. **Length Appropriateness (+15 to +30 points):**
   - If user requested brevity (*"short answer"*, *"1 line"*, *"briefly"*): awards **+30 points** if response is $\le 250$ chars; **+15 points** if $\le 500$ chars.
   - For standard prompts: awards **+30 points** if response length is between 50 and 2,000 characters; **+15 points** if $> 0$ characters.

### Known Limitations:
- An AI can produce a completely fabricated, halluciated answer with high keyword overlap and score 90–100.
- An accurate, single-word factual answer (e.g. answering *"Paris"* to *"What is the capital of France?"*) may receive a lower length score.
- This metric is useful for detecting model failures and formatting alignment, but should never be cited as an academic benchmark of factual truth.

---

## 🖼️ UI Screenshots & Interface Walkthrough

### 1. Interactive Chat Interface (`/`)
Modern blue-themed chat window showing real-time prompt completion, syntax-highlighted code blocks, Copy Code and Copy Response buttons, live latency, token telemetry, and heuristic quality score.

![Chat Interface](screenshots/01_chat_interface.png)

---

### 2. Chat History & Conversation Management (`/history-page`)
Filterable, searchable archive of all past AI conversations stored persistently in SQLite with individual conversation deletion and telemetry breakdown.

![Chat History](screenshots/02_chat_history.png)

---

### 3. AI Model Benchmark Dashboard (`/benchmark`)
Performance comparison analytics dashboard rendering four responsive comparison charts (Latency, Response Length, Token Count, Heuristic Quality Score) between Phi-3 and Llama 3.2 3B.

![Benchmark Dashboard](screenshots/03_benchmark_dashboard.png)

---

## 🔧 Troubleshooting & FAQ

### 1. "Could not connect to Ollama. Please make sure Ollama is running."
- **Cause:** The Ollama background daemon is stopped or port `11434` is blocked.
- **Solution:** 
  1. Open Start Menu and launch **Ollama**.
  2. Verify by running in PowerShell: `curl http://localhost:11434/api/tags`
  3. If not started, run in terminal: `ollama serve`.

### 2. "Ollama returned HTTP status 404. Check whether the selected model is installed."
- **Cause:** The selected model (`phi3` or `llama3.2:3b`) has not been pulled.
- **Solution:** Open PowerShell and execute:
  ```powershell
  ollama pull phi3
  ollama pull llama3.2:3b
  ```

### 3. Generation is slow / taking 20+ seconds on the first request.
- **Cause:** Local language models must be loaded from your SSD into system RAM/VRAM during cold start.
- **Solution:** Subsequent prompts for the same model will be significantly faster because the weights remain resident in memory.

### 4. PowerShell error: `Execution of scripts is disabled on this system`.
- **Cause:** Windows PowerShell execution policy prevents running unsigned activation scripts.
- **Solution:** Run this command in your PowerShell window:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

---

## 🔒 Security & Privacy Posture

- **Zero Outbound Data Transmission:** No user prompts, completions, telemetry, or analytics leave `localhost`.
- **SQL Injection Prevention:** All SQLite queries utilize parameterized placeholders (`?`). Sort directions are strictly allow-listed.
- **Path Sanitization:** User-facing error payloads never expose internal Windows filesystem paths or database directories.
- **XSS Protection:** Client-side HTML rendering passes all untrusted user strings through an `escapeHtml()` sanitizer.
- **Denial-of-Service Defense:** Prompts are restricted to a maximum length of 10,000 characters to prevent memory exhaustion attacks.

---

## 🔮 Future Roadmap

- [ ] **Streaming Token Generation (SSE):** Stream words in real time as they are generated using Server-Sent Events.
- [ ] **Multi-Turn Chat Context:** Retain recent conversation history within the current session prompt.
- [ ] **Export Capabilities:** Download conversation transcripts in Markdown, JSON, or PDF formats.
- [ ] **Expanded Model Library:** Support additional lightweight models such as Mistral 7B, Gemma 2 2B, and Qwen 2.5.
- [ ] **Dark Mode Toggle:** Optional high-contrast dark theme for night-time coding.

---

## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software for personal or commercial applications.
