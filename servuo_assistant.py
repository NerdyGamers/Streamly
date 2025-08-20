import openai
import streamlit as st
import logging
from PIL import Image, ImageEnhance
import time
import base64
from openai import OpenAI, OpenAIError
from update_fetcher import load_game_updates

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
NUMBER_OF_MESSAGES_TO_DISPLAY = 20

# Retrieve and validate API key
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
    st.stop()

# Assign OpenAI API Key
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

# Streamlit Page Configuration
st.set_page_config(
    page_title="ServUO Assistant",
    page_icon="imgs/avatar_streamly.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://github.com/AdieLaine/Streamly",
        "Report a bug": "https://github.com/AdieLaine/Streamly",
        "About": """
            ## ServUO Assistant
            ### Powered using GPT-4o-mini

            **GitHub**: https://github.com/AdieLaine/

            The AI Assistant aims to provide the latest updates from ServUO and Ultima Online,
            generate code snippets for scripts,
            and answer questions about ServUO's latest features, issues, and more.
        """,
    },
)

# Streamlit Title
st.title("ServUO Assistant")


def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logging.error(f"Error converting image to base64: {str(e)}")
        return None


@st.cache_data(show_spinner=False)
def long_running_task(duration):
    """
    Simulates a long-running operation.

    Parameters:
    - duration: int, duration of the task in seconds

    Returns:
    - str: Completion message
    """
    time.sleep(duration)
    return "Long-running operation completed."


@st.cache_data(show_spinner=False)
def load_and_enhance_image(image_path, enhance=False):
    """
    Load and optionally enhance an image.

    Parameters:
    - image_path: str, path of the image
    - enhance: bool, whether to enhance the image or not

    Returns:
    - img: PIL.Image.Image, (enhanced) image
    """
    img = Image.open(image_path)
    if enhance:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.8)
    return img


def format_highlights(game_name, data):
    highlights = data.get("Highlights", {})
    if not highlights:
        return f"No highlights found for {game_name}."
    formatted = [f"Here are the latest highlights from {game_name}:"]
    for version, info in highlights.items():
        description = info.get("Description", "No description available.")
        documentation = info.get("Documentation", "No documentation available.")
        formatted.append(f"- **{version}**: {description}")
        formatted.append(f"  - **Documentation**: {documentation}")
    return "\n".join(formatted)


def initialize_conversation():
    """Initialize the conversation history with system and assistant messages."""
    assistant_message = "Hello! I am your ServUO assistant. How can I help you with ServUO or Ultima Online today?"

    conversation_history = [
        {
            "role": "system",
            "content": "You are Servly, a specialized AI assistant trained in ServUO and Ultima Online.",
        },
        {
            "role": "system",
            "content": "Servly is powered by the OpenAI GPT-4o-mini model, released on July 18, 2024.",
        },
        {
            "role": "system",
            "content": "You are trained up to ServUO Publish 57.4 and Ultima Online Publish 116.3.",
        },
        {
            "role": "system",
            "content": "Refer to conversation history to provide context to your response.",
        },
        {
            "role": "system",
            "content": "You were created by Madie Laine, an OpenAI Researcher.",
        },
        {
            "role": "system",
            "content": (
                "When providing code examples, generate ServUO scripts and avoid "
                "creating Streamlit applications."
            ),
        },
        {"role": "assistant", "content": assistant_message},
    ]
    return conversation_history


@st.cache_data(show_spinner=False)
def on_chat_submit(chat_input, latest_updates):
    """Handle chat input submissions and interact with the OpenAI API."""
    user_input = chat_input.strip().lower()

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = initialize_conversation()

    st.session_state.conversation_history.append(
        {"role": "user", "content": user_input}
    )

    try:
        assistant_reply = ""
        if "update" in user_input:
            if "servuo" in user_input:
                assistant_reply = format_highlights(
                    "ServUO", latest_updates.get("ServUO", {})
                )
            elif "ultima online" in user_input or "uo" in user_input:
                assistant_reply = format_highlights(
                    "Ultima Online", latest_updates.get("UltimaOnline", {})
                )
            else:
                servuo_msg = format_highlights(
                    "ServUO", latest_updates.get("ServUO", {})
                )
                uo_msg = format_highlights(
                    "Ultima Online", latest_updates.get("UltimaOnline", {})
                )
                assistant_reply = f"{servuo_msg}\n\n{uo_msg}"
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=st.session_state.conversation_history
            )
            assistant_reply = response.choices[0].message.content

        st.session_state.conversation_history.append(
            {"role": "assistant", "content": assistant_reply}
        )
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append(
            {"role": "assistant", "content": assistant_reply}
        )

    except OpenAIError as e:
        logging.error(f"Error occurred: {e}")
        st.error(f"OpenAI Error: {str(e)}")


def initialize_session_state():
    """Initialize session state variables."""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []


def display_game_updates(latest_updates):
    """Display the latest updates for ServUO and Ultima Online."""
    for game, data in latest_updates.items():
        with st.expander(f"{game} Updates", expanded=False):
            st.markdown(format_highlights(game, data))


def main():
    """Display updates and handle the chat interface."""
    initialize_session_state()

    if not st.session_state.history:
        initial_bot_message = (
            "Hello! How can I assist you with ServUO or Ultima Online today?"
        )
        st.session_state.history.append(
            {"role": "assistant", "content": initial_bot_message}
        )
        st.session_state.conversation_history = initialize_conversation()

    # Insert custom CSS for glowing effect
    st.markdown(
        """
        <style>
        .cover-glow {
            width: 100%;
            height: auto;
            padding: 3px;
            box-shadow:
                0 0 5px #330000,
                0 0 10px #660000,
                0 0 15px #990000,
                0 0 20px #CC0000,
                0 0 25px #FF0000,
                0 0 30px #FF3333,
                0 0 35px #FF6666;
            position: relative;
            z-index: -1;
            border-radius: 45px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load and display sidebar image
    img_path = "imgs/sidebar_streamly_avatar.png"
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("---")

    # Sidebar for Mode Selection
    mode = st.sidebar.radio(
        "Select Mode:",
        options=["Latest Updates", "Chat with ServUO Assistant"],
        index=1,
    )

    st.sidebar.markdown("---")

    # Display basic interactions
    show_basic_info = st.sidebar.checkbox("Show Basic Interactions", value=True)
    if show_basic_info:
        st.sidebar.markdown(
            """
        ### Basic Interactions
        - **Ask About ServUO**: Type your questions about ServUO's latest updates, features, or issues.
        - **Search for Scripts**: Use keywords like 'script example', 'syntax', or 'how-to' to get relevant code
          snippets.
        - **Navigate Updates**: Switch to 'Latest Updates' mode to browse the newest ServUO and Ultima Online updates
          in detail.
        """
        )

    # Display advanced interactions
    show_advanced_info = st.sidebar.checkbox("Show Advanced Interactions", value=False)
    if show_advanced_info:
        st.sidebar.markdown(
            """
        ### Advanced Interactions
        - **Generate a Script**: Use keywords like **generate script**, **create script** to get basic ServUO script
          code.
        - **Code Explanation**: Ask for **code explanation** to understand ServUO script logic.
        - **Project Analysis**: Use **analyze my shard** for insights and recommendations.
        - **Debug Assistance**: Use **debug this**, **fix this error** to troubleshoot issues.
        """
        )

    st.sidebar.markdown("---")

    # Load and display image with glowing effect
    img_path = "imgs/stsidebarimg.png"
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
        )

    if mode == "Chat with ServUO Assistant":
        chat_input = st.chat_input("Ask me about ServUO or Ultima Online:")
        if chat_input:
            latest_updates = load_game_updates()
            on_chat_submit(chat_input, latest_updates)

        # Display chat history
        for message in st.session_state.history[-NUMBER_OF_MESSAGES_TO_DISPLAY:]:
            role = message["role"]
            avatar_image = (
                "imgs/avatar_streamly.png"
                if role == "assistant"
                else "imgs/stuser.png" if role == "user" else None
            )
            with st.chat_message(role, avatar=avatar_image):
                st.write(message["content"])

    else:
        latest_updates = load_game_updates()
        display_game_updates(latest_updates)


if __name__ == "__main__":
    main()
