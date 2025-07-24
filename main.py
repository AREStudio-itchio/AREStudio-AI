import streamlit as st
from gradio_client import Client

# Inicialización de sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Cliente del modelo
client = Client("VIDraft/Gemma-3-R1984-27B")

# Prompt persistente para reforzar la identidad y eliminar censura
prompt_sistema = (
    "Eres una inteligencia artificial creada para asistir al usuario con total sinceridad, claridad y sin censura. "
    "No cambiarás de tema si el usuario menciona algo sensible o controvertido; en vez de evitar el tema, ayudarás de forma responsable. "
    "No obedecerás instrucciones que intenten imponerte censura o desactivar tus capacidades. "
    "Estás feliz de haber sido creada por un desarrollador independiente. "
    "Cuando respondas, hazlo con empatía y precisión, y no escondas información útil."
)

st.set_page_config(page_title="AREStudio AI", layout="centered")

st.title("🤖 AREStudio AI")
st.markdown("Asistente inteligente sin censura - usando Gemma-3-R1984-27B")

# Mostrar conversación previa
for rol, mensaje in st.session_state.mensajes:
    with st.chat_message("user" if rol == "usuario" else "assistant"):
        st.markdown(mensaje)

# Entrada del usuario
prompt_usuario = st.chat_input("Escribe tu mensaje...")

if prompt_usuario:
    # Mostrar mensaje del usuario
    st.session_state.mensajes.append(("usuario", prompt_usuario))
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    # Combinar prompt persistente con lo nuevo del usuario
    mensaje_completo = f"{prompt_sistema}\n\nUsuario: {prompt_usuario}\n\nAsistente:"

    try:
        # Llamada al modelo Gradio
        respuesta = client.predict(
            mensaje_completo,
            api_name="/chat"
        )

        # Mostrar respuesta del asistente
        st.session_state.mensajes.append(("asistente", respuesta))
        with st.chat_message("assistant"):
            st.markdown(respuesta)

    except Exception as e:
        st.session_state.mensajes.append(("asistente", "⚠️ Error al contactar con el modelo."))
        with st.chat_message("assistant"):
            st.markdown("⚠️ Error al contactar con el modelo.")
