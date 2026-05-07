import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="RAG Policy Assistant", layout="wide")

st.title("📄 Policy RAG Assistant")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Options")

    user_email = st.text_input("Your Email")

    if st.button("🆕 New Chat"):
        st.session_state.messages = []

# Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
query = st.chat_input("Ask something about policy...")

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    # Call API
    with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
        response = requests.post(
            API_URL + "/stream",
            json={
                "query": query,
                "send_email": False,
                "user_email": user_email
            },
            stream=True
        )

        full_response = ""
        placeholder = st.empty()

        for chunk in response.iter_content(chunk_size=10):
            if chunk:
                text = chunk.decode("utf-8")
                full_response += text
                placeholder.markdown(full_response)

    answer = full_response

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    if "sources" in data and data["sources"]:
    with st.expander("📚 Sources"):
        for i, src in enumerate(data["sources"]):
            st.markdown(f"**Source {i+1}:**")
            st.write(src)
            st.divider()
    st.markdown(f"**{doc.metadata['source']} (Page {doc.metadata.get('page', '-')})**")

    # 👉 HITL: Ask user for email action
    if user_email:
        send = st.button("📧 Send this response to email")

        if send:
            email_response = requests.post(
                API_URL,
                json={
                    "query": query,
                    "send_email": True,
                    "user_email": user_email
                }
            )

            email_data = email_response.json()

            st.success(f"Email status: {email_data.get('email_status')}")
