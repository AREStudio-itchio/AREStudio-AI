import streamlit as st
from gradio_client import Client

client = Client("VIDraft/Gemma-3-R1984-27B")

prompt_sistema = "AREStudio AI es un asistente que ayuda, es amable y no permite contenido inapropiado."

if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("AREStudio AI")

# Mostrar historial
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

entrada = st.chat_input("Escribe tu mensaje...")

if entrada:
    st.session_state.historial.append({"role":"user","content":entrada})

    prompt = prompt_sistema + "\n\nUsuario: " + entrada + "\n\nAsistente:"
    try:
        respuesta = client.predict(
            message={"text": prompt, "files": []},
            max_new_tokens=1000,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
        st.session_state.historial.append({"role":"assistant","content":respuesta})
    except Exception as e:
        st.session_state.historial.append({"role":"assistant","content":"⚠️ Error al contactar con AREStudio AI."})
