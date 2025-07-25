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

# Inicializar historial si no existe
if "historial" not in st.session_state:
    st.session_state.historial = []

# Mostrar el historial ya guardado
for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Añadir el mensaje del usuario y mostrarlo inmediatamente
    st.session_state.historial.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Comando para mostrar el primer mensaje del usuario
    if user_input.lower() in ["cual fue mi primer mensaje", "cuál fue mi primer mensaje"]:
        primer_mensaje = None
        for m in st.session_state.historial:
            if m["role"] == "user":
                primer_mensaje = m["content"]
                break
        if primer_mensaje:
            respuesta = f"Tu primer mensaje fue:\n\n> {primer_mensaje}"
        else:
            respuesta = "No tengo registrado ningún mensaje tuyo todavía."

        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

    else:
        # Construir el prompt según idioma
        if es_ingles(user_input):
            prompt = f"""
You are AREStudio AI, a kind, respectful, and responsible assistant. You always reply in the language used by the user.
⚠️ IMPORTANT: You must ALWAYS reply in the SAME LANGUAGE the user uses. NEVER switch or mix languages. Respect this rule at all times.
If you want to be helpful, you'll need to speak the user's language fluently and stay on topic and in the right language if the user doesn't want you to.
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

        try:
            with st.spinner("AREStudio AI está escribiendo..."):
                respuesta = client.predict(
                    message={"text": prompt, "files": []},
                    max_new_tokens=1000,
                    api_name="/chat"
                )
            st.session_state.historial.append({"role": "assistant", "content": respuesta})
            with st.chat_message("assistant"):
                st.markdown(respuesta)
        except Exception:
            error_text = traceback.format_exc()
            st.error(f"⚠️ Error al contactar con AREStudio AI:\n\n```\n{error_text}\n```")
