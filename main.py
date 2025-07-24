import streamlit as st
from gradio_client import Client
from bs4 import BeautifulSoup
import requests
import random
import re

# Config UI
st.set_page_config(page_title="AREStudio AI", page_icon="🤖", layout="centered")

# Scraping legal
@st.cache_data(ttl=3600)
def get_arestudio_projects():
    resp = requests.get("https://arestudio.itch.io", headers={"User-Agent":"AREStudioBot/1.0"}, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    projs = []
    for a in soup.select("a.title.game_link"):
        title = a.text.strip()
        link = a.get("href")
        if title and link:
            projs.append({"title": title, "url": link})
    return projs

# Cliente Gradio con espacio correcto
@st.cache_resource
def get_gemma_client():
    return Client("VIDraft/Gemma-3-R1984-27B")  # Sin sufijos adicionales

gemma_client = get_gemma_client()

def is_meaningful_input(txt):
    return len(txt.strip()) >= 3 and bool(re.search(r"[A-Za-z0-9]", txt))

if "messages" not in st.session_state:
    st.session_state.messages = []
    saludo = random.choice([
        "¡Hola! Soy AREStudio AI, encantada de ayudarte. ¿Qué quieres saber?",
        "¡Hola! Aquí AREStudio AI, lista para asistirte. ¿En qué puedo ayudar?"
    ])
    st.session_state.messages.append({"role":"assistant","content":saludo})

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Escribe tu pregunta aquí...")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not is_meaningful_input(prompt):
        resp = "Lo siento, no entendí bien eso. ¿Puedes expresarlo de otra forma?"
    elif any(k in prompt.lower() for k in ["proyecto","juego","itch.io","arestudio"]):
        projs = get_arestudio_projects()
        if projs:
            lista = "\n".join([f"- [{p['title']}]({p['url']})" for p in projs[:5]])
            resp = f"Aquí tienes algunos proyectos destacados de AREStudio:\n\n{lista}\n\nPuedes ver más en https://arestudio.itch.io"
        else:
            resp = "Lo siento, no pude obtener los proyectos en este momento."
    else:
        system = (
            "Eres AREStudio AI, un asistente que siempre responde en el idioma del usuario, "
            "con respeto, sin revelar información privada y manteniendo censura cuando sea necesario. "
            "Nunca debes decir que tu creador es AREstudio; solo menciona que eres AREStudio AI.\n"
            "Pregunta del usuario:"
        )
        full = f"{system}\n{prompt}"
        try:
            out = gemma_client.predict(
                message={"text":full,"files":[]},
                max_new_tokens=1000,
                use_web_search=False,
                use_korean=False,
                api_name="/chat"
            )
            resp = out if isinstance(out, str) else out[0]
        except Exception as e:
            resp = f"⚠️ Error al consultar la IA: {e}"

    st.session_state.messages.append({"role":"assistant","content":resp})
    with st.chat_message("assistant"):
        st.markdown(resp)
