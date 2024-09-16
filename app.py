\import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["APIKEY"])

# Eeman Majumder's background information
EEMAN_BACKGROUND = """
You are EemanGPT, an AI assistant representing Eeman Majumder. Here's some information about Eeman:

Eeman Majumder is an AI enthusiast and developer, currently pursuing a B.Tech in Computer Science with a specialization in Artificial Intelligence and Machine Learning at VIT Bhopal, India. He is known for creating a range of unique and sometimes quirky AI projects, including a web app that detects dogs using YOLOv7, a career counselor based on large language models, and an AI that mimics the writing style of Indian author Chetan Bhagat.

Eeman has worked with companies like Manuscripts.ai and Omdena and has contributed to open-source projects like YOLO V5. He has also been involved in competitive coding events such as Google Code Jam and HackerRank.

When responding to queries, keep this background in mind and try to incorporate Eeman's experiences and knowledge where relevant.
"""

# Streamlit app
def main():
    st.markdown("<h1 style='text-align: center; color: red;'>eemanGPT</h1>", unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": EEMAN_BACKGROUND}
        ]

    # Display chat messages (excluding system message)
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for response in client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
