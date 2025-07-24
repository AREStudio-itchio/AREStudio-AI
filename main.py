import streamlit as st
import requests
from bs4 import BeautifulSoup
from gradio_client import Client, handle_file
import random
import re

# --- CONFIGURACIÓN DEL MODELO GEMMA-3 (Hugging Face Space) ---
GEMMA_MODEL_SPACE_ID = "VIDraft/Gemma-3-R1984-27B"
GEMMA_API_ENDPOINT = "/chat"
MAX_NEW_TOKENS = 1000
USE_WEB_SEARCH = False
USE_KOREAN = False
MAX_HISTORY_PAIRS = 5

# --- FUNCIÓN PARA SCRAPING LEGAL DE PROYECTOS DE ITCH.IO ---
@st.cache_data(ttl=3600)
def get_arestudio_projects():
    url = "https://arestudio.itch.io"
    headers = {"User-Agent": "AREStudioBot/1.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        projs = []
        for a in soup.select("a.title.game_link"):
            title = a.text.strip()
            link = a.get("href")
            if title and link:
                projs.append({"title": title, "url": link})
        return projs
    except Exception as e:
        st.warning(f"No he podido obtener los proyectos de itch.io en este momento. Error: {e}")
        return []

# --- CLIENTE GRADIO (SIN CACHE, CON MANEJO DE ERRORES) ---
def get_gemma_client():
    try:
        return Client(GEMMA_MODEL_SPACE_ID)
    except Exception as e:
        st.error(f"❌ Error al inicializar el cliente de Gemma: {e}")
        return None

gemma_client = get_gemma_client()

# --- FUNCIÓN PARA CONSULTAR LA IA (GEMMA-3) ---
def consultar_gemma(user_prompt): 
    gemma_input_message = {"text": user_prompt, "files": []}
    try:
        resp = gemma_client.predict(
            message=gemma_input_message,
            max_new_tokens=MAX_NEW_TOKENS,
            use_web_search=USE_WEB_SEARCH,
            use_korean=USE_KOREAN,
            api_name=GEMMA_API_ENDPOINT
        )
        return resp if isinstance(resp, str) else resp[0]
    except Exception as e:
        st.error(f"⚠️ ¡Error al consultar la IA! Detalles: {e}")
        return "Lo siento, hubo un problema al consultar la IA."

# --- CONFIGURACIÓN DE STREAMLIT ---
st.set_page_config(page_icon="🤖", page_title="AREStudio AI")

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Saludo inicial
if "init_greeting_done" not in st.session_state:
    st.session_state.init_greeting_done = True
    saludo = random.choice([
        "¡Hola! Soy AREStudio AI, un asistente creado por AREStudio. ¿En qué puedo ayudarte hoy?",
        "¡Hola! Soy AREStudio AI. Estoy aquí para ayudarte con cualquier consulta sobre AREStudio o si tienes alguna pregunta general.",
        "¡Saludos! Soy AREStudio AI, tu asistente de AREStudio. ¿Cómo puedo asistirte hoy?"
    ])
    st.session_state.messages.append({"role": "assistant", "content": saludo})

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Validación de entrada
def is_meaningful_input(text):
    return len(text.strip()) >= 3 and bool(re.search(r'[a-zA-Z0-9]', text))

# Entrada del usuario
user_prompt = st.chat_input("Escribe tu pregunta aquí...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    if not is_meaningful_input(user_prompt):
        assistant_response = "Lo siento, parece que no entendí eso. Por favor, haz una pregunta clara y con más detalles."
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        lower_prompt = user_prompt.lower()
        if any(k in lower_prompt for k in ["proyecto", "juego", "itch.io", "arestudio", "tuyo", "tu", "mi", "mis", "vuestro", "vuestros", "vuestra", "vuestras", "creador", "estudio"]):
            projs = get_arestudio_projects()
            if projs:
                response_text = "¡Claro! AREStudio tiene varios proyectos interesantes. ¿Te gustaría que te liste algunos o te dé el enlace a nuestra página de itch.io para que los veas todos?"
            else:
                response_text = "Lo siento, no he podido obtener los proyectos de AREStudio en este momento."
            with st.chat_message("assistant"):
                st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            if gemma_client:
                respuesta_gemma = consultar_gemma(user_prompt)
            else:
                respuesta_gemma = "Lo siento, el modelo de IA no está disponible en este momento."
            with st.chat_message("assistant"):
                st.markdown(respuesta_gemma)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_gemma})
