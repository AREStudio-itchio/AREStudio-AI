import streamlit as st
from gradio_client import Client
import time

# Inicializar idioma (solo interfaz)
idioma = st.sidebar.selectbox("🌐 Idioma / Language / Llengua", ("Español", "Català", "English"))

# Traducciones de la interfaz
título = {
    "Español": "AREStudio AI - Asistente conversacional",
    "Català": "AREStudio AI - Assistent conversacional",
    "English": "AREStudio AI - Conversational Assistant"
}

subtítulo = {
    "Español": "Hazme preguntas y hablaré contigo como un asistente inteligente.",
    "Català": "Fes-me preguntes i parlaré amb tu com un assistent intel·ligent.",
    "English": "Ask me anything and I’ll talk with you like a smart assistant."
}

# Mostrar UI
st.title(título[idioma])
st.caption(subtítulo[idioma])

# Cliente Gradio
client = Client("VIDraft/Gemma-3-R1984-27B")

# Inicializar historial en estado de sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
for msg in st.session_state.mensajes:
    with st.chat_message(msg["rol"]):
        st.markdown(msg["contenido"])

# Entrada del usuario
pregunta = st.chat_input("💬 Escribe aquí...")

if pregunta:
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        pensando = st.empty()
        pensando.markdown("⏳ Pensando...")
        try:
            respuesta = client.predict(pregunta, api_name="/chat")
        except Exception as e:
            respuesta = "⚠️ Ocurrió un error al contactar con el modelo."

        pensando.markdown(respuesta)
    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta})
