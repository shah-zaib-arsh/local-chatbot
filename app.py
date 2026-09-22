import streamlit as st
from ollama import Client
import json
from datetime import datetime


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Ollama Local Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Ollama Configuration
# ============================================================

OLLAMA_HOST = "http://127.0.0.1:11434"

client = Client(host=OLLAMA_HOST)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
    }

    /* Main content */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Cards */
    .info-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .model-name {
        font-size: 1.15rem;
        font-weight: 600;
    }

    .model-detail {
        color: #8b949e;
        font-size: 0.88rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
    }

    /* Chat messages */
    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        margin-bottom: 10px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 9px;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        border-radius: 9px;
    }

    /* Status badge */
    .status-online {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        background: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .status-offline {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        background: rgba(248, 81, 73, 0.15);
        color: #f85149;
        font-size: 0.85rem;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are a helpful local AI assistant. "
        "Answer clearly and accurately. "
        "Use simple explanations when possible."
    )

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "context_length" not in st.session_state:
    st.session_state.context_length = 4096


# ============================================================
# Helper Functions
# ============================================================

def get_value(obj, key, default=None):
    """
    Safely get a property from Ollama's response object.
    Supports both object-style and dictionary-style responses.
    """

    try:
        value = getattr(obj, key)

        if callable(value):
            return default

        return value

    except Exception:
        pass

    if isinstance(obj, dict):
        return obj.get(key, default)

    return default


def format_size(size_bytes):
    """
    Convert bytes into readable GB/MB.
    """

    if not size_bytes:
        return "Unknown"

    try:
        size_bytes = int(size_bytes)

        if size_bytes >= 1024**3:
            return f"{size_bytes / (1024**3):.2f} GB"

        if size_bytes >= 1024**2:
            return f"{size_bytes / (1024**2):.0f} MB"

        if size_bytes >= 1024:
            return f"{size_bytes / 1024:.0f} KB"

        return f"{size_bytes} B"

    except Exception:
        return "Unknown"


def get_available_models():
    """
    Return ONLY models installed on the local Ollama server.

    No manually entered model names are accepted.
    """

    try:
        response = client.list()

        models = []

        response_models = get_value(response, "models", [])

        if not response_models:
            return [], None

        for model in response_models:

            name = get_value(model, "model")

            if not name:
                name = get_value(model, "name")

            if name:

                models.append(
                    {
                        "name": str(name),
                        "size": get_value(model, "size"),
                        "parameter_size": get_value(
                            get_value(model, "details", {}),
                            "parameter_size"
                        ),
                        "family": get_value(
                            get_value(model, "details", {}),
                            "family"
                        ),
                        "quantization": get_value(
                            get_value(model, "details", {}),
                            "quantization_level"
                        ),
                    }
                )

        # Remove duplicate model names
        unique_models = {}

        for model in models:
            unique_models[model["name"]] = model

        models = list(unique_models.values())

        models.sort(key=lambda x: x["name"].lower())

        return models, None

    except Exception as e:
        return [], str(e)


def build_chat_messages():
    """
    Build messages sent to Ollama.
    The system prompt is kept separate from visible chat history.
    """

    messages = []

    if st.session_state.system_prompt.strip():
        messages.append(
            {
                "role": "system",
                "content": st.session_state.system_prompt.strip(),
            }
        )

    messages.extend(st.session_state.messages)

    return messages


def generate_response(model_name):
    """
    Stream response from Ollama.
    """

    response_placeholder = st.empty()

    full_response = ""

    options = {
        "temperature": st.session_state.temperature,
        "num_ctx": st.session_state.context_length,
    }

    try:

        stream = client.chat(
            model=model_name,
            messages=build_chat_messages(),
            stream=True,
            options=options,
        )

        final_chunk = None

        for chunk in stream:

            final_chunk = chunk

            content = ""

            # New Ollama Python API
            try:
                if hasattr(chunk, "message") and chunk.message:
                    content = chunk.message.content or ""
            except Exception:
                content = ""

            # Dictionary fallback
            if not content and isinstance(chunk, dict):

                try:
                    content = chunk["message"]["content"]
                except Exception:
                    content = ""

            if content:

                full_response += content

                response_placeholder.markdown(
                    full_response + "▌"
                )

        # Remove cursor
        response_placeholder.markdown(full_response)

        # Get final statistics when available
        eval_count = None
        total_duration = None

        if final_chunk:

            eval_count = get_value(
                final_chunk,
                "eval_count"
            )

            total_duration = get_value(
                final_chunk,
                "total_duration"
            )

        # Convert nanoseconds to seconds
        duration_seconds = None

        if total_duration:
            try:
                duration_seconds = total_duration / 1_000_000_000
            except Exception:
                pass

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response,
            }
        )

        return full_response, eval_count, duration_seconds, None

    except Exception as e:

        return "", None, None, str(e)


def clear_chat():
    st.session_state.messages = []


def export_chat_json():
    return json.dumps(
        {
            "exported_at": datetime.now().isoformat(),
            "model": st.session_state.selected_model,
            "system_prompt": st.session_state.system_prompt,
            "temperature": st.session_state.temperature,
            "context_length": st.session_state.context_length,
            "messages": st.session_state.messages,
        },
        indent=2,
        ensure_ascii=False,
    )


def export_chat_txt():

    lines = []

    for message in st.session_state.messages:

        role = message["role"].upper()

        lines.append(
            f"{role}\n{message['content']}\n"
        )

    return "\n".join(lines)


# ============================================================
# Get Local Models
# ============================================================

available_models, connection_error = get_available_models()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("⚙️ Configuration")

    # --------------------------------------------------------
    # Connection Status
    # --------------------------------------------------------

    st.subheader("Ollama")

    if connection_error:

        st.markdown(
            '<span class="status-offline">'
            "● OFFLINE"
            "</span>",
            unsafe_allow_html=True,
        )

        st.error(
            "Could not connect to local Ollama."
        )

        st.caption("Ollama host")

        st.code(
            OLLAMA_HOST,
            language="text"
        )

        st.caption("Error")

        st.code(
            connection_error,
            language="text"
        )

        st.info(
            "Start Ollama and then click Refresh Models."
        )

    else:

        st.markdown(
            '<span class="status-online">'
            "● ONLINE"
            "</span>",
            unsafe_allow_html=True,
        )

        st.caption(
            f"Local server: {OLLAMA_HOST}"
        )

    # --------------------------------------------------------
    # Refresh Models
    # --------------------------------------------------------

    if st.button(
        "🔄 Refresh Models",
        use_container_width=True,
    ):

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # Model Selection
    # --------------------------------------------------------

    st.subheader("🤖 Local Models")

    if available_models:

        model_names = [
            model["name"]
            for model in available_models
        ]

        # Keep previously selected model if still installed
        if (
            st.session_state.selected_model
            not in model_names
        ):

            preferred_model = "gemma3:4b"

            if preferred_model in model_names:
                st.session_state.selected_model = (
                    preferred_model
                )
            else:
                st.session_state.selected_model = (
                    model_names[0]
                )

        selected_model = st.selectbox(
            "Select installed model",
            options=model_names,
            index=model_names.index(
                st.session_state.selected_model
            ),
        )

        st.session_state.selected_model = selected_model

        # Find selected model details
        selected_model_info = next(
            (
                model
                for model in available_models
                if model["name"] == selected_model
            ),
            None,
        )

        if selected_model_info:

            st.markdown(
                '<div class="info-card">',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="model-name">'
                f'{selected_model_info["name"]}'
                f"</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="model-detail">'
                f'Family: '
                f'{selected_model_info["family"] or "Unknown"}'
                f"</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="model-detail">'
                f'Parameters: '
                f'{selected_model_info["parameter_size"] or "Unknown"}'
                f"</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="model-detail">'
                f'Size: '
                f'{format_size(selected_model_info["size"])}'
                f"</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="model-detail">'
                f'Quantization: '
                f'{selected_model_info["quantization"] or "Unknown"}'
                f"</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

        st.caption(
            f"{len(model_names)} installed model(s) found"
        )

    else:

        st.warning(
            "No locally installed models found."
        )

        if not connection_error:

            st.info(
                "Install a model with Ollama first, "
                "then click Refresh Models."
            )

            st.code(
                "ollama pull gemma3:4b\n"
                "ollama pull qwen2.5:3b",
                language="powershell",
            )

    st.divider()

    # --------------------------------------------------------
    # Generation Settings
    # --------------------------------------------------------

    st.subheader("🎛️ Generation")

    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state.temperature,
        step=0.1,
        help=(
            "Lower values make responses more focused. "
            "Higher values make them more creative."
        ),
    )

    st.session_state.context_length = st.select_slider(
        "Context length",
        options=[
            1024,
            2048,
            4096,
            8192,
            16384,
            32768,
        ],
        value=st.session_state.context_length,
    )

    # --------------------------------------------------------
    # System Prompt
    # --------------------------------------------------------

    st.subheader("🧠 System Prompt")

    st.session_state.system_prompt = st.text_area(
        "Instructions for AI",
        value=st.session_state.system_prompt,
        height=120,
    )

    # --------------------------------------------------------
    # Chat Controls
    # --------------------------------------------------------

    st.divider()

    st.subheader("💬 Chat Controls")

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        clear_chat()
        st.rerun()

    # --------------------------------------------------------
    # Export
    # --------------------------------------------------------

    if st.session_state.messages:

        st.download_button(
            label="📄 Download TXT",
            data=export_chat_txt(),
            file_name="ollama_chat.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.download_button(
            label="📦 Download JSON",
            data=export_chat_json(),
            file_name="ollama_chat.json",
            mime="application/json",
            use_container_width=True,
        )


# ============================================================
# Main Header
# ============================================================

st.markdown(
    '<div class="main-title">🤖 Ollama Local Chatbot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Private AI chat powered by models running locally on Ollama."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# Dashboard Information
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Connection",
        "Online" if not connection_error else "Offline",
    )

with col2:

    st.metric(
        "Installed Models",
        len(available_models),
    )

with col3:

    message_count = len(
        st.session_state.messages
    )

    st.metric(
        "Messages",
        message_count,
    )

with col4:

    current_model = (
        st.session_state.selected_model
        or "None"
    )

    st.metric(
        "Current Model",
        current_model,
    )


st.divider()


# ============================================================
# No Ollama / No Models
# ============================================================

if connection_error:

    st.warning(
        "Ollama is not reachable."
    )

    st.markdown(
        """
        ### Start Ollama

        Make sure Ollama is running on your computer.

        Your application is configured for:

        """
    )

    st.code(
        OLLAMA_HOST,
        language="text",
    )

    st.stop()


if not available_models:

    st.info(
        "No Ollama models are installed locally."
    )

    st.markdown(
        """
        ### Install a model

        For example:
        """
    )

    st.code(
        "ollama pull gemma3:4b",
        language="powershell",
    )

    st.code(
        "ollama pull qwen2.5:3b",
        language="powershell",
    )

    st.caption(
        "After installing a model, click "
        "'Refresh Models' in the sidebar."
    )

    st.stop()


# ============================================================
# Selected Model Information
# ============================================================

selected_info = next(
    (
        model
        for model in available_models
        if model["name"]
        == st.session_state.selected_model
    ),
    None,
)

if selected_info:

    st.caption(
        f"Using local model: "
        f"**{selected_info['name']}**"
    )


# ============================================================
# Display Chat History
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# Regenerate Last Response
# ============================================================

if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"]
    == "assistant"
):

    regenerate_col1, regenerate_col2 = st.columns(
        [1, 5]
    )

    with regenerate_col1:

        if st.button(
            "🔄 Regenerate",
            use_container_width=True,
        ):

            # Remove last assistant message
            st.session_state.messages.pop()

            st.rerun()


# ============================================================
# Chat Input
# ============================================================

prompt = st.chat_input(
    "Ask your local AI anything..."
)


# ============================================================
# Handle User Prompt
# ============================================================

if prompt:

    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)

    # --------------------------------------------------------
    # Generate AI response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        response, eval_count, duration, error = (
            generate_response(
                st.session_state.selected_model
            )
        )

    # --------------------------------------------------------
    # Error
    # --------------------------------------------------------

    if error:

        # Remove failed user message
        if (
            st.session_state.messages
            and st.session_state.messages[-1]["role"]
            == "user"
        ):

            st.session_state.messages.pop()

        st.error(
            "❌ Ollama returned an error."
        )

        st.code(
            error,
            language="text",
        )

        st.info(
            f"Selected local model: "
            f"{st.session_state.selected_model}"
        )

    else:

        # ----------------------------------------------------
        # Response Statistics
        # ----------------------------------------------------

        stats = []

        if eval_count:
            stats.append(
                f"Tokens: {eval_count}"
            )

        if duration:
            stats.append(
                f"Generation time: {duration:.2f}s"
            )

        if stats:

            st.caption(
                " • ".join(stats)
            )