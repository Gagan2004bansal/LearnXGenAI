# prompts.py
# MCP Prompts: reusable message templates that guide how the LLM should respond.
# A prompt has a name, optional description, optional arguments, and returns
# a list of messages (role + content) ready to send to the model.

from mcp.types import PromptMessage, TextContent


def get_clean_explanation_prompt(code: str, level: str = "beginner") -> list[PromptMessage]:
    """
    Returns a prompt that instructs Claude to explain code in a beginner-friendly way.

    Arguments:
        code  – the Python snippet to explain
        level – audience level: 'beginner', 'intermediate', or 'advanced'
    """
    level_guidance = {
        "beginner": (
            "Assume the reader has never programmed before. "
            "Avoid all jargon. Use everyday analogies. "
            "Explain EVERY keyword (def, for, if, return, etc.)."
        ),
        "intermediate": (
            "Assume the reader knows basic Python syntax. "
            "Skip obvious things like what a for-loop is, but do explain "
            "any algorithms, data structures, or design decisions."
        ),
        "advanced": (
            "Assume the reader is a Python developer. "
            "Focus on performance, edge cases, Pythonic idioms, and potential improvements."
        ),
    }.get(level, "Explain clearly and concisely.")

    system_text = (
        "You are a patient and encouraging coding tutor. "
        "Your goal is to make code understandable to anyone. "
        f"{level_guidance} "
        "Structure your answer as:\n"
        "1. **What it does** – one sentence summary.\n"
        "2. **Key parts** – bullet list of important lines/blocks.\n"
        "3. **How it flows** – walkthrough in plain English.\n"
        "4. **Pro tip** – one improvement or interesting fact."
    )

    user_text = f"Please explain this Python code:\n\n```python\n{code}\n```"

    return [
        PromptMessage(role="user", content=TextContent(type="text", text=system_text)),
        PromptMessage(role="user", content=TextContent(type="text", text=user_text)),
    ]


# Registry – maps prompt name → (handler, argument definitions)
PROMPTS = {
    "clean_explanation": {
        "description": "Generates a beginner-friendly explanation prompt for a Python snippet.",
        "arguments": [
            {
                "name": "code",
                "description": "The Python code you want explained.",
                "required": True,
            },
            {
                "name": "level",
                "description": "Audience level: 'beginner' (default), 'intermediate', or 'advanced'.",
                "required": False,
            },
        ],
        "handler": get_clean_explanation_prompt,
    }
}