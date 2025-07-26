import streamlit as st
from gradio_client import Client
import traceback
import time

# Prompt optimizado
PROMPT_BASE = """
You are AREStudio AI, a friendly, respectful, and responsible conversational assistant.
...
Close each answer with "¿Te ayudo con algo más?" / "Can I help with anything else?" etc.
"""

st.set_page_config(page_title="AREStudio AI", page_icon="🤖")

if "hist_user" not in st.session_state:
    st.session_state.hist_user = []
    st.session_state.hist_assist = []

# Crear cliente Gradio
client = Client(
    "VIDraft/Gemma-3-R1984-27B",
    hf_token=None  # Agrega token si es privado
)

def construir_prompt(hist_u, hist_a, nuevo):
    prompt = PROMPT_BASE + "\n\n"
    for u, a in zip(hist_u, hist_a):
        prompt += f"Usuario:\n{u}\n\nAssistant:\n{a}\n\n"
    prompt += f"Usuario:\n{nuevo}\n\nAssistant:\n"
    return prompt

st.title("🤖 AREStudio AI")

# Mostrar historial
for u, a in zip(st.session_state.hist_user, st.session_state.hist_assist):
    with st.chat_message("user"):
        st.markdown(u)
    with st.chat_message("assistant"):
        st.markdown(a)

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.hist_user.append(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    full_prompt = construir_prompt(st.session_state.hist_user, st.session_state.hist_assist, prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Pensando… (esperando respuesta de API)*")

    try:
        # opción sincrónica:
        result = client.predict(message=full_prompt, api_name="/chat")
        respuesta = result.strip()
        st.session_state.hist_assist.append(respuesta)
        message_placeholder.markdown(respuesta)
    except Exception as e:
        tb = traceback.format_exc()
        err_msg = f"**Error:** `{type(e).__name__}`\n\n**Traceback completo:**\n```python\n{tb}```"
        message_placeholder.markdown(err_msg)
        st.session_state.hist_assist.append(err_msg)
