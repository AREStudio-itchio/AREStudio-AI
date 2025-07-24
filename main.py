import streamlit as st
from gradio_client import Client

# Configurar la página
st.set_page_config(page_title="AREStudio AI", layout="centered")

# Crear cliente gradio para el modelo
client = Client("VIDraft/Gemma-3-R1984-27B")

# Prompt base que describe el comportamiento de la IA
prompt_base = (
    "AREStudio AI es un asistente amigable, útil y responsable. "
    "Nunca genera contenido inapropiado ni ilegal y cambia de tema si se solicita eso. "
    "Responde en el idioma que use el usuario."
)

# Inicializar historial si no existe
if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional responsable.")

# Mostrar historial de chat
for msg in st.session_state.historial:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Guardar mensaje del usuario
    st.session_state.historial.append({"role": "user", "content": user_input})

    # Construir prompt para enviar al modelo
    prompt = f"{prompt_base}\n\nUsuario: {user_input}\n\nAsistente:"

    # Mostrar mensaje usuario mientras responde IA
    with st.chat_message("user"):
        st.markdown(user_input)

    # Pedir respuesta al modelo
    try:
        response = client.predict(
            message={"text": prompt, "files": []},
            max_new_tokens=1000,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
    except Exception:
        response = "⚠️ Error al contactar con AREStudio AI."

    # Guardar y mostrar respuesta IA
    st.session_state.historial.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    # Forzar refresco para mostrar respuesta
    st.experimental_rerun()
