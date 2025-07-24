import streamlit as st
from gradio_client import Client

# Configuración inicial de la página
st.set_page_config(page_title="AREStudio AI", layout="centered")
st.title("AREStudio AI")
st.markdown("Asistente conversacional útil y responsable.")

# Inicializar historial si no existe
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Conectar al cliente de Gradio (sin mostrar detalles)
client = Client("VIDraft/Gemma-3-R1984-27B")

# Prompt del sistema que da contexto
prompt_sistema = (
    "AREStudio AI es un asistente conversacional diseñado para ayudar al usuario con respuestas claras, educativas y útiles. "
    "Responde con responsabilidad, mantiene un tono respetuoso, y evita temas delicados si pueden ser sensibles. "
    "No permite contenido ofensivo, peligroso o inapropiado. "
    "Siempre intenta ser útil y cordial, ayudando con programación, ideas creativas, tareas escolares, y más."
)

# Mostrar historial de conversación
for rol, mensaje in st.session_state.mensajes:
    with st.chat_message(role=rol):
        st.markdown(mensaje)

# Entrada del usuario
entrada = st.chat_input("Escribe tu mensaje...")

if entrada:
    # Añadir mensaje del usuario
    st.session_state.mensajes.append(("user", entrada))
    with st.chat_message("user"):
        st.markdown(entrada)

    # Combinar el contexto con la entrada del usuario
    mensaje = f"{prompt_sistema}\n\nUsuario: {entrada}\n\nAsistente:"

    try:
        respuesta = client.predict(mensaje, api_name="/chat")

        # Añadir respuesta al historial
        st.session_state.mensajes.append(("assistant", respuesta))
        with st.chat_message("assistant"):
            st.markdown(respuesta)

    except Exception:
        error_msg = "⚠️ Error al contactar con AREStudio AI."
        st.session_state.mensajes.append(("assistant", error_msg))
        with st.chat_message("assistant"):
            st.markdown(error_msg)
