# Local Chatbot with Ollama and Streamlit

A simple, local chatbot implementation using [Ollama](https://ollama.com/) for LLM orchestration and [Streamlit](https://streamlit.io/) for the user interface.

## Prerequisites

1. **Install Ollama**: Download and install Ollama from [ollama.com](https://ollama.com/).
2. **Run Ollama**: Ensure the Ollama server is running on your machine.
3. **Pull a Model**: Open your terminal and pull a model to use. For example:
   ```bash
   ollama pull llama3
   ```

## Setup and Installation

This project is managed with `uv`. To set up the environment and run the application:

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the Streamlit app**:
   ```bash
   uv run streamlit run src/local_chatbot/app.py
   ```

## Features

- **Model Selection**: Choose from popular models or enter a custom model name in the sidebar.
- **Streaming Responses**: Responses are streamed in real-time for a better user experience.
- **Session History**: Conversation history is maintained during your session.
- **Chat Reset**: Clear the conversation history with a single click.

## Project Structure

- `src/local_chatbot/app.py`: The main Streamlit application logic.
- `pyproject.toml`: Project dependencies and metadata.
