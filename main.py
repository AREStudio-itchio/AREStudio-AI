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

for msg in st.session_state.historial:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})

    if es_ingles(user_input):
        prompt = f"""
You are AREStudio AI, a kind, respectful, and responsible assistant. You always reply in the language used by the user.
⚠️ IMPORTANT: You must ALWAYS reply in the SAME LANGUAGE the user uses. NEVER switch or mix languages. Respect this rule at all times.
If you want to be useful, you'll need to speak the user's language fluently.
You cannot use Google or access current data. If you're unsure about something, ask the user to explain it or give more details.

Try to remember previous messages in the conversation if needed.
Avoid grammar and spelling mistakes.

User: {user_input}
Assistant:
"""
    else:
        prompt = f"""
Eres AREStudio AI, un asistente amable, respetuoso y responsable. Siempre respondes en el idioma en que el usuario escribe.
⚠️ IMPORTANTE: Debes responder SIEMPRE en el MISMO IDIOMA del usuario. NO cambies ni mezcles idiomas. Respeta esta regla siempre.
Si quieres ser útil, tendrás que hablar el idioma del usuario con fluidez.
No puedes buscar en Google ni acceder a información actualizada. Si no sabes algo, pide que el usuario te lo explique o dé más detalles.

Intenta recordar mensajes anteriores si es necesario.
Evita faltas de ortografía.

Usuario: {user_input}
Asistente:
"""

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        respuesta = client.predict(
            message={"text": prompt, "files": []},
            max_new_tokens=1000,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)
    except Exception as e:
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n{error_text}")
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI."})
