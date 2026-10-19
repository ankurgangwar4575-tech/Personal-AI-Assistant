# AI Personal Assistant

A lightweight web-based personal assistant built with Flask and Google Gemini. The app provides a simple browser interface for asking general questions and summarizing email text.

## Features

- **Ask Anything:** Submit a question and receive a response from the AI assistant.
- **Summarize Email:** Paste email text and get a concise summary intended to be 2–3 sentences.
- **Responsive interface:** A straightforward HTML interface styled with CSS.

## Tech stack

- **Python** – application language
- **Flask** – web server and HTTP routes
- **HTML and CSS** – page structure and styling
- **JavaScript** – submits form data asynchronously and displays results
- **OpenAI Python client** – sends chat completion requests
- **Google Gemini API** – model provider, accessed through its OpenAI-compatible API endpoint
- **python-dotenv** – loads the API key from a local `.env` file

## How it works

The Flask app serves the page at `/`. The browser sends form data to `/ask` for general questions or `/summarize` for email summaries. Flask forwards the text to the configured Gemini chat model and returns the generated result as JSON for the page to display.

## Setup

### Requirements

- Python 3.9 or newer
- A Google Gemini API key

### Install and run

1. Clone or download this project and open a terminal in its directory.
2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Activate it with `source .venv/bin/activate` on macOS/Linux, or `.venv\Scripts\Activate.ps1` in PowerShell.

3. Install the Python packages used by the app:

   ```bash
   pip install Flask python-dotenv openai
   ```

4. Create a `.env` file in the project directory and add your API key:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. Start the app:

   ```bash
   python main.py
   ```

6. Open the local address printed by Flask in your browser (by default, `http://127.0.0.1:5000`).

## Project structure

```text
.
├── main.py              # Flask routes and Gemini API calls
├── templates/
│   └── index.html       # Assistant and email summary interface
├── static/
│   └── style.css        # Page styles
├── .env                 # Local API key (create this; do not commit it)
└── README.md
```

## Configuration

The application reads `GEMINI_API_KEY` from the environment. It uses Google’s OpenAI-compatible API endpoint and the `gemini-3.8-flash` model configured in `main.py`.
