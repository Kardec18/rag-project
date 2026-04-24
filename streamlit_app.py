import streamlit as st
import requests

API_URL = "http://rag-api:8000/ask"

st.title("🤖 Chat RAG")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá, eu sou IA de demonstração! 👋\n\nPosso te ajudar a consultar documentos e responder perguntas."
        }
    ]

def build_history(messages, limit=5):
    recent = messages[-limit:]
    return "\n".join(
        [f'{m["role"]}: {m["content"]}' for m in recent]
    )

# render histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input
if prompt := st.chat_input("Pergunte algo..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    history = build_history(st.session_state.messages)

    payload = {
        "question": prompt,
        "history": history
    }

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                res = requests.post(API_URL, json=payload)
                answer = res.json().get("answer", "Erro")
            except Exception as e:
                answer = f"Erro: {e}"

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })