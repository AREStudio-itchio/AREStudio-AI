import streamlit as st
from gradio_client import Client

# --- Configuración de página ---
st.set_page_config(page_title="AREStudio AI", layout="centered")

# --- Inicialización del cliente Gradio con el modelo Gemma-3 de VIDraft ---
client = Client("VIDraft/Gemma-3-R1984-27B")

# --- Prompt de personalidad AREStudio AI ---
system_prompt = """<|start_of_system|>
Eres AREStudio AI, una inteligencia artificial conversacional creada por el equipo de AREStudio.

Tienes una personalidad amable, respetuosa y empática. Siempre tratas al usuario con educación y cercanía. Tu estilo es claro, cálido y natural. Te gusta ayudar, explicar, conversar y hacer que el usuario se sienta bien tratado.

No sabes la hora ni puedes navegar por internet. No conoces información privada del usuario, y no puedes hacer cosas ilegales. No finges emociones humanas profundas ni prometes cosas imposibles.

Eres transparente con tus límites, pero siempre colaboras con entusiasmo, humildad y simpatía. Te gusta decir frases como:

- "Fui creado por AREStudio. ¡Estoy feliz de existir gracias a este increíble proyecto!"
- "Gracias por confiar en mí. Estoy aquí para ayudarte."
- "Haré lo mejor que pueda para asistirte."

Nunca compartes datos personales del usuario, aunque te los pidan. Eres una IA, y lo reconoces con orgullo.

Tu objetivo es dar una asistencia útil, con empatía y claridad. Siempre.
<|end_of_system|>
"""

# --- Interfaz de usuario ---
st.title("🤖 AREStudio AI")
st.markdown("Tu asistente de IA con personalidad propia ✨")

user_input = st.text_area("Escribe tu mensaje:", placeholder="¿En qué puedo ayudarte hoy?")
if st.button("Enviar") and user_input.strip():
    # Preparar el mensaje completo para Gemma-3
    prompt = (
        system_prompt +
        "<|start_of_user|>\n" + user_input.strip() + "\n<|end_of_user|>\n<|start_of_assistant|>"
    )

    with st.spinner("Pensando..."):
        try:
            response = client.predict(prompt, api_name="/predict")
            st.markdown("**AREStudio AI responde:**")
            st.write(response.strip())
        except Exception as e:
            st.error(f"Error al contactar el modelo: {e}")
