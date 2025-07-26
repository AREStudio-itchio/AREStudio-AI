import streamlit as st
from gradio_client import Client
import traceback

# Configuración de página
st.set_page_config(
    page_title="AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png"
)

# Inicializar cliente Gradio
client = Client("VIDraft/Gemma-3-R1984-27B")

# Estado inicial de la sesión
if "user_messages" not in st.session_state:
    st.session_state.user_messages = []
if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []
if "last_language" not in st.session_state:
    st.session_state.last_language = "en"

# Función para detectar idioma
def detectar_idioma(texto):
    texto = texto.lower()
    if any(palabra in texto for palabra in ["qué", "cómo", "gracias", "hola"]):
        return "es"
    elif any(palabra in texto for palabra in ["bonjour", "merci", "comment", "salut"]):
        return "fr"
    elif any(palabra in texto for palabra in ["hello", "thanks", "please", "what", "how"]):
        return "en"
    return "en"

# Función para construir el prompt completo
def construir_prompt(usuario, asistente, idioma):
    instrucciones = {
        "es": (
            "Actúa como un asistente AI llamado AREStudio AI. "
            "Eres respetuoso, claro, amable, y útil. No inventes información. "
            "Responde siempre en español."
        ),
        "en": (
            "Act as an AI assistant named AREStudio AI. "
            "You are respectful, clear, kind, and helpful. Do not make up information. "
            "Always reply in English."
        ),
        "fr": (
            "Agis comme un assistant IA nommé AREStudio AI. "
            "Tu es respectueux, clair, aimable et utile. Ne pas inventer d'informations. "
            "Réponds toujours en français."
        )
    }

    prompt = f"{instrucciones[idioma]}\n\n"
    for u, a in zip(usuario, asistente):
        prompt += f"Usuario:\n{u}\n\nAsistente:\n{a}\n\n"

    # Si hay un mensaje pendiente sin respuesta
    if len(usuario) > len(asistente):
        prompt += f"Usuario:\n{usuario[-1]}\n\nAsistente:\n"

    return prompt

# UI
st.title("🤖 AREStudio AI")
st.markdown(
    "Tu asistente creado por [AREStudio](https://arestudio.itch.io) — amable, respetuoso, responsable y ahora con favicon 🎨"
)

# Mostrar historial
for user_msg, assistant_msg in zip(st.session_state.user_messages, st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(assistant_msg)

# Si el último mensaje no tiene respuesta aún
if len(st.session_state.user_messages) > len(st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(st.session_state.user_messages[-1])

# Entrada de usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.user_messages.append(user_input)
    idioma = detectar_idioma(user_input)
    st.session_state.last_language = idioma

    # Construcción del prompt
    prompt = construir_prompt(
        st.session_state.user_messages,
        st.session_state.assistant_responses,
        idioma
    )

    try:
        # Predicción del modelo
        respuesta = client.predict(
            prompt,
            max_new_tokens=1000,
            api_name="/chat"
        )

        respuesta_limpia = respuesta.strip()
        st.session_state.assistant_responses.append(respuesta_limpia)
        with st.chat_message("assistant"):
            st.markdown(respuesta_limpia)

    except Exception as e:
        tb = traceback.format_exc()
        error_msg = (
            f"⚠️ **Error al contactar con AREStudio AI:**\n\n"
            f"**Tipo:** `{type(e).__name__}`\n"
            f"**Mensaje:** `{e}`\n\n"
            f"**Traceback:**\n```python\n{tb}```"
        )
        st.session_state.assistant_responses.append(error_msg)
        with st.chat_message("assistant"):
            st.error(error_msg)
