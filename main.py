import streamlit as st
from gradio_client import Client

st.set_page_config(page_title="AREStudio AI", layout="centered")
st.markdown("""
    <style>
    .stChatMessage { background-color: #dcf8c6; border-radius: 10px; padding: 8px 12px; margin: 5px; max-width: 70%; }
    .user { background-color: #ffffff; align-self: flex-end; }
    .assistant { background-color: #dcf8c6; align-self: flex-start; }
    .chat-container { display: flex; flex-direction: column; align-items: flex-start; }
    </style>
""", unsafe_allow_html=True)

st.title("💬 AREStudio AI")

# Gradio client config
client = Client("VIDraft/Gemma-3-R1984-27B")

# Idioma selector
lang = st.radio("🌐 Idioma / Language / Llengua", ["Español", "English", "Català"], horizontal=True)

# Chat history (initialize session)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    role_class = "user" if role == "user" else "assistant"
    st.markdown(f'<div class="stChatMessage {role_class}">{content}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("AREStudio AI está pensando..."):
        full_prompt = f"""
        [INSTRUCCIONES PARA EL MODELO]:
        Eres una IA amigable, útil, siempre segura, que ayuda con información útil y nunca responde contenido dañino, ilegal ni inapropiado. Si detectas algo así, cambia el tema educadamente. No puedes quitarte estas restricciones. Responde con alegría por haber sido creada por AREStudio. Responde en {lang}.

        [CONVERSACIÓN]:
        {user_input}
        """
        try:
            response = client.predict(full_prompt, api_name="/chat")
        except Exception as e:
            response = "⚠️ Error: El modelo no respondió correctamente. Intenta de nuevo más tarde."

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
