import streamlit as st
import requests




st.image("data/images/DK.jpg", width=200)

st.markdown("#### Ask a question to Djwal Khul")


with open("data/system_prompt.txt", 'r') as f:
    prompt_template = f.read()


url = "https://aidk-image-ysui3kex7a-ew.a.run.app/response"

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": prompt_template}]

# Display chat messages from history on app rerun
for i, message in enumerate(st.session_state.messages):
    if i != 0:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar="🧘🏻‍♂️"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar="data/images/DK.jpg"):
                st.markdown(message["content"])

# Accept user input
question = st.chat_input("What is your question?")
if question:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    # Display user message in chat message container
    with st.chat_message("user", avatar="🧘🏻‍♂️"):
        st.markdown(question)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="data/images/DK.jpg"):

        def fetch_response(url, question, messages):
            payload = {
                "question": question,
                "messages": messages  # Send entire chat history
            }

            response = requests.post(url, json=payload, stream=True)

            def stream():
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk.decode("utf-8")  # Decode and stream response

            return stream

        ai_response = st.write_stream(fetch_response(url, question, st.session_state.messages))

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
