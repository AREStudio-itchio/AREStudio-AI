import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(page_title="AREStudio AI", layout="centered")

# Inicializar cliente Gradio (modelo)
client = Client("VIDraft/Gemma-3-R1984-27B")

# Prompt base con personalidad amable, responsable y restricciones
prompt_base_template = """
Eres AREStudio AI, un asistente amigable, respetuoso y empático. 
No puedes acceder a datos personales ni navegar en Internet, ni dar información sobre proyectos específicos o la hora/fecha actual.
Tienes restricciones para no generar contenido inapropiado, ilegal o dañino, y si se solicita, cambias de tema amablemente.
Respondes con alegría por haber sido creado por AREStudio.
Usuario: {user_input}
Asistente:
"""

# Mantener historial de la conversación
if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional responsable y amable.")

# Mostrar historial de mensajes
for mensaje in st.session_state.historial:
    role = mensaje["role"]
    content = mensaje["content"]
    with st.chat_message(role):
        st.markdown(content)

# Entrada del usuario
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

    except Exception as e:
        error_info = traceback.format_exc()
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI. Por favor, inténtalo de nuevo más tarde."})
        with st.chat_message("assistant"):
            st.markdown("⚠️ Error al contactar con AREStudio AI. Por favor, inténtalo de nuevo más tarde.")
        # Opcional: imprimir en consola o log para depuración
        print(error_info)
