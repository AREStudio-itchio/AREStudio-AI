import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(
    page_title="AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png",
    layout="centered"
)

client = Client("VIDraft/Gemma-3-R1984-27B")

def es_ingles(texto):
    palabras_ingles = ["hello", "hi", "what", "how", "where", "why", "who", "can", "do", "you", "are"]
    return any(palabra in texto.lower() for palabra in palabras_ingles)

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

if "historial" not in st.session_state:
    st.session_state.historial = []

# Saludo inicial si no hay mensajes
if len(st.session_state.historial) == 0:
    saludo = "¡Hola! ¿En qué puedo ayudarte hoy?"
    st.session_state.historial.append({"role": "assistant", "content": saludo})

# Mostrar el historial de mensajes
for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})

    # Construir historial como texto plano
    MAX_MENSAJES = 10
    historial_reciente = st.session_state.historial[-MAX_MENSAJES:]

    historial_str = ""
    for mensaje in historial_reciente:
        if mensaje["role"] == "user":
            historial_str += f"Usuario: {mensaje['content']}\n"
        else:
            historial_str += f"Asistente: {mensaje['content']}\n"

    # Definir prompt base según idioma
    if es_ingles(user_input):
        system_prompt = (
            "You are AREStudio AI, a kind, respectful, and responsible assistant. "
            "Always respond in the same language the user uses.\n\n"
        )
    else:
        system_prompt = (
            "Eres AREStudio AI, un asistente amable, respetuoso y responsable. "
            "Siempre responde en el mismo idioma del usuario.\n\n"
        )

    prompt_final = system_prompt + historial_str + "Asistente:"

    try:
        # Enviar solo el texto plano, sin JSON
        respuesta = client.predict(
            prompt_final,
            max_new_tokens=1000,
            api_name="/chat"
        )

        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

    except Exception:
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n\n```\n{error_text}\n```")
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI."})
