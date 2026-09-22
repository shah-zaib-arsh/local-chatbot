# 🤖 Local Chatbot with Ollama and Streamlit

A simple and privacy-focused local AI chatbot built with **Python**, **Ollama**, and **Streamlit**.

The application connects to your locally running Ollama server and lets you chat with installed local language models through a clean web interface. No cloud API key is required for the chatbot itself.


## ✨ Features

- 🦙 **Ollama integration**: Uses models running on your local machine.
- 💬 **Interactive chat UI**: Clean Streamlit-based chatbot interface.
- ⚡ **Streaming responses**: AI responses appear in real time.
- 🤖 **Automatic model discovery**: Shows only models installed in your local Ollama server.
- 🎯 **Model selection**: Switch between available local models from the sidebar.
- 🧠 **Custom system prompt**: Control how the AI behaves and responds.
- 🌡️ **Temperature control**: Adjust response creativity.
- 📚 **Context length control**: Choose the context window used for generation.
- 🔄 **Regenerate response**: Regenerate the latest assistant response.
- 🗑️ **Clear chat**: Remove the current conversation history.
- 📄 **Export chat as TXT**: Download your conversation as a text file.
- 📦 **Export chat as JSON**: Save conversation data and settings in JSON format.
- 📊 **Chat statistics**: Displays token count and generation time when provided by Ollama.
- 🔌 **Connection status**: Shows whether the local Ollama server is online or offline.
- 🌙 **Dark interface**: Custom styling for a modern dark UI.


## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.14** | Application programming language |
| **Streamlit** | Web-based user interface |
| **Ollama** | Local LLM runtime and API |
| **uv** | Python environment and dependency management |

---

## 📋 Prerequisites

Before running the project, install:

### 1. Python

This project is configured for:

```text
Python 3.14
```

### 2. Ollama

Download and install Ollama:

- https://ollama.com/

After installation, make sure the Ollama server is running.

The application connects to:

```text
http://127.0.0.1:11434
```

### 3. uv

This project uses `uv` to manage the Python environment and dependencies.

Install `uv` if you do not already have it:

- https://docs.astral.sh/uv/

---

## 📥 Install the Project

Clone the repository:

```bash
git clone https://github.com/shah-zaib-arsh/local-chatbot.git
```

Move into the project directory:

```bash
cd local-chatbot
```

Sync the project environment and install dependencies:

```bash
uv sync
```

---

## 🦙 Install an Ollama Model

The application automatically detects models installed on your local Ollama server.

For example:

```bash
ollama pull gemma3:4b
```

or:

```bash
ollama pull qwen2.5:3b
```

Check installed models with:

```bash
ollama list
```

You can install any compatible Ollama model and select it from the application's sidebar.

---

## ▶️ Run the Application

Because `app.py` is located in the project root, run:

```bash
uv run streamlit run app.py
```

Streamlit will display a local web address, usually similar to:

```text
http://localhost:8501
```

Open that address in your browser.

---

## 🖥️ How It Works

The application follows this basic flow:

```text
User
  │
  ▼
Streamlit Web UI
  │
  ▼
Python Application (app.py)
  │
  ▼
Ollama Python Client
  │
  ▼
Local Ollama Server
  │
  ▼
Installed Local LLM
  │
  ▼
Streaming Response
  │
  ▼
Streamlit Chat UI
```

Your prompts are sent to the Ollama server running on your own machine.

---

## ⚙️ Configuration

The Ollama host is configured in `app.py`:

```python
OLLAMA_HOST = "http://127.0.0.1:11434"
```

The application uses the following generation settings:

- **Temperature** — Controls how focused or creative the response is.
- **Context length** — Controls how much conversation context is sent to the model.
- **System prompt** — Defines the assistant's behavior and instructions.

These settings can be changed directly from the sidebar while using the application.

---

## 🤖 Model Selection

The application does **not** require you to manually type a model name.

It asks Ollama for the locally installed models and displays them automatically.

For each detected model, the sidebar can show information such as:

- Model name
- Model family
- Parameter size
- Model size
- Quantization level

By default, the application prefers:

```text
gemma3:4b
```

when that model is installed. Otherwise, it selects an available local model.

---

## 💬 Chat Features

### Conversation History

Messages are stored in Streamlit session state while the current session is active.

### Regenerate

When the last message is an assistant response, the **Regenerate** button removes that response so you can generate a new answer.

### Clear Chat

The **Clear Chat** button removes the current conversation history.

### Export

You can export the conversation as:

```text
ollama_chat.txt
```

or:

```text
ollama_chat.json
```

The JSON export also includes the selected model, system prompt, temperature, context length, and export timestamp.

---

## 📁 Project Structure

```text
shah-zaib-arsh-local-chatbot/
│
├── README.md
├── app.py
├── pyproject.toml
├── .python-version
│
└── src/
    └── local_chatbot/
        └── __init__.py
```

### Important Files

**`app.py`**

Main Streamlit application containing:

- Ollama connection
- Model discovery
- Chat interface
- Streaming response handling
- Generation settings
- Session history
- Chat export
- Custom UI styling

**`pyproject.toml`**

Contains project metadata and Python dependencies.

**`.python-version`**

Specifies:

```text
3.14
```

**`src/local_chatbot/__init__.py`**

Contains the package entry point defined by the project configuration.

---

## 🔧 Troubleshooting

### Ollama is Offline

If the application shows:

```text
OFFLINE
```

make sure Ollama is running.

You can verify the installed models with:

```bash
ollama list
```

Then restart the Streamlit application.

---

### No Models Found

Install a model first:

```bash
ollama pull gemma3:4b
```

Then click:

```text
Refresh Models
```

inside the application sidebar.

---

### Check Ollama Server

The application expects Ollama at:

```text
http://127.0.0.1:11434
```

If your Ollama server uses a different host or port, update `OLLAMA_HOST` in `app.py`.

---

### Streamlit Command Not Found

Use `uv` to run Streamlit:

```bash
uv run streamlit run app.py
```

This ensures the project's environment and dependencies are used.

---

## 🔒 Privacy

This project is designed for local AI usage.

The chatbot connects to the Ollama server running on your computer rather than requiring a remote LLM API for the chat generation.

Your actual privacy also depends on the Ollama setup, installed models, operating system, and any other software running on your machine.

---

## 🚀 Future Improvements

Possible improvements for future versions include:

- Persistent chat history
- Multiple conversations
- Chat history database
- Markdown file upload
- PDF/document chat
- RAG with local documents
- Token usage dashboard
- Ollama model download management
- Custom model parameters
- Authentication
- Better mobile UI
- Voice input and text-to-speech


## 👨‍💻 Author

**Shahzaib Arshed**

GitHub:

https://github.com/shah-zaib-arsh/local-chatbot

Gmail:
mrshahzaib903@gmail.com

Linkedin:
https://www.linkedin.com/in/muhammad-shahzaib-arshed/

---

## ⭐ Support

If this project is useful to you, consider giving the repository a ⭐ on GitHub.
