import streamlit as st
from gradio_client import Client

# Configuración de la página
st.set_page_config(page_title="AREStudio AI", layout="centered")
st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional útil y responsable.")

# Mensaje inicial del sistema (no se muestra al usuario)
prompt_sistema = (
    "AREStudio AI es un asistente conversacional diseñado para ayudar al usuario con respuestas claras, educativas y útiles. "
    "Responde con responsabilidad, mantiene un tono respetuoso, y evita temas delicados si pueden ser sensibles. "
    "No permite contenido ofensivo, peligroso o inapropiado. "
    "Siempre intenta ser útil y cordial, ayudando con programación, ideas creativas, tareas escolares, y más."
)

# Inicialización de sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Cliente de Gradio (NO se muestra el modelo al usuario)
client = Client("VIDraft/Gemma-3-R1984-27B")

# Mostrar el historial de mensajes
for rol, mensaje in st.session_state.mensajes:
    emoji = "🧑" if rol == "usuario" else "🤖"
    with st.chat_message(rol):
        st.markdown(f"{emoji} {mensaje}")

# Entrada del usuario
prompt_usuario = st.chat_input("Escribe tu mensaje...")

if prompt_usuario:
    # Mostrar mensaje del usuario
    st.session_state.mensajes.append(("usuario", prompt_usuario))
    with st.chat_message("usuario"):
        st.markdown(f"🧑 {prompt_usuario}")

    # Crear el mensaje combinado
    mensaje_completo = f"{prompt_sistema}\n\nUsuario: {prompt_usuario}\n\nAsistente:"

    # Obtener la respuesta del modelo
    try:
        respuesta = client.predict(
            mensaje_completo,
            api_name="/chat"
        )
    except Exception as e:
        respuesta = "⚠️ Error al contactar con AREStudio AI."

    # Mostrar respuesta
    st.session_state.mensajes.append(("asistente", respuesta))
    with st.chat_message("assistant"):
        st.markdown(f"🤖 {respuesta}")
