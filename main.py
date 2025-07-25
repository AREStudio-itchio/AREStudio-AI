import streamlit as st
from gradio_client import Client

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
    for u, a in zip(user_msgs, assistant_msgs):
        base_prompt += f"Usuario:\n{u}\n\n"
        base_prompt += f"Asistente:\n{a}\n\n"
    if len(user_msgs) > len(assistant_msgs):
        base_prompt += f"Usuario:\n{user_msgs[-1]}\n\nAsistente:\n"
    return base_prompt

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

for u_msg, a_msg in zip(st.session_state.user_messages, st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(u_msg)
    with st.chat_message("assistant"):
        st.markdown(a_msg)

if len(st.session_state.user_messages) > len(st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(st.session_state.user_messages[-1])

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
        st.session_state.assistant_responses.append(respuesta.strip())
        st.chat_message("assistant").markdown(respuesta.strip())
    except Exception:
        st.error("⚠️ Error al contactar con AREStudio AI.")
        st.session_state.assistant_responses.append("⚠️ Error al contactar con AREStudio AI.")
