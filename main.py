import streamlit as st
from gradio_client import Client

st.set_page_config(page_title="AREStudio AI", layout="centered")
st.markdown("""
    <style>
    .chat-bubble {
        border-radius: 12px;
        padding: 10px 15px;
        margin: 8px 0;
        max-width: 80%;
        line-height: 1.5;
        display: inline-block;
    }
    .user {
        background-color: #e1ffc7;
        color: #000;
        align-self: flex-end;
        margin-left: auto;
    }
    .assistant {
        background-color: #fff;
        color: #000;
        border: 1px solid #ddd;
        align-self: flex-start;
        margin-right: auto;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    """, unsafe_allow_html=True)

st.title("💬 AREStudio AI - Estilo WhatsApp")

# Cliente Gradio
client = Client("VIDraft/Gemma-3-R1984-27B")

# Selector de idioma
lang = st.radio("🌐 Idioma / Language / Llengua", ["Español", "English", "Català"], horizontal=True)

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    bubble_class = "user" if role == "user" else "assistant"
    st.markdown(f'<div class="chat-container"><div class="chat-bubble {bubble_class}">{content}</div></div>', unsafe_allow_html=True)

# Entrada del usuario
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
        except Exception:
            response = "⚠️ Error: El modelo no respondió correctamente. Intenta de nuevo más tarde."

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
