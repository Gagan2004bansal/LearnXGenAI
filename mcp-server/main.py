# main.py
# Entry point for the MCP server.
# Uses the official `mcp` SDK with FastAPI + SSE transport so Claude Desktop
# can connect to it as a remote MCP server over HTTP.

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from tools import explain_code, format_code
from resources import list_sample_codes, get_sample_code, SAMPLE_CODES
from prompts import PROMPTS

# ── 1. Create the FastMCP application ──────────────────────────────────────
#   `name`        → displayed in Claude Desktop's tool list
#   Instructions  → system-level hint Claude receives about this server
mcp = FastMCP(
    name="CodeHelper MCP",
    instructions=(
        "This server helps you understand and clean up Python code. "
        "Use explain_code to learn what a snippet does, "
        "format_code to tidy messy indentation, "
        "and sample_codes to browse ready-made examples."
    ),
)


# ── 2. Register Tools ───────────────────────────────────────────────────────
#   Tools are functions Claude can *call* during a conversation.
#   Decorated with @mcp.tool(); type annotations become the JSON schema.

@mcp.tool(
    description=(
        "Analyse a Python code snippet and return a beginner-friendly "
        "explanation of what it does, line by line."
    )
)
def explain_code_tool(code: str) -> str:
    """Explain what a piece of Python code does."""
    return explain_code(code)


@mcp.tool(
    description=(
        "Take messy Python code and return a cleaned-up version with "
        "consistent 4-space indentation, no trailing whitespace, and "
        "proper blank lines between blocks."
    )
)
def format_code_tool(code: str) -> str:
    """Format / clean up messy Python code."""
    return format_code(code)


# ── 3. Register Resources ───────────────────────────────────────────────────
#   Resources are read-only data Claude can *read* (like files or DB rows).
#   URI pattern: sample://codes/{snippet_name}

@mcp.resource("sample://codes/list")
def list_samples() -> str:
    """List all available sample code snippets."""
    items = list_sample_codes()
    lines = ["Available sample code snippets:\n"]
    for item in items:
        lines.append(f"  • {item['name']}  →  {item['uri']}")
    return "\n".join(lines)


# Register one resource per sample so each has its own URI
for _snippet_name in SAMPLE_CODES:

    # We need a closure to capture _snippet_name correctly
    def _make_resource(name: str):
        @mcp.resource(
            f"sample://codes/{name}",
            name=name,
            description=f"Sample Python snippet: {name.replace('_', ' ')}",
            mime_type="text/plain",
        )
        def _resource() -> str:
            code = get_sample_code(name)
            return code if code else f"# Sample '{name}' not found."
        return _resource

    _make_resource(_snippet_name)


# ── 4. Register Prompts ─────────────────────────────────────────────────────
#   Prompts are reusable message templates (pre-filled instructions for Claude).

@mcp.prompt(
    name="clean_explanation",
    description=(
        "Generate a structured, beginner-friendly explanation of a Python snippet. "
        "Pass `code` (required) and optionally `level` "
        "('beginner' | 'intermediate' | 'advanced')."
    ),
)
def clean_explanation_prompt(code: str, level: str = "beginner"):
    """Prompt template that produces clear, structured code explanations."""
    prompt_def = PROMPTS["clean_explanation"]
    return prompt_def["handler"](code=code, level=level)


# ── 5. Run ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    # Pass  `--stdio`  on the command line to use stdio transport
    # (required for Claude Desktop local process mode).
    # Default: SSE over HTTP on port 8000.
    if "--stdio" in sys.argv:
        # Claude Desktop can launch this as a local subprocess
        mcp.run(transport="stdio")
    else:
        # Remote HTTP server – Claude Desktop connects via SSE
        mcp.run(transport="sse")