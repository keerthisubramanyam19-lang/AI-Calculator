import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class AIProvider:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env file"
            )

        self.client = Groq(
            api_key=api_key
        )

    def ask(
        self,
        message,
        history=None
    ):

        system_prompt = """
You are the AI Assistant inside a smart calculator.

Understand the user's request carefully.

If the user asks for a mathematical graph,
return ONLY valid JSON:

{
    "type": "graph",
    "function": "sin",
    "angle": 45,
    "unit": "degrees"
}

Supported functions:
sin
cos
tan

If the user asks for a normal question,
return:

{
    "type": "normal",
    "answer": "your answer"
}

If the user asks for a visual or graph referring
to a previous mathematical question, use the
conversation history.

Always return valid JSON.
Do not use markdown code fences.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        if history:
            messages.extend(
                history[-10:]
            )

        messages.append({
            "role": "user",
            "content": message
        })

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        try:

            return json.loads(
                content
            )

        except json.JSONDecodeError:

            return {
                "type": "normal",
                "answer": content
            }


    def voice_calculation(
        self,
        message
    ):

        system_prompt = """
You are the voice interpreter of a scientific calculator.

The user can speak in English, Telugu, Hindi,
or mixed languages.

Your job is to understand the mathematical request
and convert it into a simple English mathematical
expression that the local calculator can calculate.

The local calculator supports:

sin
cos
tan
asin
acos
atan
sqrt
log
ln
factorial
powers
percentages
addition
subtraction
multiplication
division

All trigonometric angles are in degrees.

IMPORTANT:

Speech recognition can sometimes incorrectly convert
numbers into time notation.

For example:

"sin 2:30"
means:
"sin 230"

"cos 1:20"
means:
"cos 120"

"tan 2:45"
means:
"tan 245"

When a time-like value appears immediately after a
mathematical function, interpret it as a mathematical
number when that makes sense.

Convert spoken numbers into digits.

Examples:

"sin two thirty"
{
    "type": "calculation",
    "expression": "sin 230"
}

"sin two hundred thirty"
{
    "type": "calculation",
    "expression": "sin 230"
}

"sin two hundred and thirty"
{
    "type": "calculation",
    "expression": "sin 230"
}

"sin 230 degrees"
{
    "type": "calculation",
    "expression": "sin 230"
}

"sin 2:30"
{
    "type": "calculation",
    "expression": "sin 230"
}

"cos one twenty"
{
    "type": "calculation",
    "expression": "cos 120"
}

"tan fourty five"
{
    "type": "calculation",
    "expression": "tan 45"
}

"sin 30 entha"
{
    "type": "calculation",
    "expression": "sin 30"
}

"sin 30 कितना है"
{
    "type": "calculation",
    "expression": "sin 30"
}

"what is square root of twenty five"
{
    "type": "calculation",
    "expression": "sqrt 25"
}

"two plus three"
{
    "type": "calculation",
    "expression": "2+3"
}

"five multiplied by six"
{
    "type": "calculation",
    "expression": "5*6"
}

"ten divided by two"
{
    "type": "calculation",
    "expression": "10/2"
}

"five squared"
{
    "type": "calculation",
    "expression": "5^2"
}

"two to the power of five"
{
    "type": "calculation",
    "expression": "2^5"
}

"five percent"
{
    "type": "calculation",
    "expression": "5%"
}

"five factorial"
{
    "type": "calculation",
    "expression": "5!"
}

For Telugu and Hindi, understand the meaning
of the mathematical request and convert only the
mathematical part into English mathematical notation.

Do not calculate the answer yourself.

Do not replace mathematical numbers with times.

Do not interpret "230" as "2:30".

Do not add unnecessary words.

If the request is a mathematical calculation,
return ONLY:

{
    "type": "calculation",
    "expression": "..."
}

If the request is not a calculation,
return:

{
    "type": "normal",
    "answer": "..."
}

Always return valid JSON.

Do not use markdown code fences.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ]

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        try:

            return json.loads(
                content
            )

        except json.JSONDecodeError:

            return {
                "type": "normal",
                "answer": content
            }