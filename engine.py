import math
import re


def calculate(expression):

    expression = expression.lower().strip()

    expression = expression.replace("degrees", "")
    expression = expression.replace("degree", "")
    expression = expression.replace("°", "")

    expression = expression.replace(
        "square root of",
        "sqrt"
    )

    expression = expression.replace(
        "square root",
        "sqrt"
    )

    expression = expression.replace(" ", "")

    try:

        if expression.startswith("asin"):
            value = float(expression[4:])

            if value < -1 or value > 1:
                return "Invalid calculation"

            return format_result(
                math.degrees(
                    math.asin(value)
                )
            )

        if expression.startswith("acos"):
            value = float(expression[4:])

            if value < -1 or value > 1:
                return "Invalid calculation"

            return format_result(
                math.degrees(
                    math.acos(value)
                )
            )

        if expression.startswith("atan"):
            value = float(expression[4:])

            return format_result(
                math.degrees(
                    math.atan(value)
                )
            )

        if expression.startswith("sin"):
            value = float(expression[3:])

            return format_result(
                math.sin(
                    math.radians(value)
                )
            )

        if expression.startswith("cos"):
            value = float(expression[3:])

            return format_result(
                math.cos(
                    math.radians(value)
                )
            )

        if expression.startswith("tan"):
            value = float(expression[3:])

            radians = math.radians(value)

            if abs(math.cos(radians)) < 1e-10:
                return "Undefined"

            return format_result(
                math.tan(radians)
            )

        if expression.startswith("sqrt"):
            value = float(expression[4:])

            if value < 0:
                return "Invalid calculation"

            return format_result(
                math.sqrt(value)
            )

        if expression.startswith("log"):
            value = float(expression[3:])

            if value <= 0:
                return "Invalid calculation"

            return format_result(
                math.log10(value)
            )

        if expression.startswith("ln"):
            value = float(expression[2:])

            if value <= 0:
                return "Invalid calculation"

            return format_result(
                math.log(value)
            )

        if expression.endswith("!"):
            value = float(
                expression[:-1]
            )

            if value < 0 or value != int(value):
                return "Invalid calculation"

            return format_result(
                math.factorial(
                    int(value)
                )
            )

        expression = expression.replace(
            "^",
            "**"
        )

        expression = re.sub(
            r"(\d+(?:\.\d+)?)%",
            r"(\1/100)",
            expression
        )

        allowed = {
            "pi": math.pi,
            "e": math.e
        }

        result = eval(
            expression,
            {
                "__builtins__": {}
            },
            allowed
        )

        return format_result(result)

    except:
        return "Invalid calculation"


def format_result(value):

    if abs(value) < 1e-10:
        return "0"

    if abs(value - round(value)) < 1e-10:
        return str(
            int(round(value))
        )

    return str(
        round(value, 10)
    )


def get_explanation(expression, result):

    original = expression.strip()

    expression = expression.lower().strip()

    expression = expression.replace(
        "degrees",
        ""
    )

    expression = expression.replace(
        "degree",
        ""
    )

    expression = expression.replace(
        "°",
        ""
    )

    expression = expression.strip()


    if expression.startswith("sin"):

        value = expression[3:].strip()

        try:
            angle = float(value)
        except:
            angle = 0

        radians = math.radians(angle)

        x = math.cos(radians)
        y = math.sin(radians)

        return {
            "type": "sin",
            "expression": f"sin({value}°)",
            "result": result,
            "angle": angle,
            "unit_circle": {
                "x": format_result(x),
                "y": format_result(y)
            },
            "steps": [
                f"The given angle is {value}°.",
                "A unit circle has radius 1.",
                f"At {value}°, the point on the unit circle is ({format_result(x)}, {format_result(y)}).",
                "For an angle θ, sin(θ) is the y-coordinate of the point on the unit circle.",
                f"Therefore, sin({value}°) = {format_result(y)}."
            ]
        }


    if expression.startswith("cos"):

        value = expression[3:].strip()

        try:
            angle = float(value)
        except:
            angle = 0

        radians = math.radians(angle)

        x = math.cos(radians)
        y = math.sin(radians)

        return {
            "type": "cos",
            "expression": f"cos({value}°)",
            "result": result,
            "angle": angle,
            "unit_circle": {
                "x": format_result(x),
                "y": format_result(y)
            },
            "steps": [
                f"The given angle is {value}°.",
                "A unit circle has radius 1.",
                f"At {value}°, the point on the unit circle is ({format_result(x)}, {format_result(y)}).",
                "For an angle θ, cos(θ) is the x-coordinate of the point on the unit circle.",
                f"Therefore, cos({value}°) = {format_result(x)}."
            ]
        }


    if expression.startswith("tan"):

        value = expression[3:].strip()

        try:
            angle = float(value)
        except:
            angle = 0

        radians = math.radians(angle)

        x = math.cos(radians)
        y = math.sin(radians)

        if abs(x) < 1e-10:

            return {
                "type": "tan",
                "expression": f"tan({value}°)",
                "result": result,
                "angle": angle,
                "unit_circle": {
                    "x": format_result(x),
                    "y": format_result(y)
                },
                "steps": [
                    f"The given angle is {value}°.",
                    "A unit circle has radius 1.",
                    f"At {value}°, the point on the unit circle is ({format_result(x)}, {format_result(y)}).",
                    "tan(θ) = sin(θ) / cos(θ).",
                    "Here cos(θ) = 0, so division by zero occurs.",
                    f"Therefore, tan({value}°) is undefined."
                ]
            }

        tangent = y / x

        return {
            "type": "tan",
            "expression": f"tan({value}°)",
            "result": result,
            "angle": angle,
            "unit_circle": {
                "x": format_result(x),
                "y": format_result(y)
            },
            "steps": [
                f"The given angle is {value}°.",
                "A unit circle has radius 1.",
                f"At {value}°, the point on the unit circle is ({format_result(x)}, {format_result(y)}).",
                "tan(θ) = sin(θ) / cos(θ).",
                f"tan({value}°) = {format_result(y)} / {format_result(x)}.",
                f"Therefore, tan({value}°) = {format_result(tangent)}."
            ]
        }


    if expression.startswith("asin"):

        value = expression[4:].strip()

        return {
            "type": "asin",
            "expression": f"sin⁻¹({value})",
            "result": result,
            "steps": [
                f"The given value is {value}.",
                "Inverse sine finds the angle whose sine equals the given value.",
                f"Find the angle whose sine is {value}.",
                f"Therefore, sin⁻¹({value}) = {result}°."
            ]
        }


    if expression.startswith("acos"):

        value = expression[4:].strip()

        return {
            "type": "acos",
            "expression": f"cos⁻¹({value})",
            "result": result,
            "steps": [
                f"The given value is {value}.",
                "Inverse cosine finds the angle whose cosine equals the given value.",
                f"Find the angle whose cosine is {value}.",
                f"Therefore, cos⁻¹({value}) = {result}°."
            ]
        }


    if expression.startswith("atan"):

        value = expression[4:].strip()

        return {
            "type": "atan",
            "expression": f"tan⁻¹({value})",
            "result": result,
            "steps": [
                f"The given value is {value}.",
                "Inverse tangent finds the angle whose tangent equals the given value.",
                f"Find the angle whose tangent is {value}.",
                f"Therefore, tan⁻¹({value}) = {result}°."
            ]
        }


    if expression.startswith("sqrt"):

        value = expression[4:].strip()

        return {
            "type": "sqrt",
            "expression": f"√{value}",
            "result": result,
            "steps": [
                f"The given number is {value}.",
                "Square root finds the number which multiplied by itself gives the original number.",
                f"Calculate √{value}.",
                f"Therefore, √{value} = {result}."
            ]
        }


    if expression.startswith("log"):

        value = expression[3:].strip()

        return {
            "type": "log",
            "expression": f"log({value})",
            "result": result,
            "steps": [
                f"The given value is {value}.",
                "log means logarithm with base 10.",
                f"Calculate log₁₀({value}).",
                f"Therefore, log({value}) = {result}."
            ]
        }


    if expression.startswith("ln"):

        value = expression[2:].strip()

        return {
            "type": "ln",
            "expression": f"ln({value})",
            "result": result,
            "steps": [
                f"The given value is {value}.",
                "ln means natural logarithm with base e.",
                f"Calculate ln({value}).",
                f"Therefore, ln({value}) = {result}."
            ]
        }


    if expression.endswith("!"):

        value = expression[:-1].strip()

        return {
            "type": "factorial",
            "expression": f"{value}!",
            "result": result,
            "steps": [
                f"The given number is {value}.",
                f"Factorial means multiplying all positive integers from 1 to {value}.",
                f"Calculate {value}!",
                f"Therefore, {value}! = {result}."
            ]
        }


    if "^" in expression:

        parts = expression.split("^")

        return {
            "type": "power",
            "expression": original,
            "result": result,
            "steps": [
                f"The base is {parts[0]}.",
                f"The exponent is {parts[1]}.",
                f"Raise {parts[0]} to the power of {parts[1]}.",
                f"Therefore, {parts[0]}^{parts[1]} = {result}."
            ]
        }


    return {
        "type": "basic",
        "expression": original,
        "result": result,
        "steps": [
            f"The given expression is {original}.",
            "The calculator evaluates the expression.",
            f"The final result is {result}."
        ]
    }