import streamlit as st
import requests
import os
import json
import uuid

# =========================
# CONFIG E DEFINIÇÕES
# =========================
API_URL = "http://rag-api:8000/ask"
HISTORY_DIR = "history"
os.makedirs(HISTORY_DIR, exist_ok=True)

# Forçamos o estado inicial da sidebar como expandido
st.set_page_config(page_title="IA", layout="wide", initial_sidebar_state="expanded")

DEFAULT_MESSAGE = {
    "role": "assistant",
    "content": "Olá, eu sou a IA! 👋\n\nPosso te ajudar a consultar documentos e responder perguntas."
}

# =========================
# CSS
# =========================
st.markdown("""
<style>
    /* 1. Esconder o botão de recolher e o controle de colapso da sidebar */
    [data-testid="stSidebarCollapseButton"], 
    [data-testid="collapsedControl"],
    button[kind="headerNoPadding"] {
        display: none !important;
    }

    /* 2. Travar largura da sidebar para não "dançar" */
    section[data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }
    
    /* 3. Centralização dos ícones nas colunas */
    [data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 4. Estilo dos botões da sidebar */
    .stButton button {
        border-radius: 8px !important;
        margin: 0px !important;
        padding: 2px 5px !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# STORAGE
# =========================
def save_history(data, session_id):
    with open(f"{HISTORY_DIR}/{session_id}.json", "w") as f:
        json.dump(data, f)

def load_history(session_id):
    try:
        path = f"{HISTORY_DIR}/{session_id}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except:
        return None
    return None

def get_conversations():
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    def sort_key(f):
        data = load_history(f.replace(".json", ""))
        if not data: return (True, 0)
        return (not data.get("pinned", False), -os.path.getmtime(f"{HISTORY_DIR}/{f}"))
    return sorted(files, key=sort_key)

# =========================
# SESSION INIT (NOVA CONVERSA NO REFRESH)
# =========================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat_data = {
        "title": "Nova conversa",
        "pinned": False,
        "messages": [DEFAULT_MESSAGE]
    }

# =========================
# SIDEBAR
# =========================
st.sidebar.title("💬 Conversas")

if st.sidebar.button("➕ Nova conversa", use_container_width=True):
    new_id = str(uuid.uuid4())
    st.session_state.session_id = new_id
    st.session_state.chat_data = {
        "title": "Nova conversa",
        "pinned": False,
        "messages": [DEFAULT_MESSAGE]
    }
    st.rerun()

search = st.sidebar.text_input("🔎 Buscar", label_visibility="collapsed", placeholder="Buscar conversa...")

convs = get_conversations()
for conv in convs:
    sid = conv.replace(".json", "")
    data = load_history(sid)
    if not data or (search and search.lower() not in data.get("title", "").lower()):
        continue

    c1, c2, c3 = st.sidebar.columns([6, 1.5, 1.5])
    
    with c1:
        label = ("📌 " if data.get("pinned") else "") + data.get("title", "Sem título")
        style = "primary" if sid == st.session_state.session_id else "secondary"
        if st.button(label, key=f"sel_{sid}", use_container_width=True, type=style):
            st.session_state.session_id = sid
            st.session_state.chat_data = data
            st.rerun()
    
    with c2:
        if st.button("📌", key=f"pin_{sid}"):
            data["pinned"] = not data.get("pinned", False)
            save_history(data, sid)
            st.rerun()
            
    with c3:
        if st.button("🗑️", key=f"del_{sid}"):
            if os.path.exists(f"{HISTORY_DIR}/{conv}"):
                os.remove(f"{HISTORY_DIR}/{conv}")
            if sid == st.session_state.session_id:
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.chat_data = {"title": "Nova conversa", "pinned": False, "messages": [DEFAULT_MESSAGE]}
            st.rerun()

# =========================
# UI PRINCIPAL
# =========================
st.title("🤖 IA")

for msg in st.session_state.chat_data["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# LÓGICA DE CHAT
# =========================
if prompt := st.chat_input("Pergunte algo..."):
    
    if st.session_state.chat_data["title"] == "Nova conversa":
        st.session_state.chat_data["title"] = prompt[:30] + ( '...' if len(prompt) > 30 else '')

    st.session_state.chat_data["messages"].append({"role": "user", "content": prompt})
    save_history(st.session_state.chat_data, st.session_state.session_id)

    with st.chat_message("user"):
        st.markdown(prompt)

    history_str = "\n".join([f'{m["role"].upper()}: {m["content"]}' for m in st.session_state.chat_data["messages"][-5:]])

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                res = requests.post(API_URL, json={"question": prompt, "history": history_str}, timeout=30)
                answer = res.json().get("answer", "Não consegui processar sua resposta.")
            except Exception as e:
                answer = f"Erro de conexão com a API: {e}"
            
            st.markdown(answer)

    st.session_state.chat_data["messages"].append({"role": "assistant", "content": answer})
    save_history(st.session_state.chat_data, st.session_state.session_id)
    st.rerun()