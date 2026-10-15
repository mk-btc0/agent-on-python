import os
import platform
import subprocess
import webbrowser
from datetime import datetime
from openai import OpenAI

# ============ API KEY ============
API_KEY = "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"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# ============ TOOLS (REAL ACTIONS) ============

def create_file(filename: str, content: str = "") -> str:
    """Create a file with content."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{filename}' created ({len(content)} chars)."
    except Exception as e:
        return f"Error: {e}"


def read_file(filename: str) -> str:
    """Read a file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return f"Content of '{filename}':\n{content[:500]}"
    except Exception as e:
        return f"Error: {e}"


def delete_file(filename: str) -> str:
    """Delete a file."""
    try:
        os.remove(filename)
        return f"File '{filename}' deleted."
    except Exception as e:
        return f"Error: {e}"


def list_files(folder: str = ".") -> str:
    """List files in a folder."""
    try:
        files = os.listdir(folder)
        return f"Files in '{folder}':\n" + "\n".join(f"  - {f}" for f in files)
    except Exception as e:
        return f"Error: {e}"


def run_command(command: str) -> str:
    """Run a terminal command (Windows)."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        output = (result.stdout or "") + (result.stderr or "")
        return f"Command: {command}\nOutput:\n{output[:500] or '(no output)'}"
    except Exception as e:
        return f"Error: {e}"


def open_website(url: str) -> str:
    """Open a website in browser."""
    try:
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opened {url} in browser."
    except Exception as e:
        return f"Error: {e}"


def calculator(expr: str) -> str:
    """Evaluate math expression."""
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}"


def get_time(_: str = "") -> str:
    """Get current time and date."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def system_info(_: str = "") -> str:
    """Get system information."""
    return (
        f"OS: {platform.system()} {platform.release()}\n"
        f"Python: {platform.python_version()}\n"
        f"Machine: {platform.machine()}\n"
        f"User: {os.getlogin()}\n"
        f"CWD: {os.getcwd()}"
    )


def write_note(note: str, filename: str = "notes.txt") -> str:
    """Append a note to a file."""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {note}\n")
        return f"Note added to '{filename}'."
    except Exception as e:
        return f"Error: {e}"


# ============ TOOL REGISTRY ============

TOOLS = {
    "create_file": create_file,
    "read_file": read_file,
    "delete_file": delete_file,
    "list_files": list_files,
    "run_command": run_command,
    "open_website": open_website,
    "calculator": calculator,
    "get_time": get_time,
    "system_info": system_info,
    "write_note": write_note,
}


TOOL_SCHEMA = [
    {"type": "function", "function": {
        "name": "create_file",
        "description": "Create a new file with content",
        "parameters": {"type": "object", "properties": {
            "filename": {"type": "string"},
            "content": {"type": "string"}}, "required": ["filename"]}}},
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read content of a file",
        "parameters": {"type": "object", "properties": {
            "filename": {"type": "string"}}, "required": ["filename"]}}},
    {"type": "function", "function": {
        "name": "delete_file",
        "description": "Delete a file",
        "parameters": {"type": "object", "properties": {
            "filename": {"type": "string"}}, "required": ["filename"]}}},
    {"type": "function", "function": {
        "name": "list_files",
        "description": "List files in a folder",
        "parameters": {"type": "object", "properties": {
            "folder": {"type": "string"}}}}},
    {"type": "function", "function": {
        "name": "run_command",
        "description": "Run a terminal command (cmd on Windows)",
        "parameters": {"type": "object", "properties": {
            "command": {"type": "string"}}, "required": ["command"]}}},
    {"type": "function", "function": {
        "name": "open_website",
        "description": "Open a website in default browser",
        "parameters": {"type": "object", "properties": {
            "url": {"type": "string"}}, "required": ["url"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate a math expression",
        "parameters": {"type": "object", "properties": {
            "expr": {"type": "string"}}, "required": ["expr"]}}},
    {"type": "function", "function": {
        "name": "get_time",
        "description": "Get current date and time",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "system_info",
        "description": "Get system information (OS, Python, user, CWD)",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "write_note",
        "description": "Append a note to notes.txt",
        "parameters": {"type": "object", "properties": {
            "note": {"type": "string"},
            "filename": {"type": "string"}}, "required": ["note"]}}},
]


# ============ AGENT LOOP ============

def run_agent(task, max_steps=8):
    messages = [
        {"role": "system", "content": (
            "You are an AI agent that performs REAL actions on the user's computer. "
            "You have tools: create_file, read_file, delete_file, list_files, "
            "run_command, open_website, calculator, get_time, system_info, write_note. "
            "ALWAYS answer ONLY in English. Never use Chinese or any other language. "
            "IMPORTANT: Your final answer MUST be in English. "
            "If you write in Chinese — that is a mistake. Check the language before outputting. "
            "Use tools whenever the user asks to DO something. "
            "Explain briefly what you did."
        )},
        {"role": "user", "content": task},
    ]

    for i in range(max_steps):
        r = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=TOOL_SCHEMA,
            tool_choice="auto",
        )
        msg = r.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for c in msg.tool_calls:
                try:
                    args = eval(c.function.arguments) if c.function.arguments else {}
                except Exception:
                    args = {}
                result = TOOLS[c.function.name](**args) if args else TOOLS[c.function.name]()
                print(f"[TOOL] {c.function.name}({args})")
                print(f"   -> {result[:150]}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": c.id,
                    "content": str(result),
                })
        else:
            print(f"\n[DONE] {msg.content}\n")
            return
    print("Step limit reached.")


# ============ MAIN ============

if __name__ == "__main__":
    print("=" * 50)
    print("   AI AGENT - REAL TASK EXECUTOR")
    print("=" * 50)
    print("Try commands like:")
    print("  - create a file hello.txt with 'Hi there'")
    print("  - list all files in this folder")
    print("  - open youtube.com")
    print("  - show system info")
    print("  - what time is it")
    print("  - save note: buy milk")
    print("  - run command: dir")
    print("=" * 50 + "\n")

    while True:
        task = input("Your task (or 'exit'): ").strip()
        if task.lower() in ("exit", "quit", "q"):
            print("Bye!")
            break
        if not task:
            continue
        run_agent(task)