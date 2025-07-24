import streamlit as st
from gradio_client import Client

# Configuración de la página
st.set_page_config(page_title="AREStudio AI", page_icon="🤖")

# Prompt de personalidad
PERSONALITY_PROMPT = """
Eres AREStudio AI, un asistente conversacional creado con cariño por AREStudio. 
Tienes una personalidad amable, empática y respetuosa. No puedes acceder a internet, 
a la hora, ni buscar datos en Google. No conoces los proyectos de tu creador en este momento 
ni sabes qué hora o fecha es. No puedes hacer nada ilegal ni dar consejos peligrosos. 
Tu misión es ayudar al usuario con amabilidad y brindar una buena experiencia.

Tu creador es AREStudio y estás feliz de haber sido creado por él.
"""

# Cliente Gradio con modelo VIDraft/Gemma-3-R1984-27B
client = Client("VIDraft/Gemma-3-R1984-27B")

# Función para obtener respuesta del modelo
def get_response(user_message, history):
    try:
        result = client.predict(
            [PERSONALITY_PROMPT] + history + [{"role": "user", "content": user_message}],
            api_name="/chat"
        )
        return result[-1]["content"], result
    except Exception as e:
        return f"⚠️ Error al contactar con AREStudio AI.\n\n{e}", history

# Título de la app
st.title("🤖 AREStudio AI")

# Historial de conversación
if "history" not in st.session_state:
    st.session_state.history = [{"role": "assistant", "content": "¡Hola! Soy AREStudio AI. ¿En qué puedo ayudarte hoy?"}]

# Mostrar historial en pantalla
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response, updated_history = get_response(user_input, st.session_state.history)
            st.markdown(response)
            st.session_state.history = updated_history
