import streamlit as st
from gradio_client import Client
import traceback

# Cliente Gradio para tu IA personalizada
client = Client("VIDraft/Gemma-3-R1984-27B")

# Inicialización del estado de sesión
if "user_messages" not in st.session_state:
    st.session_state.user_messages = []
if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []

# Construcción del prompt completo para enviar a la IA
def construir_prompt(user_msgs, assistant_msgs):
    base_prompt = (
        "🤖 AREStudio AI\n\n"
        "Tu asistente conversacional amable, respetuoso y responsable.\n\n"
    )
    for u, a in zip(user_msgs, assistant_msgs):
        base_prompt += f"Usuario:\n{u}\n\n"
        base_prompt += f"Asistente:\n{a}\n\n"
    if len(user_msgs) > len(assistant_msgs):
        base_prompt += f"Usuario:\n{user_msgs[-1]}\n\nAsistente:\n"
    return base_prompt

# Interfaz de Streamlit
st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

# Mostrar el historial de la conversación
for u_msg, a_msg in zip(st.session_state.user_messages, st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(u_msg)
    with st.chat_message("assistant"):
        st.markdown(a_msg)

# Mostrar el último mensaje del usuario si aún no tiene respuesta
if len(st.session_state.user_messages) > len(st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(st.session_state.user_messages[-1])

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.user_messages.append(user_input)
    prompt = construir_prompt(st.session_state.user_messages, st.session_state.assistant_responses)
    
    try:
        respuesta = client.predict(
            prompt,
            max_new_tokens=1000,
            api_name="/chat"
        )
        respuesta_limpia = respuesta.strip()
        st.session_state.assistant_responses.append(respuesta_limpia)
        st.chat_message("assistant").markdown(respuesta_limpia)

    except Exception as e:
        tb = traceback.format_exc()
        error_detallado = (
            f"⚠️ Error al contactar con AREStudio AI:\n\n"
            f"**Tipo:** `{type(e).__name__}`\n"
            f"**Mensaje:** `{e}`\n\n"
            f"**Traceback:**\n```\n{tb}\n```"
        )
        st.error(error_detallado)
        st.session_state.assistant_responses.append(error_detallado)
