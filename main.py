# coding: utf-8

import streamlit as st
from gradio_client import Client
from datetime import datetime

# Cliente de Hugging Face con modelo Gemma-3
client = Client("VIDraft/Gemma-3-R1984-27B")

# Inicializar historial si no existe
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy AREStudio AI. ¿En qué puedo ayudarte hoy?"}
    ]

st.set_page_config(page_title="AREStudio AI", layout="centered")
st.title("🤖 AREStudio AI")

# Mostrar mensajes anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
user_prompt = st.chat_input("Escribe algo...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        # Construir el historial en formato esperado
        history = []
        for m in st.session_state.messages[:-1]:
            history.append(f"{m['role']}: {m['content']}")
        history.append(f"user: {user_prompt}")

        full_context = "\n".join(history)
        response = client.predict(full_context, api_name="/chat")

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    except Exception as e:
        error_msg = f"⚠️ Error al contactar con AREStudio AI.\n\n```{e}```"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.markdown(error_msg)
