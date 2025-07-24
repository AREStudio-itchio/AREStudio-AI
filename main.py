import streamlit as st
from gradio_client import Client

# Inicialización de sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Cliente de Gradio (modelo no mencionado)
client = Client("VIDraft/Gemma-3-R1984-27B")  # Se conecta internamente, pero no se muestra al usuario

# Descripción general de AREStudio AI
prompt_sistema = (
    "AREStudio AI es un asistente conversacional diseñado para ayudar al usuario con respuestas claras, educativas y útiles. "
    "Responde con responsabilidad, mantiene un tono respetuoso, y evita temas delicados si pueden ser sensibles. "
    "No permite contenido ofensivo, peligroso o inapropiado. "
    "Siempre intenta ser útil y cordial, ayudando con programación, ideas creativas, tareas escolares, y más."
)

st.set_page_config(page_title="AREStudio AI", layout="centered")

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional útil y responsable.")

# Mostrar mensajes previos
for rol, mensaje in st.session_state.mensajes:
    with st.chat_message("user" if rol == "usuario" else "assistant"):
        st.markdown(mensaje)

# Entrada del usuario
prompt_usuario = st.chat_input("Escribe tu mensaje...")

if prompt_usuario:
    st.session_state.mensajes.append(("usuario", prompt_usuario))
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    # Unir el mensaje con el prompt inicial
    mensaje_completo = f"{prompt_sistema}\n\nUsuario: {prompt_usuario}\n\nAsistente:"

    try:
        respuesta = client.predict(
            mensaje_completo,
            api_name="/chat"
        )

        st.session_state.mensajes.append(("asistente", respuesta))
        with st.chat_message("assistant"):
            st.markdown(respuesta)

    except Exception as e:
        st.session_state.mensajes.append(("asistente", "⚠️ Error al contactar con AREStudio AI."))
        with st.chat_message("assistant"):
            st.markdown("⚠️ Error al contactar con AREStudio AI.")
