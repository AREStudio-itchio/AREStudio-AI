import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(
    page_title="🤖 AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png",
    layout="centered"
)

client = Client("VIDraft/Gemma-3-R1984-27B")

def es_ingles(texto):
    palabras_ingles = ["hello", "hi", "what", "how", "where", "why", "who", "can", "do", "you", "are"]
    return any(palabra in texto.lower() for palabra in palabras_ingles)

if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

# Mostrar historial previo
for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Mostrar mensaje del usuario inmediatamente
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.historial.append({"role": "user", "content": user_input})

    # Construir prompt según idioma
    if es_ingles(user_input):
        prompt = f"""
You are AREStudio AI, a kind, respectful, and responsible assistant. Always reply in the user's language.
User: {user_input}
Assistant:
"""
    else:
        prompt = f"""
Eres AREStudio AI, un asistente amable, respetuoso y responsable. Siempre respondes en el idioma del usuario.
Usuario: {user_input}
Asistente:
"""

    with st.spinner("AREStudio AI está escribiendo..."):
        try:
            respuesta = client.predict(
                message={"text": prompt, "files": []},
                max_new_tokens=1000,
                api_name="/chat"
            )
            with st.chat_message("assistant"):
                st.markdown(respuesta)
            st.session_state.historial.append({"role": "assistant", "content": respuesta})
        except Exception:
            error_text = traceback.format_exc()
            st.error(f"⚠️ Error al contactar con AREStudio AI:\n\n```\n{error_text}\n```")
