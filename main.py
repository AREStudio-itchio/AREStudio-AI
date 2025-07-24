# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from gradio_client import Client
import json

st.set_page_config(page_title="AREStudio AI", layout="centered")
st.title("🤖 AREStudio AI")
st.write("Tu asistente conversacional responsable.")
st.markdown("---")

def get_projects():
    try:
        url = "https://arestudio.itch.io"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            raise Exception(f"Estado: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        projects = [p.text.strip() for p in soup.select("div.game_cell_data a.title")]
        return projects if projects else ["(Sin resultados o estructura diferente)"]
    except Exception as e:
        st.error(f"⚠️ Error al contactar con AREStudio AI.\n\n`{e}`")
        return []

# Mostramos proyectos
st.subheader("🗂️ Proyectos de AREStudio:")
projects = get_projects()
for proj in projects:
    st.markdown(f"- {proj}")

st.markdown("---")

# Chat
client = Client("OpenFreeAI/Gemma-3-R1984-27B-Chatbot")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "Eres un asistente útil creado por AREStudio. Responde con claridad y amabilidad, y si te preguntan por AREStudio, responde que fue quien te creó."},
        {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy? 😊"}
    ]

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

user_input = st.chat_input("Escribe tu mensaje...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        messages = [(m["role"], m["content"]) for m in st.session_state.chat_history]
        response = client.predict(messages, api_name="/chat")
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    except Exception as e:
        st.session_state.chat_history.append({"role": "assistant", "content": f"⚠️ Error interno: `{e}`"})
        st.error(f"⚠️ Error al contactar con el modelo de IA.\n\n`{e}`")
