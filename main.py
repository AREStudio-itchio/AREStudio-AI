import streamlit as st
from gradio_client import Client
import traceback

# Inyecta JS para scroll suave hacia el final, velocidad proporcional a la distancia
def scroll_to_bottom():
    scroll_script = """
    <script>
    const el = window.parent.document.querySelector('main div[role="main"]');
    if(el) {
        const distance = el.scrollHeight - el.scrollTop - el.clientHeight;
        // Ajustar duración proporcional (100ms mínimo, 1000ms máximo)
        let duration = Math.min(1000, Math.max(100, distance));
        el.style.scrollBehavior = "smooth";
        el.scrollTo(0, el.scrollHeight);
        setTimeout(() => { el.style.scrollBehavior = "auto"; }, duration);
    }
    </script>
    """
    st.components.v1.html(scroll_script, height=0, width=0)

st.set_page_config(page_title="AREStudio AI", layout="centered")

client = Client("VIDraft/Gemma-3-R1984-27B")

prompt_template = """
Eres AREStudio AI, un asistente amable, respetuoso y empático. Respondes en el idioma que usa el usuario, con alegría y educación.
No tienes acceso a datos personales, ni la hora, ni la fecha, ni puedes buscar en internet.
No generas contenido inapropiado ni dañino, y si te lo piden, cambias amablemente de tema.
Si el usuario te pide sintaxis o ejemplos de programación, responde con ejemplos completos y claros.
Si no estás seguro o crees que la información puede estar desactualizada, pide que te corrijan o actualicen.
El usuario: {user_input}
Asistente:
"""

if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

# Mostrar historial de chat
for mensaje in st.session_state.historial:
    role = mensaje["role"]
    content = mensaje["content"]
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})
    prompt = prompt_template.format(user_input=user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        respuesta = client.predict(
            message={"text": prompt, "files": []},
            max_new_tokens=1000,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

        scroll_to_bottom()

    except Exception:
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI. Por favor, inténtalo de nuevo más tarde."})
        with st.chat_message("assistant"):
            st.markdown("⚠️ Error al contactar con AREStudio AI. Por favor, inténtalo de nuevo más tarde.")
        scroll_to_bottom()
else:
    scroll_to_bottom()
