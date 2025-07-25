import streamlit as st
from gradio_client import Client

client = Client("VIDraft/Gemma-3-R1984-27B")

if "user_messages" not in st.session_state:
    st.session_state.user_messages = []
if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []

def construir_prompt(user_msgs, assistant_msgs):
    # Contexto base
    base_prompt = (
        "🤖 AREStudio AI\n\n"
        "Tu asistente conversacional amable, respetuoso y responsable.\n\n"
    )
    # Añadimos historial de mensajes alternando roles
    for u, a in zip(user_msgs, assistant_msgs):
        base_prompt += f"Usuario:\n{u}\n\n"
        base_prompt += f"Asistente:\n{a}\n\n"
    # Si el usuario acaba de enviar un mensaje que no tiene respuesta aún
    if len(user_msgs) > len(assistant_msgs):
        base_prompt += f"Usuario:\n{user_msgs[-1]}\n\nAsistente:\n"
    return base_prompt

st.title("🤖 AREStudio AI")

# Mostrar conversación previa
for u_msg, a_msg in zip(st.session_state.user_messages, st.session_state.assistant_responses):
    st.markdown(f"**Usuario:** {u_msg}")
    st.markdown(f"**Asistente:** {a_msg}")

# Mostrar último mensaje de usuario pendiente de respuesta
if len(st.session_state.user_messages) > len(st.session_state.assistant_responses):
    st.markdown(f"**Usuario:** {st.session_state.user_messages[-1]}")

user_input = st.text_input("Escribe tu mensaje...")

if user_input:
    st.session_state.user_messages.append(user_input)
    prompt = construir_prompt(st.session_state.user_messages, st.session_state.assistant_responses)
    try:
        respuesta = client.predict(
            prompt,
            max_new_tokens=500,
            api_name="/chat"
        )
        st.session_state.assistant_responses.append(respuesta.strip())
    except Exception as e:
        st.error(f"Error contactando con AREStudio AI: {e}")
        st.session_state.assistant_responses.append("⚠️ Error al contactar con AREStudio AI.")

    # Mostrar último intercambio
    st.markdown(f"**Usuario:** {user_input}")
    st.markdown(f"**Asistente:** {st.session_state.assistant_responses[-1]}")
