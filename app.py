from flask import Flask, render_template, request, jsonify
from calculator.engine import calculate, get_explanation
from ai.assistant import AIAssistant
import re

app = Flask(__name__)

ai = AIAssistant()


def normalize_voice_math(text):

    text = text.strip()

    patterns = [
        r"\b(sin|cos|tan|asin|acos|atan)\s+(\d+):(\d+)\b",
        r"\b(sin|cos|tan|asin|acos|atan)(\d+):(\d+)\b"
    ]

    for pattern in patterns:

        text = re.sub(
            pattern,
            lambda match:
                f"{match.group(1)} {match.group(2)}{match.group(3)}",
            text,
            flags=re.IGNORECASE
        )

    return text


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    expression = ""

    if request.method == "POST":

        expression = request.form.get(
            "expression",
            ""
        )

        result = calculate(expression)

    return render_template(
        "index.html",
        result=result,
        expression=expression
    )


@app.route("/explain", methods=["POST"])
def explain():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No calculation provided."
        }), 400

    expression = data.get(
        "expression",
        ""
    ).strip()

    if not expression:
        return jsonify({
            "error": "Please enter a calculation."
        }), 400

    result = calculate(expression)

    if result == "Invalid calculation":
        return jsonify({
            "error": "Invalid calculation."
        }), 400

    explanation = get_explanation(
        expression,
        result
    )

    return jsonify(explanation)


@app.route("/ai", methods=["POST"])
def ai_chat():

    data = request.get_json()

    if not data:
        return jsonify({
            "type": "normal",
            "answer": "Please enter a question."
        })

    message = data.get(
        "message",
        ""
    ).strip()

    history = data.get(
        "history",
        []
    )

    if not message:
        return jsonify({
            "type": "normal",
            "answer": "Please enter a question."
        })

    try:

        result = ai.ask(
            message,
            history
        )

        return jsonify(result)

    except Exception as error:

        print("AI Error:", error)

        return jsonify({
            "type": "normal",
            "answer": "Sorry, I couldn't process that request."
        }), 500


@app.route("/voice", methods=["POST"])
def voice_assistant():

    data = request.get_json()

    if not data:
        return jsonify({
            "type": "error",
            "answer": "No voice question received."
        }), 400

    message = data.get(
        "message",
        ""
    ).strip()

    if not message:
        return jsonify({
            "type": "error",
            "answer": "Please speak something."
        }), 400

    message = normalize_voice_math(
        message
    )

    try:

        result = ai.voice_calculation(
            message
        )

        if result.get("type") == "calculation":

            expression = result.get(
                "expression",
                ""
            )

            expression = normalize_voice_math(
                expression
            )

            answer = calculate(
                expression
            )

            if answer != "Invalid calculation":

                return jsonify({
                    "type": "calculation",
                    "expression": expression,
                    "answer": answer
                })

        return jsonify(result)

    except Exception as error:

        print("Voice Error:", error)

        return jsonify({
            "type": "error",
            "answer": "Sorry, I couldn't understand that."
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True
    )