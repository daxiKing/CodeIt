CODEIT - LOCAL AI STARTER
=========================

What this package contains
--------------------------
app.py                 Local Streamlit chat application
Modelfile              CodeIt model personality/configuration
requirements.txt       Python dependencies
setup_codeit.ps1       Creates venv, installs packages, downloads model
start_codeit.ps1       Starts the local chat application
training/train.jsonl   Tiny example dataset for a later training stage

REQUIREMENTS
------------
- Windows 10/11 64-bit
- Python 3.11 or newer (Python 3.12 recommended)
- Ollama for Windows
- Internet for the initial downloads
- Several GB of free disk space for the model

INSTALL
-------
1. Install Python from https://www.python.org/downloads/
   Enable "Add Python to PATH".
2. Install Ollama from https://ollama.com/download/windows.
3. Extract this folder to C:\CodeIt (or another folder).
4. Open PowerShell in this folder.
5. If script execution is blocked, run:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
6. Run:
   .\setup_codeit.ps1

START
-----
Run:
   .\start_codeit.ps1

Then open:
   http://localhost:8501

NOTES
-----
- The setup script downloads qwen2.5-coder:7b, which can require
  several GB of disk space and may be demanding on a 6 GB GPU.
- If it is too slow or runs out of memory, use a smaller model:
  ollama pull qwen2.5-coder:3b
  Then edit the first line of Modelfile to:
  FROM qwen2.5-coder:3b
  Re-run:
  ollama create codeit -f .\Modelfile
- This starter creates a customized Ollama model configuration.
  It does NOT fine-tune model weights yet.
- The sample training dataset is only a format example, not enough
  data to meaningfully fine-tune a model.
- Chat history is stored locally in codeit.db.
- The first model download needs internet. Chatting works locally.

TROUBLESHOOTING
---------------
"ollama not found":
  Reinstall Ollama or reopen PowerShell after installation.

"Cannot connect to Ollama":
  Start the Ollama desktop app and retry.

PowerShell blocks scripts:
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

OpenAI API keys or paid APIs are not used.
