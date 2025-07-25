import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(
    page_title="AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png",
    layout="centered"
)

client = Client("VIDraft/Gemma-3-R1984-27B")

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

if "historial" not in st.session_state:
    st.session_state.historial = []

if len(st.session_state.historial) == 0:
    st.session_state.historial.append({"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy?"})

for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})

    try:
        respuesta = client.predict(
            message={"text": user_input, "files": []},
            max_new_tokens=1000,
            api_name="/chat"
        )
        st.session_state.historial.append({"role": "assistant", "content": respuesta})

        with st.chat_message("assistant"):
            st.markdown(respuesta)

    except Exception:
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n\n```\n{error_text}\n```")
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI."})
