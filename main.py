import streamlit as st
from gradio_client import Client

st.set_page_config(page_title="AREStudio AI - Asistente Multilingüe", layout="centered")

# Inicializar sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "client" not in st.session_state:
    st.session_state.client = Client("https://openfreeai-gemma-3b-chat.hf.space/")

# UI: Idioma y título
st.markdown("### 🌐 Idioma / Language / Llengua")
st.text("es")  # Puedes conectar con un selector si quieres cambiar el idioma
st.title("AREStudio AI - Asistente Multilingüe")

# Prompt de bienvenida
if len(st.session_state.chat_history) == 0:
    st.session_state.chat_history.append({
        "role": "assistant",
        "text": "🧠 Hola. Soy tu asistente de AREStudio. Puedes preguntarme sobre nuestros proyectos, IA, programación, y mucho más."
    })

# Mostrar historial del chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Entrada del usuario
prompt = st.chat_input("Escribe aquí tu pregunta...")

# Si hay entrada, procesar
if prompt:
    st.session_state.chat_history.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = st.session_state.client.predict(
                    prompt, api_name="/chat"
                )
                st.session_state.chat_history.append({"role": "assistant", "text": response})
                st.markdown(response)
            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "text": "❌ Error al obtener respuesta de la IA."
                })
                st.error("Ocurrió un error.")

# Fin del código
