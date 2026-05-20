import ast
import textwrap

def explain_code(code: str) -> str:
    """ 
    Produces a simple, beginner friendly explanation of the given code. 
    Instead of calling an LLM here, we will do a lightweight static analysis
    so the server has zero external dependencies.
    """

    code = code.strip()
    if not code:
        return "No code provided."

    lines = code.splitlines()
    findings = []

    # Count basic constructs via keyword scanning
    kw_counts = {
        "def":      sum(1 for l in lines if l.lstrip().startswith("def ")),
        "class":    sum(1 for l in lines if l.lstrip().startswith("class ")),
        "for":      sum(1 for l in lines if l.lstrip().startswith("for ")),
        "while":    sum(1 for l in lines if l.lstrip().startswith("while ")),
        "if":       sum(1 for l in lines if l.lstrip().startswith("if ")),
        "import":   sum(1 for l in lines if l.lstrip().startswith(("import ", "from "))),
        "return":   sum(1 for l in lines if "return " in l),
        "try":      sum(1 for l in lines if l.lstrip().startswith("try:")),
        "lambda":   sum(1 for l in lines if "lambda " in l),
        "list_comp":sum(1 for l in lines if "[" in l and " for " in l),
    }

    findings.append(f"The snippet is {len(lines)} line(s) long.")

    if kw_counts["import"]:
        findings.append(f"It imports {kw_counts['import']} module(s) — these bring in extra functionality.")
 
    if kw_counts["class"]:
        findings.append(f"It defines {kw_counts['class']} class(es) — blueprints for creating objects.")
 
    if kw_counts["def"]:
        findings.append(f"It defines {kw_counts['def']} function(s) — reusable blocks of logic.")
 
    if kw_counts["for"]:
        findings.append(f"It uses {kw_counts['for']} for-loop(s) — repeating actions over a sequence.")
 
    if kw_counts["while"]:
        findings.append(f"It uses {kw_counts['while']} while-loop(s) — repeating until a condition is False.")
 
    if kw_counts["if"]:
        findings.append(f"It has {kw_counts['if']} if-statement(s) — making decisions based on conditions.")
 
    if kw_counts["try"]:
        findings.append(f"It has try/except block(s) — handling errors gracefully.")
 
    if kw_counts["lambda"]:
        findings.append(f"It uses lambda expression(s) — tiny anonymous functions.")
 
    if kw_counts["list_comp"]:
        findings.append(f"It uses list comprehension(s) — a compact way to build lists.")
 
    if kw_counts["return"]:
        findings.append(f"It has {kw_counts['return']} return statement(s) — sending values back to the caller.")

    try:
        tree = ast.parse(code)
        func_names = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        class_names = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        if func_names:
            findings.append(f"Function name(s) found: {', '.join(func_names)}")
        if class_names:
            findings.append(f"Class name(s) found: {', '.join(class_names)}")
    except SyntaxError as e:
        findings.append(f"⚠️  Note: The code has a syntax error — {e}")
 
    explanation = "Here is a beginner-friendly explanation of the code:\n\n"
    explanation += "\n".join(f"  • {f}" for f in findings)
    explanation += "\n\nTip: Run it step-by-step in a Python REPL to see exactly what each part does!"
    return explanation


def format_code(code: str) -> str:
    """
    Applies basic formatting to messy Python code:
      - Normalises indentation to 4 spaces
      - Strips trailing whitespace from every line
      - Ensures a single blank line between top-level blocks
      - Adds a newline at the end of the file
    This is intentionally simple (no black/autopep8 dependency).
    """
    code = code.strip()
    if not code:
        return "# (empty input)"
 
    lines = code.splitlines()
    cleaned = []
 
    prev_was_blank = False
    for raw_line in lines:
        # Strip trailing spaces
        line = raw_line.rstrip()
 
        # Replace tabs with 4 spaces
        line = line.replace("\t", "    ")
 
        # Collapse multiple consecutive blank lines into one
        is_blank = (line.strip() == "")
        if is_blank and prev_was_blank:
            continue
 
        cleaned.append(line)
        prev_was_blank = is_blank
 
    # Ensure exactly one trailing newline
    formatted = "\n".join(cleaned).rstrip() + "\n"
    return formatted