import streamlit as st
from gradio_client import Client
import traceback

# Favicon personalizado
st.set_page_config(
    page_title="AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png"
)

# Inicializar cliente IA
client = Client("VIDraft/Gemma-3-R1984-27B")

# Inicializar sesión
if "user_messages" not in st.session_state:
    st.session_state.user_messages = []
if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []
if "last_language" not in st.session_state:
    st.session_state.last_language = "en"  # inglés por defecto

# Función para deducir idioma del mensaje anterior
def detectar_idioma_anterior():
    # Buscar idioma desde el último mensaje largo del usuario
    for msg in reversed(st.session_state.user_messages):
        if len(msg.strip()) > 5:
            # Buscamos pistas por palabras clave simples (muy básico)
            if any(w in msg.lower() for w in ["qué", "cómo", "hola", "gracias"]):
                return "es"
            elif any(w in msg.lower() for w in ["bonjour", "merci", "comment"]):
                return "fr"
            elif any(w in msg.lower() for w in ["hello", "please", "thanks", "what"]):
                return "en"
    return st.session_state.last_language or "en"

# Función para construir el prompt
def construir_prompt(user_msgs, assistant_msgs, idioma):
    introducciones = {
        "es": (
            "🤖 AREStudio AI\n"
            "Tu asistente conversacional amable, respetuoso y responsable.\n"
            "Creado por AREStudio. Conoce sus proyectos aquí: https://arestudio.itch.io\n\n"
        ),
        "en": (
            "🤖 AREStudio AI\n"
            "Your friendly, respectful, and responsible conversational assistant.\n"
            "Created by AREStudio. Check out their projects here: https://arestudio.itch.io\n\n"
        ),
        "fr": (
            "🤖 AREStudio AI\n"
            "Votre assistant conversationnel aimable, respectueux et responsable.\n"
            "Créé par AREStudio. Découvrez ses projets ici : https://arestudio.itch.io\n\n"
        )
    }

    intro = introducciones.get(idioma, introducciones["en"])
    prompt = intro

    for u, a in zip(user_msgs, assistant_msgs):
        prompt += f"Usuario:\n{u}\n\nAsistente:\n{a}\n\n"

    if len(user_msgs) > len(assistant_msgs):
        prompt += f"Usuario:\n{user_msgs[-1]}\n\nAsistente:\n"

    return prompt

# Título
st.title("🤖 AREStudio AI")
st.markdown("Tu asistente creado por [AREStudio](https://arestudio.itch.io) — amable, respetuoso, responsable y ahora con favicon 🎨")

# Mostrar historial
for u_msg, a_msg in zip(st.session_state.user_messages, st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(u_msg)
    with st.chat_message("assistant"):
        st.markdown(a_msg)

if len(st.session_state.user_messages) > len(st.session_state.assistant_responses):
    with st.chat_message("user"):
        st.markdown(st.session_state.user_messages[-1])

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    try:
        # Guardar mensaje
        st.session_state.user_messages.append(user_input)

        # Detectar idioma del último mensaje válido
        idioma_actual = detectar_idioma_anterior()
        st.session_state.last_language = idioma_actual

        # Construir prompt completo con historial
        prompt = construir_prompt(
            st.session_state.user_messages,
            st.session_state.assistant_responses,
            idioma_actual
        )

        # Llamar a la IA
        respuesta = client.predict(
            prompt,
            max_new_tokens=1000,
            api_name="/chat"
        )

        respuesta_limpia = respuesta.strip()
        st.session_state.assistant_responses.append(respuesta_limpia)
        st.chat_message("assistant").markdown(respuesta_limpia)

    except Exception as e:
        tb = traceback.format_exc()
        error_msg = (
            f"⚠️ Error al contactar con AREStudio AI:\n\n"
            f"**Tipo:** `{type(e).__name__}`\n"
            f"**Mensaje:** `{e}`\n\n"
            f"**Traceback:**\n```\n{tb}```"
        )
        st.error(error_msg)
        st.session_state.assistant_responses.append(error_msg)
