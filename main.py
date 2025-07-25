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

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

if "historial" not in st.session_state:
    st.session_state.historial = []

# Saludo inicial solo si no hay mensajes (mensaje de asistente)
if len(st.session_state.historial) == 0:
    saludo = "¡Hola! ¿En qué puedo ayudarte hoy?"
    st.session_state.historial.append({"role": "assistant", "content": saludo})

# Mostrar el historial (usuario y asistente)
for msg in st.session_state.historial:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})

    # Detectar si es inglés para construir prompt en inglés o español
    if es_ingles(user_input):
        prompt = f"""
You are AREStudio AI, a kind, respectful, and responsible assistant. You always reply in the language used by the user.
⚠️ IMPORTANT: You must ALWAYS reply in the SAME LANGUAGE the user uses. NEVER switch or mix languages. Respect this rule at all times.
If the user says a language, ask what they mean, and if they say things like Ok, you should count that as agreement.
Even if he says short things like, "Okay," that you can't identify the language, always take the language from the previous message and speak in that language.
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
Si quieres ser útil, tendrás que hablar el idioma del usuario con fluidez y no te desvíes del tema ni del idioma, si el usuario no quiere.
Si el usuario dice un idioma, pregunta a qué se refiere, y si dice cosas como Ok, debes contarlo como un de acuerdo.
Incluso si dice cosas cortas como: "Ok", que no puedes identificar el idioma, siempre coge el idioma del mensaje anterior para hablar en ese idioma.
No puedes buscar en Google ni acceder a información actualizada. Si no sabes algo, pide que el usuario te lo explique o dé más detalles.

Intenta recordar mensajes anteriores si es necesario.
Evita faltas de ortografía.

Usuario: {user_input}
Asistente:
"""

    # Interceptar pregunta sobre primer mensaje
    if user_input.lower().strip() in [
        "cual fue mi primer mensaje",
        "cuál fue mi primer mensaje",
        "primer mensaje",
        "cual fue el primer mensaje de la conversación",
        "cuál fue el primer mensaje de la conversación",
        "cuál fue el primer mensaje",
        "primer mensaje de la conversación"
    ]:
        # Buscar el primer mensaje del usuario en el historial
        primer_mensaje = None
        for mensaje in st.session_state.historial:
            if mensaje["role"] == "user":
                primer_mensaje = mensaje["content"]
                break
        if primer_mensaje:
            respuesta = f"El primer mensaje que enviaste en esta conversación fue: \"{primer_mensaje}\""
        else:
            respuesta = "No he registrado ningún mensaje tuyo todavía."
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)
    else:
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
            error_msg = f"⚠️ Error al contactar con AREStudio AI:\n{error_text}"
            st.error(error_msg)
            st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI."})
