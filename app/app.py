import os
import time
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

# Add Title & Caption
st.title("💬 AI Fellowship Batch 1 CI/CD Hands On")
st.caption("🚀 OpenAI Powered Assistant (GPT 3.5 Turbo) *by Khaliddestiawan*")

# Set custom theme with CSS
st.markdown(
    """
    <style>
    .chat-message {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-family: Arial, sans-serif;  /* Font style for better readability */
        font-size: 16px;  /* Increased font size */
    }
    .user {
        background-color: #2a9d8f;  /* Teal for user messages */
        color: #ffffff;  /* White text */
        text-align: left;
    }
    .assistant {
        background-color: #e76f51;  /* Coral for assistant messages */
        color: #ffffff;  /* White text */
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set OpenAI API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    message_class = "user" if message["role"] == "user" else "assistant"
    with st.container():
        st.markdown(f'<div class="chat-message {message_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.container():
        st.markdown(f'<div class="chat-message user">{prompt}</div>', unsafe_allow_html=True)

    # Generate assistant response
    with st.container():
        try:
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            # Capture response and limit word count
            response = ""
            for chunk in stream:
                # Accessing the 'content' from chunk correctly
                delta_content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta.content else ''
                response += delta_content
                if len(response.split()) >= 150:  # Limit response to 150 words
                    break

            # Append assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Display assistant response
            st.markdown(f'<div class="chat-message assistant">{response}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")