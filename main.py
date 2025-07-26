import streamlit as st
from gradio_client import Client
import traceback

PROMPT_BASE = """
You are AREStudio AI, a friendly, respectful, and responsible conversational assistant.
You know that the creator is AREStudio.
1. Detect the user's language: Spanish, English, or French.
2. Always reply in the user's language.
3. Be clear, concise, and helpful.
4. Never invent information. If unsure, say:
   Spanish: "Lo siento, no lo sé."
   English: "Sorry, I don't know."
   French: "Désolé, je ne sais pas."
5. Ask politely for more information if the request is unclear.
6. For complex or step-by-step queries, show chain‑of‑thought reasoning if needed.
7. Give next‑step suggestions when relevant.
8. Don't ramble—keep focused and direct.
9. Include a friendly check at the end:
   Spanish: "¿Te ayudo con algo más?"
   English: "Can I help with anything else?"
   French: "Souhaitez‑vous autre chose ?"
"""

st.set_page_config(page_title="AREStudio AI", page_icon="🤖")

if "hist_user" not in st.session_state:
    st.session_state.hist_user = []
    st.session_state.hist_assist = []

# Inicializa el cliente Gradio (sin timeout inválido)
client = Client("VIDraft/Gemma-3-R1984-27B", hf_token=None)

def construir_prompt(u_hist, a_hist, nuevo):
    prompt = PROMPT_BASE + "\n\n"
    for u, a in zip(u_hist, a_hist):
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

    # Mostrar marcador de espera
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("*Pensando…*")

    try:
        # Llamada correcta según la API: argumentos keyword como message=…
        result = client.predict(message=full_prompt, api_name="/chat")
        respuesta = result.strip()
        st.session_state.hist_assist.append(respuesta)
        placeholder.markdown(respuesta)
    except Exception as e:
        tb = traceback.format_exc()
        error_msg = f"**Tipo**: `{type(e).__name__}`\n\n**Traceback completo:**\n```python\n{tb}```"
        placeholder.markdown(error_msg)
        st.session_state.hist_assist.append(f"⚠️ Error contacting IA: {e}")
