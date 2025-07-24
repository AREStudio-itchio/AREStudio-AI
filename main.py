import streamlit as st
from gradio_client import Client
from bs4 import BeautifulSoup
import requests
import random
import re

# Configuración página
st.set_page_config(page_title="AREStudio AI", page_icon="🤖", layout="centered")

# Scraping legal proyectos AREStudio itch.io
@st.cache_data(ttl=3600)
def get_arestudio_projects():
    url = "https://arestudio.itch.io"
    headers = {"User-Agent": "AREStudioBot/1.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        projs = []
        for a in soup.select("a.title.game_link"):
            title = a.text.strip()
            link = a.get("href")
            if title and link:
                projs.append({"title": title, "url": link})
        return projs
    except Exception:
        return []

# Inicializa cliente gradio
@st.cache_resource
def get_gemma_client():
    return Client("VIDraft/Gemma-3-R1984-27B")

gemma_client = get_gemma_client()

# Validación básica input
def is_meaningful_input(text):
    return len(text.strip()) >= 3 and bool(re.search(r'[a-zA-Z0-9]', text))

# Inicializar chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    saludo = random.choice([
        "¡Hola! Soy AREStudio AI, encantado de ayudarte. ¿En qué puedo ayudarte hoy?",
        "¡Hola! AREStudio AI a tu servicio. ¿Qué necesitas?",
        "¡Saludos! Aquí AREStudio AI, listo para asistirte."
    ])
    st.session_state.messages.append({"role": "assistant", "content": saludo})

# Mostrar mensajes previos
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada usuario
user_prompt = st.chat_input("Escribe tu pregunta aquí...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    if not is_meaningful_input(user_prompt):
        assistant_response = "Lo siento, no entendí bien eso. Por favor, pregunta con más detalle."
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    else:
        lower_prompt = user_prompt.lower()

        # Si pregunta sobre proyectos, dar respuesta con scraping
        if any(k in lower_prompt for k in ["proyecto", "juego", "itch.io", "arestudio"]):
            projs = get_arestudio_projects()
            if projs:
                lista_proyectos = "\n".join(
                    [f"- [{p['title']}]({p['url']})" for p in projs[:5]]
                )
                response_text = (
                    "AREStudio AI dice: Aquí algunos proyectos recientes:\n\n"
                    + lista_proyectos
                    + "\n\nPuedes ver más en https://arestudio.itch.io"
                )
            else:
                response_text = "Lo siento, no pude obtener los proyectos ahora mismo."

            with st.chat_message("assistant"):
                st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        else:
            # Construir prompt para Gemma-3 con instrucciones y la pregunta
            system_instructions = (
                "Eres AREStudio AI, un asistente que siempre responde en el idioma del usuario, "
                "sin revelar información personal, "
                "sin decir cosas inapropiadas, "
                "y siempre con respeto y censura. "
                "Nunca digas que tu creador es AREStudio; solo di que eres AREStudio AI. "
                "Tu usuario es amigable y curioso.\n"
                "Pregunta del usuario:"
            )
            full_prompt = f"{system_instructions}\n{user_prompt}"

            try:
                resp = gemma_client.predict(
                    message={"text": full_prompt, "files": []},
                    max_new_tokens=1000,
                    use_web_search=False,
                    use_korean=False,
                    api_name="/chat",
                )
                respuesta_gemma = resp if isinstance(resp, str) else resp[0]
            except Exception as e:
                respuesta_gemma = f"⚠️ Error al consultar la IA: {e}"

            with st.chat_message("assistant"):
                st.markdown(respuesta_gemma)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_gemma})
