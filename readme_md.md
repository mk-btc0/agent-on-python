# AI Agent - Real Task Executor on Groq API

An autonomous, lightweight Python AI agent powered by the **Groq API** (`openai/gpt-oss-120b`). This agent bridges natural language instructions with real system actions, enabling it to manage files, execute shell commands, browse the web, perform calculations, and inspect system environments.

---

## 🚀 Features

- **Real-World Execution**: Interacts directly with your local machine's filesystem, shell, and browser.
- **Autonomous Tool Selection**: Uses OpenAI-compatible `tool_calls` schema routing to select the correct function dynamically based on user intent.
- **Multi-Step ReAct Loop**: Capable of multi-step reasoning chains (up to 8 steps by default) to solve complex nested instructions.
- **Robust Error Handling**: Safely catches exceptions across file I/O, subprocess execution, and mathematical evaluations.

---

## 🛠️ Available Tools

| Tool Name | Description | Parameters |
| :--- | :--- | :--- |
| `create_file` | Creates a new file with optional text content. | `filename` (str), `content` (str) |
| `read_file` | Reads the first 500 characters of a file. | `filename` (str) |
| `delete_file` | Deletes a specified file from disk. | `filename` (str) |
| `list_files` | Lists all contents of a target directory. | `folder` (str, default: `"."`) |
| `run_command` | Runs a shell/terminal command with a 15s timeout. | `command` (str) |
| `open_website` | Opens any web URL in your default browser. | `url` (str) |
| `calculator` | Evaluates safe inline Python mathematical expressions. | `expr` (str) |
| `get_time` | Retrieves current system date and timestamp. | None |
| `system_info` | Inspects OS details, Python version, user, and CWD. | None |
| `write_note` | Appends timestamped notes to a text file. | `note` (str), `filename` (str) |

---

## ⚙️ Installation & Setup

1. **Clone or save** the script as `agent.py`.
2. **Install dependencies**:
   ```bash
   pip install openai
   ```
3. **Configure your API Key**:
   Make sure your Groq API key is set correctly in the script:
   ```python
   API_KEY = "your_groq_api_key_here"
   ```

---

## 🚀 Usage

Run the script from your terminal:
```bash
python agent.py
```

Once started, type any natural language task at the interactive prompt:

```text
==================================================
   AI AGENT - REAL TASK EXECUTOR
==================================================
Try commands like:
  - create a file hello.txt with 'Hi there'
  - list all files in this folder
  - open youtube.com
  - show system info
  - what time is it
  - save note: buy milk
  - run command: dir
==================================================

Your task (or 'exit'): 
```

---

## 🔒 Safety & Disclaimer
This script executes real commands and writes files directly to your operating system via subprocess and file I/O operations. Use it with caution and review tasks before execution in production environments.