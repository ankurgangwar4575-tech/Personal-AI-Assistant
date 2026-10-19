from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI, APIStatusError, APIConnectionError

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

app = Flask(__name__)


def get_ai_error_message(error):
    """Return a user-friendly message for Gemini API errors."""
    status_code = getattr(error, "status_code", None)

    if status_code == 429:
        return (
            "AI service quota or rate limit reached. "
            "Please try again later when your quota resets."
        )

    if status_code == 503:
        return (
            "The AI service is temporarily busy. "
            "Please try again in a few minutes."
        )

    if status_code in (401, 403):
        return (
            "AI service authentication failed. "
            "Please check the API key configuration."
        )

    return "The AI service is temporarily unavailable. Please try again later."


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question", "").strip()

    if not question:
        return jsonify({"response": "Please enter a question."}), 400

    try:
        response = client.chat.completions.create(
            model="gemini-3.8-flash",
            messages=[
                {
                    "role": "system",
                    "content": "Act like a helpful personal assistant"
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=512
        )

        answer = response.choices[0].message.content
        answer = (answer or "").strip()

        return jsonify({"response": answer}), 200

    except (APIStatusError, APIConnectionError) as error:
        app.logger.exception("Gemini API request failed")
        return jsonify({"response": get_ai_error_message(error)}), 503

    except Exception:
        app.logger.exception("Unexpected error in /ask")
        return jsonify({
            "response": "Something went wrong. Please try again later."
        }), 500


@app.route("/summarize", methods=["POST"])
def summarize():
    email_text = request.form.get("email", "").strip()

    if not email_text:
        return jsonify({"response": "Please enter an email to summarize."}), 400

    prompt = f"summarize the following email in 2-3 sentences: {email_text}"

    try:
        response = client.chat.completions.create(
            model="gemini-3.8-flash",
            messages=[
                {
                    "role": "system",
                    "content": "Act like an expert email assistant"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=512
        )

        summary = response.choices[0].message.content
        summary = (summary or "").strip()

        return jsonify({"response": summary}), 200

    except (APIStatusError, APIConnectionError) as error:
        app.logger.exception("Gemini API request failed")
        return jsonify({"response": get_ai_error_message(error)}), 503

    except Exception:
        app.logger.exception("Unexpected error in /summarize")
        return jsonify({
            "response": "Something went wrong. Please try again later."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
