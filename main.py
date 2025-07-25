import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(
    page_title="🤖 AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png",
    layout="centered"
)

client = Client("VIDraft/Gemma-3-R1984-27B")

def construir_prompt(user_msgs, assistant_msgs, nuevo_usuario):
    # Construir el prompt con contexto separado (puedes adaptarlo)
    prompt = "Eres AREStudio AI, un asistente amable, respetuoso y responsable.\n\n"
    # Añadir historial contexto mezclado
    for u_msg, a_msg in zip(user_msgs, assistant_msgs):
        prompt += f"Usuario: {u_msg}\n"
        prompt += f"Asistente: {a_msg}\n"
    # Si hay mensaje usuario sin respuesta aún
    if len(user_msgs) > len(assistant_msgs):
        prompt += f"Usuario: {nuevo_usuario}\n"
        prompt += "Asistente: "
    else:
        # Si no hay mensaje pendiente
        prompt += f"Usuario: {nuevo_usuario}\nAsistente: "
    return prompt

if "user_messages" not in st.session_state:
    st.session_state.user_messages = []
if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

# Mostrar mensajes previos en orden
for u_msg, a_msg in zip(st.session_state.user_messages, st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(u_msg)
    with st.chat_message("assistant"):
        st.markdown(a_msg)
# Si hay un mensaje del usuario sin respuesta (pendiente)
if len(st.session_state.user_messages) > len(st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(st.session_state.user_messages[-1])

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Guardar mensaje usuario inmediatamente y mostrar
    st.session_state.user_messages.append(user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir prompt con contexto para la IA
    prompt_final = construir_prompt(
        st.session_state.user_messages,
        st.session_state.assistant_responses,
        user_input
    )

    try:
        respuesta = client.predict(
            message={"text": prompt_final, "files": []},
            max_new_tokens=1000,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
        # Guardar respuesta y mostrarla
        st.session_state.assistant_responses.append(respuesta)
        with st.chat_message("assistant"):
            st.markdown(respuesta)
    except Exception as e:
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n{error_text}")
        st.session_state.assistant_responses.append("⚠️ Error al contactar con AREStudio AI.")
        with st.chat_message("assistant"):
            st.markdown("⚠️ Error al contactar con AREStudio AI.")
