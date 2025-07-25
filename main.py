import streamlit as st
from gradio_client import Client

st.title("🤖 AREStudio AI")

client = Client("VIDraft/Gemma-3-R1984-27B")

if "historial" not in st.session_state:
    st.session_state.historial = []

if len(st.session_state.historial) == 0:
    saludo = "¡Hola! ¿En qué puedo ayudarte hoy?"
    st.session_state.historial.append({"role": "assistant", "content": saludo})

for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})

    # Construir el prompt que enviarás
    prompt = f"Usuario: {user_input}\nAsistente:"

    try:
        respuesta = client.predict(
            message={"text": prompt, "files": []},
            max_new_tokens=1000,
            api_name="/chat"
        )
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        st.chat_message("assistant").markdown(respuesta)
    except Exception:
        st.error("⚠️ Error al contactar con AREStudio AI.")
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI."})
