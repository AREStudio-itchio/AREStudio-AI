import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(
    page_title="🤖 AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png",
    layout="centered"
)

client = Client("VIDraft/Gemma-3-R1984-27B")

if "user_messages" not in st.session_state:
    st.session_state.user_messages = []
if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []

def construir_prompt(user_msgs, assistant_msgs):
    base_prompt = (
        "🤖 AREStudio AI\n\n"
        "Tu asistente conversacional amable, respetuoso y responsable.\n\n"
    )
    # Construir el diálogo completo alternando mensajes
    for u, a in zip(user_msgs, assistant_msgs):
        base_prompt += f"Usuario:\n{u}\n\n"
        base_prompt += f"Asistente:\n{a}\n\n"
    # Añadir mensaje de usuario pendiente respuesta
    if len(user_msgs) > len(assistant_msgs):
        base_prompt += f"Usuario:\n{user_msgs[-1]}\n\nAsistente:\n"
    return base_prompt

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

# Mostrar todo el historial estilo chat
for u_msg, a_msg in zip(st.session_state.user_messages, st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(u_msg)
    with st.chat_message("assistant"):
        st.markdown(a_msg)

# Mostrar último mensaje del usuario pendiente respuesta
if len(st.session_state.user_messages) > len(st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(st.session_state.user_messages[-1])

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.user_messages.append(user_input)

    prompt = construir_prompt(st.session_state.user_messages, st.session_state.assistant_responses)

    with st.chat_message("assistant"):
        try:
            respuesta = client.predict(
                prompt,
                max_new_tokens=1000,
                api_name="/chat"
            )
            st.session_state.assistant_responses.append(respuesta.strip())
            st.markdown(respuesta.strip())
        except Exception as e:
            st.error("⚠️ Error al contactar con AREStudio AI.")
            st.session_state.assistant_responses.append("⚠️ Error al contactar con AREStudio AI.")
