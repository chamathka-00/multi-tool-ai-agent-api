from langchain_core.tools import tool
from datetime import datetime


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression and return the result. Use this for any math calculations."""
    # Only allow safe characters in the expression
    allowed_chars = set("0123456789+-*/.() ")
    if not all(c in allowed_chars for c in expression):
        return "Error: Invalid characters in expression. Only numbers and +-*/.() are allowed."
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
    
@tool
def analyze_text(text: str) -> str:
    """Analyze text and return statistics including word count, character count, and sentence count."""
    word_count = len(text.split())
    char_count = len(text)
    # Count sentence-ending punctuation
    sentence_count = text.count(".") + text.count("!") + text.count("?")
    if sentence_count == 0:
        sentence_count = 1
    return (
        f"Text Analysis:\n"
        f"- Words: {word_count}\n"
        f"- Characters: {char_count}\n"
        f"- Sentences: {sentence_count}"
    )

@tool
def get_current_datetime(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Get the current date and time. Optionally specify a format string."""
    try:
        return datetime.now().strftime(format)
    except ValueError as e:
        return f"Error with format string: {e}"