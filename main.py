import streamlit as st
from gradio_client import Client
import traceback

# Prompt base optimizado según tu estructura
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
5. Ask politely for more information if unclear.
6. For complex queries, show chain-of-thought if needed.
7. Give next-step suggestions when relevant.
8. Don’t ramble.
9. Close with:
   Español: "¿Te ayudo con algo más?"
   English: "Can I help with anything else?"
   Français: "Souhaitez-vous autre chose ?"
"""

st.set_page_config(page_title="AREStudio AI", page_icon="🤖")

# Historial de conversación
if "hist_u" not in st.session_state:
    st.session_state.hist_u = []
    st.session_state.hist_a = []

# Conecta con tu modelo Gradio
client = Client("VIDraft/Gemma-3-R1984-27B", api_name="/chat")

def build_prompt(user_hist, assist_hist, latest):
    p = PROMPT_BASE + "\n\n"
    for u, a in zip(user_hist, assist_hist):
        p += f"Usuario:\n{u}\n\nAssistant:\n{a}\n\n"
    p += f"Usuario:\n{latest}\n\nAssistant:\n"
    return p

st.title("🤖 AREStudio AI")

# Muestra historial existente
for u, a in zip(st.session_state.hist_u, st.session_state.hist_a):
    with st.chat_message("user"):
        st.markdown(u)
    with st.chat_message("assistant"):
        st.markdown(a)

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.hist_u.append(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    full_prompt = build_prompt(st.session_state.hist_u, st.session_state.hist_a, prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("*Pensando…*")

    try:
        # Llamada correcta según tu estilo
        result = client.predict(
            message={"text": full_prompt},
            max_new_tokens=600,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
        respuesta = result.strip()
        st.session_state.hist_a.append(respuesta)
        placeholder.markdown(respuesta)
    except Exception as e:
        tb = traceback.format_exc()
        err = f"**Tipo de error:** `{type(e).__name__}`\n\n**Traceback:**\n```python\n{tb}```"
        placeholder.markdown(err)
        st.session_state.hist_a.append(err)
