import streamlit as st
import requests
from bs4 import BeautifulSoup
from gradio_client import Client

# Cliente Gradio sin mostrar modelo al usuario
client = Client("VIDraft/Gemma-3-R1984-27B")

st.set_page_config(page_title="AREStudio AI", layout="centered")
st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional útil y responsable.")

# Prompt base para la IA
prompt_sistema = (
    "AREStudio AI es un asistente conversacional diseñado para ayudar al usuario con respuestas claras, educativas y útiles. "
    "Responde con responsabilidad, mantiene un tono respetuoso, y evita temas delicados si pueden ser sensibles. "
    "No permite contenido ofensivo, peligroso o inapropiado. "
    "Siempre intenta ser útil y cordial, ayudando con programación, ideas creativas, tareas escolares, y más."
)

# Función para hacer scraping legal en arestudio.itch.io y obtener proyectos
def obtener_proyectos():
    url = "https://arestudio.itch.io/"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        # Aquí el selector CSS o XPath para encontrar proyectos: ejemplo, buscar los links con clase "game_cell_link"
        proyectos = []
        for a in soup.select("a.game_cell_link"):
            titulo = a.get("title") or a.text.strip()
            enlace = a.get("href")
            if enlace and not enlace.startswith("http"):
                enlace = "https://arestudio.itch.io" + enlace
            if titulo and enlace:
                proyectos.append(f"[{titulo}]({enlace})")
        return proyectos
    except Exception:
        return []

# Mostrar mensajes previos
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for rol, mensaje in st.session_state.mensajes:
    with st.chat_message("user" if rol == "usuario" else "assistant"):
        st.markdown(mensaje)

# Entrada usuario
entrada = st.chat_input("Escribe tu mensaje...")

if entrada:
    st.session_state.mensajes.append(("usuario", entrada))
    with st.chat_message("user"):
        st.markdown(entrada)

    # Aquí llamamos a la función scraping
    proyectos = obtener_proyectos()

    # Construir el prompt con info sobre proyectos solo si hay
    if proyectos:
        proyectos_str = "\n".join(f"- {p}" for p in proyectos)
        prompt = (
            f"{prompt_sistema}\n\n"
            f"El usuario preguntó: {entrada}\n\n"
            f"AREStudio tiene estos proyectos actualmente:\n{proyectos_str}\n\n"
            "Responde en el idioma del usuario."
        )
    else:
        prompt = (
            f"{prompt_sistema}\n\n"
            f"El usuario preguntó: {entrada}\n\n"
            "Actualmente no hay proyectos disponibles en AREStudio. "
            "Pero estamos trabajando en cosas emocionantes y esperamos tener nuevos proyectos pronto. "
            "Por favor, mantente atento para futuras actualizaciones."
            "\n\nResponde en el idioma del usuario."
        )

    try:
        respuesta = client.predict(prompt, api_name="/chat")
    except Exception as e:
        respuesta = "⚠️ Error al contactar con AREStudio AI."

    st.session_state.mensajes.append(("asistente", respuesta))
    with st.chat_message("assistant"):
        st.markdown(respuesta)
