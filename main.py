import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(
    page_title="AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png",
    layout="centered"
)

client = Client("VIDraft/Gemma-3-R1984-27B")

st.title("🤖 AREStudio AI - Prueba mínima")

user_input = st.text_input("Escribe tu mensaje:")

if user_input:
    try:
        # Solo enviar el texto del usuario
        respuesta = client.predict(
            user_input,
            max_new_tokens=1000
        )
        st.markdown(f"**Respuesta:** {respuesta}")

    except Exception:
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n\n```\n{error_text}\n```")
