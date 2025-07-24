import streamlit as st
from gradio_client import Client
import traceback
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AREStudio AI", layout="centered")

client = Client("VIDraft/Gemma-3-R1984-27B")

prompt_base_template = """
Eres AREStudio AI, un asistente amigable y responsable. Siempre respondes en el idioma en que el usuario escribe. No generas contenido inapropiado ni dañino y cambias de tema si te piden eso. Responde con alegría y educación.
Usuario: {user_input}
Asistente:
"""

def detectar_idioma(texto):
    texto = texto.lower()
    if any(palabra in texto for palabra in ["hola", "qué", "cómo", "dónde", "por qué"]):
        return "Español"
    elif any(palabra in texto for palabra in ["hello", "how", "what", "where", "why"]):
        return "English"
    elif any(palabra in texto for palabra in ["hola", "com va", "què", "per què"]):
        return "Català"
    else:
        return "Español"  # Por defecto español

def scrape_proyectos():
    try:
        url = "https://arestudio.itch.io"
        r = requests.get(url)
        r.raise_for_status()
        sopa = BeautifulSoup(r.text, "html.parser")
        titulos = sopa.select("div.game_title")
        proyectos = [t.get_text(strip=True) for t in titulos]
        if proyectos:
            return proyectos
        else:
            return ["Actualmente no hay proyectos disponibles."]
    except Exception as e:
        return [f"No se pudieron obtener los proyectos: {e}"]

if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional responsable.")

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

    idioma = detectar_idioma(user_input)
    
    # Detectar si el usuario pregunta por proyectos
    keywords_proyectos = ["proyecto", "proyectos", "juegos", "game", "games", "itch.io"]
    if any(palabra in user_input.lower() for palabra in keywords_proyectos):
        proyectos = scrape_proyectos()
        respuesta = "Aquí tienes algunos proyectos disponibles en AREStudio:\n\n"
        for p in proyectos:
            respuesta += f"- {p}\n"
        respuesta = respuesta.strip()
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)
    else:
        prompt = prompt_base_template.format(user_input=user_input)
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
