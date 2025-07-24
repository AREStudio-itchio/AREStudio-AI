# -*- coding: utf-8 -*-
import streamlit as st
from gradio_client import Client
import random

st.set_page_config(page_title="AREStudio AI", layout="centered")
st.title("🤖 AREStudio AI - Chatbot conversacional")

# Iniciar cliente con el modelo Gemma-3
try:
    client = Client("OpenFreeAI/Gemma-3-R1984-27B-Chatbot")
    model_ready = True
except Exception as e:
    model_ready = False
    error_msg = str(e)

# Inicializar sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar historial
for mensaje in st.session_state.chat_history:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada del usuario
if model_ready:
    prompt = st.chat_input("Escribe tu mensaje...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Llamar al modelo Gemma
        try:
            output = client.predict(
                prompt,
                "Are you ready?",
                1,
                api_name="/chat"
            )
        except Exception as e:
            output = "⚠️ Error al procesar la respuesta de la IA."

        st.session_state.chat_history.append({"role": "assistant", "content": output})
        with st.chat_message("assistant"):
            st.markdown(output)
else:
    st.error("⚠️ Error al contactar con AREStudio AI.")
    if st.toggle("Mostrar detalles técnicos"):
        st.code(error_msg, language="bash")
