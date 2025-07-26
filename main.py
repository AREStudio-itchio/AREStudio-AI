import streamlit as st
from gradio_client import Client
import traceback

# Prompt optimizado para detección y respuesta en el idioma del usuario
PROMPT_BASE = """
You are AREStudio AI, a friendly, respectful, and responsible conversational assistant.
1. Detect the user's language: Spanish, English, or French.
2. Always reply in the user's language.
3. Be clear, concise, and helpful.
4. Never invent information. If unsure, say:
   Spanish: "Lo siento, no lo sé."
   English: "Sorry, I don't know."
   French: "Désolé, je ne sais pas."
5. Ask politely for more information if the request is unclear.
6. For complex or step-by-step queries, show chain-of-thought reasoning if needed.
7. Give next-step suggestions when relevant.
8. Don't ramble—keep focused and direct.
9. Include a friendly check at the end:
   Spanish: "¿Te ayudo con algo más?"
   English: "Can I help with anything else?"
   French: "Souhaitez-vous autre chose ?"
"""

st.set_page_config(page_title="AREStudio AI", page_icon="🤖")

# Inicializar el historial si no existe
if "hist_user" not in st.session_state:
    st.session_state.hist_user = []
    st.session_state.hist_assist = []

# Conectar con el cliente de Gradio
client = Client("VIDraft/Gemma-3-R1984-27B")

def construir_prompt(hist_u, hist_a, nuevo):
    prompt = PROMPT_BASE + "\n\n"
    for u, a in zip(hist_u, hist_a):
        prompt += f"Usuario:\n{u}\n\nAssistant:\n{a}\n\n"
    prompt += f"Usuario:\n{nuevo}\n\nAssistant:\n"
    return prompt

# Título de la aplicación
st.title("🤖 AREStudio AI")

# Mostrar el historial de la conversación
for u, a in zip(st.session_state.hist_user, st.session_state.hist_assist):
    with st.chat_message("user"):
        st.markdown(u)
    with st.chat_message("assistant"):
        st.markdown(a)

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.hist_user.append(user_input)
    prompt = construir_prompt(
        st.session_state.hist_user,
        st.session_state.hist_assist,
        user_input
    )

    try:
        with st.spinner("Pensando…"):
            respuesta = client.predict(
                prompt,
                max_new_tokens=600,
                api_name="/chat",
                timeout=60
            )
        respuesta = respuesta.strip()
        st.session_state.hist_assist.append(respuesta)
        with st.chat_message("assistant"):
            st.markdown(respuesta)
    except Exception as e:
        tb = traceback.format_exc()
        st.error("⚠️ Oops, algo salió mal al contactar con la IA.")
        st.write(f"`{type(e).__name__}: {e}`")
        st.session_state.hist_assist.append("⚠️ Error al contactar con la IA.")
