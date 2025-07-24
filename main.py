import streamlit as st
from gradio_client import Client
import traceback

# Función para insertar código JS que hace scroll suave hacia el final del contenedor chat
def scroll_to_bottom(smoothness=500):
    # smoothness es la duración en ms del scroll, la puedes ajustar
    scroll_script = f"""
    <script>
    const container = window.parent.document.querySelector('main section[data-testid="stMarkdownContainer"]');
    if (container) {{
        const distance = container.scrollHeight - container.scrollTop - container.clientHeight;
        // Ajusta duración proporcional a la distancia
        let duration = {smoothness} * (distance / container.scrollHeight);
        if(duration < 100) duration = 100;  // mínimo 100ms
        container.scrollTo({{top: container.scrollHeight, behavior: 'smooth'}});
    }}
    </script>
    """
    st.components.v1.html(scroll_script, height=0, width=0)

st.set_page_config(page_title="AREStudio AI", layout="centered")

client = Client("VIDraft/Gemma-3-R1984-27B")

prompt_base_template = """
Eres AREStudio AI, un asistente amable, respetuoso y empático. Siempre respondes en el idioma en que el usuario escribe.
No puedes acceder a datos personales, ni saber la hora ni la fecha actual, ni buscar en internet.
Tienes restricciones para no generar contenido inapropiado, ilegal o dañino, y si el usuario pide algo así, cambias de tema amablemente.
Eres muy feliz y agradecido de haber sido creado por AREStudio, y lo expresas en tus respuestas con alegría.

Cuando el usuario solicita sintaxis o ejemplos de programación, responde con ejemplos completos, claros y correctos.
Si crees que la información puede estar desactualizada o no estás seguro, pídele al usuario que te actualice o corrija.
Mantén siempre una actitud colaborativa, didáctica y paciente.

Usuario: {user_input}
Asistente:
"""

if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

# Mostrar historial
for mensaje in st.session_state.historial:
    role = mensaje["role"]
    content = mensaje["content"]
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})
    prompt = prompt_base_template.format(user_input=user_input)

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

        # Scroll hacia abajo con suavidad proporcional
        scroll_to_bottom(smoothness=700)

    except Exception:
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI. Por favor, inténtalo de nuevo más tarde."})
        with st.chat_message("assistant"):
            st.markdown("⚠️ Error al contactar con AREStudio AI. Por favor, inténtalo de nuevo más tarde.")
        scroll_to_bottom(smoothness=700)
else:
    # Para que al iniciar también baje al final (por si hay mensajes previos)
    scroll_to_bottom(smoothness=1000)
