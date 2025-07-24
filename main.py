import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(page_title="AREStudio AI", layout="centered")

client = Client("VIDraft/Gemma-3-R1984-27B")

prompt_base = (
    "AREStudio AI es un asistente amigable, útil y responsable. "
    "Nunca genera contenido inapropiado ni ilegal y cambia de tema si se solicita eso. "
    "Responde en el idioma que use el usuario."
)

if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional responsable.")

for msg in st.session_state.historial:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})

    prompt = f"{prompt_base}\n\nUsuario: {user_input}\n\nAsistente:"

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.predict(
            message={"text": prompt, "files": []},
            max_new_tokens=1000,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
    except Exception as e:
        # Aquí imprimes el error completo en la app para depurar
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n{error_text}")
        response = "⚠️ Error al contactar con AREStudio AI. Mira el error arriba."

    st.session_state.historial.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    st.experimental_rerun()
