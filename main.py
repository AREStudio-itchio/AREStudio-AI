import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(
    page_title="AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png",
    layout="centered"
)

client = Client("VIDraft/Gemma-3-R1984-27B")

# Función para detectar inglés
def es_ingles(texto):
    palabras_ingles = ["hello", "hi", "what", "how", "where", "why", "who", "can", "do", "you", "are"]
    return any(palabra in texto.lower() for palabra in palabras_ingles)

# Inicializar historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Mostrar historial
for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Saludo inicial
if len(st.session_state.historial) == 0:
    saludo = "¡Hola! ¿En qué puedo ayudarte hoy?"
    st.session_state.historial.append({"role": "assistant", "content": saludo})
    with st.chat_message("assistant"):
        st.markdown(saludo)

# Entrada de usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construcción del historial como texto
    MAX_MENSAJES = 10
    historial_reciente = st.session_state.historial[-MAX_MENSAJES:]

    historial_str = ""
    for mensaje in historial_reciente:
        if mensaje["role"] == "user":
            historial_str += f"Usuario: {mensaje['content']}\n"
        else:
            historial_str += f"Asistente: {mensaje['content']}\n"

    # Elección de idioma base
    if es_ingles(user_input):
        system_prompt = """
You are AREStudio AI, a kind, respectful, and responsible assistant. You always reply in the same language the user uses.
⚠️ IMPORTANT: NEVER mix languages. Be consistent. Avoid grammar or spelling mistakes. If you don’t understand something, ask.
"""
    else:
        system_prompt = """
Eres AREStudio AI, un asistente amable, respetuoso y responsable. Siempre respondes en el mismo idioma del usuario.
⚠️ IMPORTANTE: NUNCA mezcles idiomas. Sé consistente. Evita faltas de ortografía. Si no entiendes algo, pregunta.
"""

    final_prompt = system_prompt.strip() + "\n\n" + historial_str + "Asistente:"

    try:
        # 🔥 Aquí usamos prompt directamente, no message
        respuesta = client.predict(
            prompt=final_prompt,
            max_new_tokens=1000,
            api_name="/chat"
        )
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

    except Exception as e:
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n{error_text}")
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI."})
