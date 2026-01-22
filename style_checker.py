import ast


def show_style_corrected(code: str) -> dict:
    """
    Formats Python code using AST unparsing.

    Returns:
    {
        success: bool,
        corrected_code: str,
        error: str | None
    }
    """

    if not code.strip():
        return {
            "success": False,
            "corrected_code": "",
            "error": "No code provided"
        }

    try:
        # Parse code into AST
        tree = ast.parse(code)

        # Convert AST back to formatted Python code
        formatted_code = ast.unparse(tree)

        return {
            "success": True,
            "corrected_code": formatted_code,
            "error": None
        }

    except SyntaxError as e:
        return {
            "success": False,
            "corrected_code": code,
            "error": f"SyntaxError: {e.msg} (line {e.lineno})"
        }

    except Exception as e:
        return {
            "success": False,
            "corrected_code": code,
            "error": f"Unexpected error: {str(e)}"
        }
