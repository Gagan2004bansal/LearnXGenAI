# Everything You Need to Know About This MCP Server

---

## Table of Contents
1. [What is MCP?](#1-what-is-mcp)
2. [Project Structure](#2-project-structure)
3. [The Four MCP Primitives](#3-the-four-mcp-primitives)
4. [How Each File Maps to MCP Concepts](#4-how-each-file-maps-to-mcp-concepts)
5. [Transport Layers: stdio vs SSE](#5-transport-layers-stdio-vs-sse)
6. [Step-by-Step Setup Guide](#6-step-by-step-setup-guide)
7. [Connecting to Claude Desktop](#7-connecting-to-claude-desktop)
8. [Testing with curl](#8-testing-with-curl)
9. [Testing with Postman](#9-testing-with-postman)
10. [JSON-RPC 2.0 Explained](#10-json-rpc-20-explained)
11. [Common Errors & Fixes](#11-common-errors--fixes)
12. [How to Extend This Server](#12-how-to-extend-this-server)
13. [MCP vs REST API — Key Differences](#13-mcp-vs-rest-api--key-differences)
14. [Further Reading](#14-further-reading)

---

## 1. What is MCP?

**Model Context Protocol (MCP)** is an open standard created by Anthropic that defines
how AI models (like Claude) communicate with *external tools and data sources*.

Think of it like **USB for AI** — a standard plug-and-play protocol so any LLM can
talk to any server without custom integrations.

```
┌──────────────────────┐        MCP Protocol         ┌────────────────────────┐
│   Claude Desktop /   │ ◄──────────────────────────► │   Your MCP Server      │
│   Claude API         │   (JSON-RPC over stdio/SSE)  │   (this project)       │
└──────────────────────┘                              └────────────────────────┘
         │                                                        │
    Sends requests:                                     Exposes:
    • list_tools                                        • Tools  (actions)
    • call_tool                                         • Resources (data)
    • list_resources                                    • Prompts (templates)
    • read_resource
    • list_prompts
    • get_prompt
```

### Why MCP instead of plain REST?

| Plain REST API            | MCP Server                            |
|---------------------------|---------------------------------------|
| You write custom code     | Claude auto-discovers capabilities    |
| No standard schema        | Standardised JSON Schema for tools    |
| Claude can't self-explore | Claude calls `list_tools` to explore  |
| Per-project integration   | Works with any MCP-compatible client  |

---

## 2. Project Structure

```
mcp-server/
│
├── main.py          ← Entry point. Wires everything together. Runs the server.
├── tools.py         ← Tool implementations (explain_code, format_code)
├── resources.py     ← Resource data (sample Python snippets)
├── prompts.py       ← Prompt templates (clean_explanation)
├── requirements.txt ← Python dependencies
└── learn.md         ← This file!
```

### Dependency graph
```
main.py
  ├── imports tools.py      (explain_code, format_code)
  ├── imports resources.py  (list_sample_codes, get_sample_code)
  └── imports prompts.py    (PROMPTS dict, get_clean_explanation_prompt)
```

`main.py` is the only file that knows about MCP internals (`FastMCP`).
The other three files are pure Python — easy to test independently.

---

## 3. The Four MCP Primitives

### 🔧 Tools
**What they are:** Functions that Claude can *invoke* to take actions or compute results.

**Analogies:**  
- Like a calculator button — you press it, you get an output.  
- Like a REST POST endpoint — sends input, gets output.

**Our tools:**
| Tool Name         | Input         | Output                          |
|-------------------|---------------|---------------------------------|
| `explain_code`    | Python string | Beginner-friendly explanation   |
| `format_code`     | Python string | Cleaned-up / formatted code     |

**JSON Schema Claude sees:**
```json
{
  "name": "explain_code_tool",
  "description": "Analyse a Python code snippet ...",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code": { "type": "string" }
    },
    "required": ["code"]
  }
}
```

---

### Resources
**What they are:** Read-only data sources Claude can *read* — like files, database rows,
or API responses. Identified by a **URI** (like a file path or URL).

**Analogies:**  
- Like a GET endpoint — read only, no side effects.  
- Like files in a filesystem — Claude asks for a path, gets the content.

**Our resources:**
| URI                            | Content                        |
|--------------------------------|--------------------------------|
| `sample://codes/list`          | List of all available snippets |
| `sample://codes/bubble_sort`   | Bubble sort source code        |
| `sample://codes/binary_search` | Binary search source code      |
| `sample://codes/fibonacci`     | Fibonacci source code          |
| `sample://codes/stack_class`   | Stack class source code        |
| `sample://codes/word_frequency`| Word frequency source code     |

---

### Prompts
**What they are:** Reusable message templates that pre-fill Claude's instructions.
They can accept arguments and return a structured list of messages.

**Analogies:**  
- Like a Word document template — fill in the blanks, get a ready-to-use document.  
- Like a system prompt factory — dynamically generated based on inputs.

**Our prompt:**
| Prompt Name         | Arguments            | What it does                         |
|---------------------|----------------------|--------------------------------------|
| `clean_explanation` | `code`, `level`      | Structured explanation at given level|

---

###  Sampling (not in this project, but good to know)
Sampling lets the server ask the *client* (Claude) to run an LLM inference.
This is how servers can chain AI calls without an API key of their own.
We don't use it here to keep things simple.

---

## 4. How Each File Maps to MCP Concepts

### `tools.py`
```
MCP Concept: Tools
Purpose:     Pure Python logic, no MCP SDK needed here.
Functions:
  explain_code(code: str) → str   — static analysis of a code string
  format_code(code: str)  → str   — basic whitespace / indentation cleanup
```

Key design choice: keeping tool logic in `tools.py` (not `main.py`) means
you can unit-test these functions without starting the server.

---

### `resources.py`
```
MCP Concept: Resources
Purpose:     Stores the actual data (code snippets) and helper functions.
Data:
  SAMPLE_CODES dict → { name: source_code_string }
Functions:
  list_sample_codes() → list of resource metadata dicts
  get_sample_code(name) → source string or None
```

---

### `prompts.py`
```
MCP Concept: Prompts
Purpose:     Builds the message list that Claude receives when a prompt is invoked.
Functions:
  get_clean_explanation_prompt(code, level) → list[PromptMessage]
Data:
  PROMPTS dict → registry of all prompts (name → handler + arg definitions)
```

The returned `PromptMessage` objects look like this in JSON:
```json
[
  { "role": "user", "content": { "type": "text", "text": "You are a coding tutor..." } },
  { "role": "user", "content": { "type": "text", "text": "Please explain: ..." } }
]
```

---

### `main.py`
```
MCP Concept: Server (the host that registers everything)
Purpose:     Wires tools/resources/prompts into the FastMCP app and starts the server.
Key lines:
  mcp = FastMCP("CodeHelper MCP")    ← create server
  @mcp.tool(...)                     ← register a tool
  @mcp.resource("sample://...")      ← register a resource
  @mcp.prompt(name="...")            ← register a prompt
  mcp.run(transport="sse")           ← start HTTP server
```

---

## 5. Transport Layers: stdio vs SSE

MCP supports two transports. This server supports both.

### stdio (Standard I/O)
```
Claude Desktop process
       │
       │  spawns subprocess
       ▼
  python main.py --stdio
       │
   JSON-RPC messages over stdin/stdout
```

- Claude Desktop **launches** your server as a child process.
- Communication happens via stdin/stdout (text lines of JSON).
- **Best for:** local development, Claude Desktop integration.
- **Config:** `"command": "python", "args": ["main.py", "--stdio"]`

---

### SSE (Server-Sent Events) over HTTP
```
Claude Desktop / API client
       │
       │  HTTP GET /sse  (long-lived connection)
       ▼
  python main.py  (running on port 8000)
       │
   JSON-RPC messages streamed as SSE events
```

- Your server runs **independently** and Claude connects to it over HTTP.
- Uses Server-Sent Events for the server→client stream, HTTP POST for client→server.
- **Best for:** deployed servers, shared across multiple clients.
- **Config:** `"url": "http://localhost:8000/sse"`

---

## 6. Step-by-Step Setup Guide

### Step 1 — Prerequisites
```bash
# Make sure Python 3.11+ is installed
python --version

# Make sure pip is up to date
pip install --upgrade pip
```

### Step 2 — Create a virtual environment
```bash
cd mcp-server
python -m venv venv

# Activate it:
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the server
```bash
# HTTP/SSE mode (for curl, Postman, or remote Claude Desktop):
python main.py

# stdio mode (for local Claude Desktop subprocess):
python main.py --stdio
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 5 — Verify it's alive
```bash
curl http://localhost:8000/
```

---

## 7. Connecting to Claude Desktop

Claude Desktop reads a JSON config file to know which MCP servers to connect to.

### Find your config file

| OS      | Path                                                               |
|---------|--------------------------------------------------------------------|
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`                      |
| Linux   | `~/.config/Claude/claude_desktop_config.json`                      |

### Option A — stdio (recommended for local dev, most reliable)

Claude Desktop spawns your Python process directly.

```json
{
  "mcpServers": {
    "code-helper": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-server/main.py", "--stdio"],
      "env": {}
    }
  }
}
```

> ⚠️ **Use the absolute path** to `main.py`. Relative paths do not work.
> Also make sure `python` resolves to Python 3.11+ in your shell.
> If you use a venv, point to `venv/bin/python` instead.

Example (macOS with venv):
```json
{
  "mcpServers": {
    "code-helper": {
      "command": "/Users/yourname/mcp-server/venv/bin/python",
      "args": ["/Users/yourname/mcp-server/main.py", "--stdio"]
    }
  }
}
```

---

### Option B — SSE / HTTP (for remote servers)

Start the server first (`python main.py`), then add to config:

```json
{
  "mcpServers": {
    "code-helper": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

---

### After editing the config

1. **Fully quit** Claude Desktop (Cmd+Q on Mac, not just close the window).
2. **Reopen** Claude Desktop.
3. Click the **🔌 plug icon** in the chat input area — your server should appear.
4. You'll see `explain_code_tool`, `format_code_tool` in the tools list.

---

## 8. Testing with curl

The SSE transport exposes a `/messages` POST endpoint for JSON-RPC calls.
Make sure the server is running (`python main.py`) before these commands.

### Initialize the session
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": { "name": "curl-test", "version": "1.0" }
    }
  }'
```

### List all tools
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'
```

### Call explain_code
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "explain_code_tool",
      "arguments": {
        "code": "def hello(name):\n    return f\"Hello, {name}!\""
      }
    }
  }'
```

### Call format_code
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "format_code_tool",
      "arguments": {
        "code": "def foo():\n\tx=1\n\t\ty=2\n\treturn x+y"
      }
    }
  }'
```

### List resources
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 5,
    "method": "resources/list",
    "params": {}
  }'
```

### Read a resource
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 6,
    "method": "resources/read",
    "params": {
      "uri": "sample://codes/bubble_sort"
    }
  }'
```

### List prompts
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 7,
    "method": "prompts/list",
    "params": {}
  }'
```

### Get a prompt
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 8,
    "method": "prompts/get",
    "params": {
      "name": "clean_explanation",
      "arguments": {
        "code": "print(\"hello\")",
        "level": "beginner"
      }
    }
  }'
```

---

## 9. Testing with Postman

1. Open Postman → **New Request**
2. Set method to **POST**
3. URL: `http://localhost:8000/messages`
4. Headers tab → Add: `Content-Type: application/json`
5. Body tab → Select **raw** → **JSON**
6. Paste any of the JSON bodies from Section 8 above
7. Click **Send**

**Pro tip:** In Postman, create a **Collection** called "MCP Server Tests" and save
each request as a separate item. Then you can run them all at once with
Collection Runner.

---

## 10. JSON-RPC 2.0 Explained

MCP uses JSON-RPC 2.0 as its message format. Here's the anatomy:

### Request
```json
{
  "jsonrpc": "2.0",      ← always this string
  "id": 42,              ← your tracking ID (any number or string)
  "method": "tools/list",← what you want to do
  "params": {}           ← arguments (object or array)
}
```

### Success Response
```json
{
  "jsonrpc": "2.0",
  "id": 42,              ← same id as the request
  "result": { ... }      ← the actual data
}
```

### Error Response
```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "error": {
    "code": -32601,        ← standard error codes (see below)
    "message": "Method not found",
    "data": "tools/nonexistent"
  }
}
```

### Standard Error Codes
| Code    | Meaning             |
|---------|---------------------|
| -32700  | Parse error         |
| -32600  | Invalid request     |
| -32601  | Method not found    |
| -32602  | Invalid params      |
| -32603  | Internal error      |

### MCP Method Namespaces
| Namespace    | Methods                                     |
|--------------|---------------------------------------------|
| `tools/`     | `tools/list`, `tools/call`                  |
| `resources/` | `resources/list`, `resources/read`          |
| `prompts/`   | `prompts/list`, `prompts/get`               |
| (root)       | `initialize`, `ping`                        |

---

## 11. Common Errors & Fixes

### ❌ `ModuleNotFoundError: No module named 'mcp'`
```bash
# Fix: install dependencies in your active venv
pip install -r requirements.txt
```

---

### ❌ `Address already in use` (port 8000 taken)
```bash
# Fix: kill the existing process or change the port in main.py
lsof -i :8000           # find the PID
kill -9 <PID>

# Or change port:
mcp.run(transport="sse", host="127.0.0.1", port=8001)
```

---

### ❌ Claude Desktop shows "Server disconnected"
- Make sure you used **absolute paths** in the config JSON.
- Make sure `python` in PATH points to Python 3.11+.
- Try running the exact command from your terminal first to see errors.
- Check Claude Desktop logs:
  - macOS: `~/Library/Logs/Claude/mcp-server-code-helper.log`
  - Windows: `%APPDATA%\Claude\logs\`

---

### ❌ curl returns 404 on `/messages`
The SSE server uses a two-phase connection:
1. First open `GET /sse` (this gives you a session endpoint URL in the SSE stream).
2. Then POST to that session-specific URL (e.g. `/messages?session_id=abc123`).

For simple testing, use the MCP Inspector tool (see Section 12).

---

### ❌ `PromptMessage` import error
```bash
# Make sure mcp package is ≥1.0.0
pip show mcp
pip install --upgrade mcp
```

---

## 12. How to Extend This Server

### Add a new tool
In `tools.py`, write a plain function:
```python
def count_lines(code: str) -> str:
    n = len(code.splitlines())
    return f"The snippet has {n} lines."
```

In `main.py`, register it:
```python
@mcp.tool(description="Count the number of lines in a code snippet.")
def count_lines_tool(code: str) -> str:
    from tools import count_lines
    return count_lines(code)
```

---

### Add a new resource
In `resources.py`, add to `SAMPLE_CODES`:
```python
"quicksort": '''
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)
'''
```

That's it — the `_make_resource` loop in `main.py` picks it up automatically.

---

### Add a new prompt
In `prompts.py`, write a handler:
```python
def get_debug_prompt(code: str, error: str) -> list[PromptMessage]:
    return [
        PromptMessage(role="user", content=TextContent(
            type="text",
            text=f"Debug this code:\n```python\n{code}\n```\nError: {error}"
        ))
    ]
```

In `main.py`, register it:
```python
@mcp.prompt(name="debug_helper", description="Help debug a Python error.")
def debug_helper_prompt(code: str, error: str):
    from prompts import get_debug_prompt
    return get_debug_prompt(code, error)
```

---

### Use the MCP Inspector (GUI testing tool)
```bash
npx @modelcontextprotocol/inspector python main.py --stdio
```

This opens a web UI at `http://localhost:5173` where you can:
- Browse tools, resources, prompts
- Call tools with a form UI
- See raw JSON-RPC messages

---

## 13. MCP vs REST API — Key Differences

| Aspect              | REST API                   | MCP Server                            |
|---------------------|----------------------------|---------------------------------------|
| **Discovery**       | Docs / OpenAPI spec        | `tools/list` at runtime               |
| **Schema**          | OpenAPI / manual           | JSON Schema auto-generated            |
| **Transport**       | HTTP (any client)          | stdio or SSE (MCP clients only)       |
| **State**           | Stateless (usually)        | Session-aware via SSE                 |
| **Auth**            | API keys, OAuth, etc.      | Optional (not in our server)          |
| **Primary user**    | Any HTTP client            | AI models / Claude Desktop            |
| **Data flow**       | Request → Response         | Request → Response + streaming events |
| **Best for**        | Web services, apps         | AI tool integration                   |

---

## 14. Further Reading

| Resource | URL |
|---|---|
| MCP Specification | https://spec.modelcontextprotocol.io |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| Claude Desktop MCP Docs | https://docs.anthropic.com/en/docs/claude-desktop/mcp |
| MCP Inspector Tool | https://github.com/modelcontextprotocol/inspector |
| FastMCP Docs | https://github.com/modelcontextprotocol/python-sdk/tree/main/src/mcp/server/fastmcp |
| JSON-RPC 2.0 Spec | https://www.jsonrpc.org/specification |

---

*Happy hacking! — Start with `python main.py` and connect Claude Desktop using Option A in Section 7.*