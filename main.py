import streamlit as st
from gradio_client import Client
import traceback

# Define el prompt base
PROMPT_BASE = """
Eres AREStudio AI, un asistente conversacional amigable, respetuoso y responsable.
Sabes que el creador es AREStudio.
1. Detecta el idioma del usuario: español, inglés o francés.
2. Responde siempre en el idioma del usuario.
3. Sé claro, conciso y útil.
4. Nunca inventes información. Si no sabes algo, di:
   Español: "Lo siento, no lo sé."
   Inglés: "Sorry, I don't know."
   Francés: "Désolé, je ne sais pas."
5. Si la solicitud no está clara, pide amablemente más información.
6. Para consultas complejas o paso a paso, muestra razonamiento en cadena si es necesario.
7. Ofrece sugerencias de próximos pasos cuando sea relevante.
8. No divagues: mantén el enfoque y la brevedad.
9. Incluye un cierre amable:
   Español: "¿Te ayudo con algo más?"
   Inglés: "Can I help with anything else?"
   Francés: "Souhaitez-vous autre chose ?"
"""

# Configura la página de Streamlit
st.set_page_config(page_title="AREStudio AI", page_icon="🤖")

# Inicializa el historial de conversación si no existe
if "hist_user" not in st.session_state:
    st.session_state.hist_user = []
    st.session_state.hist_assist = []

# Inicializa el cliente de Gradio
client = Client("VIDraft/Gemma-3-R1984-27B", api_name="/chat")

# Función para construir el prompt completo
def construir_prompt(u_hist, a_hist, nuevo):
    prompt = PROMPT_BASE + "\n\n"
    for u, a in zip(u_hist, a_hist):
        prompt += f"Usuario:\n{u}\n\nAssistant:\n{a}\n\n"
    prompt += f"Usuario:\n{nuevo}\n\nAssistant:\n"
    return prompt

# Título de la aplicación
st.title("🤖 AREStudio AI")

# Muestra el historial de la conversación
for u, a in zip(st.session_state.hist_user, st.session_state.hist_assist):
    with st.chat_message("user"):
        st.markdown(u)
    with st.chat_message("assistant"):
        st.markdown(a)

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.hist_user.append(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Construye el prompt completo
    full_prompt = construir_prompt(st.session_state.hist_user, st.session_state.hist_assist, prompt)

    # Muestra el marcador de espera
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("*Pensando…*")

    try:
        # Llama a la API de Gradio
        result = client.predict(message=full_prompt)
        respuesta = result.strip()
        st.session_state.hist_assist.append(respuesta)
        placeholder.markdown(respuesta)
    except Exception as e:
        # Captura y muestra el error
        tb = traceback.format_exc()
        error_msg = f"**Tipo**: `{type(e).__name__}`\n\n**Traceback completo:**\n```python\n{tb}```"
        placeholder.markdown(error_msg)
        st.session_state.hist_assist.append(f"⚠️ Error al contactar con la IA: {e}")
