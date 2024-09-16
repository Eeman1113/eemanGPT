import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["APIKEY"])

# Streamlit app
def main():
    st.markdown("<h1 style='text-align: center; color: lavender;'>eemanGPT</h1>", unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
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
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                temperature=1,
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
