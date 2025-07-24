import streamlit as st
import requests
from bs4 import BeautifulSoup
from gradio_client import Client
import random
import re # Importar re para validación de entrada

# --- CONFIGURACIÓN DEL MODELO GEMMA-3 (Hugging Face Space) ---
GEMMA_MODEL_SPACE_ID = "VIDraft/Gemma-3-R1984-27B"
GEMMA_API_ENDPOINT = "/chat"
MAX_NEW_TOKENS = 1000
USE_WEB_SEARCH = False
USE_KOREAN = False

# NOTA: MAX_HISTORY_PAIRS y la lógica de 'formatted_chat_history'
# ya no son directamente necesarios para la llamada a gemma_client.predict()
# porque el parámetro 'history' no es aceptado por este modelo específico.
# Sin embargo, mantenemos 'st.session_state.messages' para mostrar el historial en la interfaz.
MAX_HISTORY_PAIRS = 5 # Aún útil si en el futuro se cambia a un modelo con soporte de historial

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

# --- CLIENTE GRADIO PARA CONECTARSE AL MODELO GEMMA-3 ---
@st.cache_resource
def get_gemma_client():
    return Client(GEMMA_MODEL_SPACE_ID)

gemma_client = get_gemma_client()

# --- FUNCIÓN PARA CONSULTAR LA IA (GEMMA-3) ---
def consultar_gemma(user_prompt): 
    # *** CAMBIO CRÍTICO AQUÍ: 'message' ahora es un diccionario como la API espera ***
    gemma_input_message = {"text": user_prompt, "files": []}

    try:
        resp = gemma_client.predict(
            message=gemma_input_message, # Pasar el diccionario con 'text' y 'files'
            max_new_tokens=MAX_NEW_TOKENS,
            use_web_search=USE_WEB_SEARCH,
            use_korean=USE_KOREAN,
            api_name=GEMMA_API_ENDPOINT
        )
        return resp if isinstance(resp, str) else resp[0]
    except Exception as e:
        st.error(f"⚠️ ¡Error de red o conexión con la IA! Por favor, inténtalo de nuevo. Detalles: {e}")
        return "Lo siento, hubo un problema al consultar la IA en este momento."

# --- CONFIGURACIÓN DE LA INTERFAZ DE STREAMLIT ---
st.set_page_config(page_icon="🤖", page_title="AREStudio AI")

# Inicializa el historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Lógica para el saludo inicial de la IA
if "init_greeting_done" not in st.session_state:
    st.session_state.init_greeting_done = True
    saludo = random.choice([
        "¡Hola! Soy AREStudio AI, un asistente creado por AREStudio. ¿En qué puedo ayudarte hoy?",
        "¡Hola! Soy AREStudio AI. Estoy aquí para ayudarte con cualquier consulta sobre AREStudio o si tienes alguna pregunta general.",
        "¡Saludos! Soy AREStudio AI, tu asistente de AREStudio. ¿Cómo puedo asistirte hoy?"
    ])
    st.session_session.messages.append({"role": "assistant", "content": saludo})

# Muestra todos los mensajes del historial en la interfaz de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- VALIDACIÓN BÁSICA DE ENTRADA DEL USUARIO ---
def is_meaningful_input(text):
    return len(text.strip()) >= 3 and bool(re.search(r'[a-zA-Z0-9]', text))

# Campo de entrada de texto para el usuario
user_prompt = st.chat_input("Escribe tu pregunta aquí...")

# Procesa la entrada del usuario si hay un prompt
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
        # --- LÓGICA DE PROMOCIÓN CONDICIONAL DE ARESTUDIO ---
        if any(k in lower_prompt for k in ["proyecto", "juego", "itch.io", "arestudio", "tuyo", "tu", "mi", "mis", "vuestro", "vuestros", "vuestra", "vuestras", "creador", "estudio"]):
            projs = get_arestudio_projects()
            if projs:
                response_text = "¡Claro! AREStudio tiene varios proyectos interesantes. ¿Te gustaría que te liste algunos o te dé el enlace a nuestra página de itch.io para que los veas todos?"
            else:
                response_text = "Lo siento, no he podido obtener los proyectos de AREStudio en este momento. Puede que haya un problema con la conexión a la página."
            
            with st.chat_message("assistant"):
                st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            respuesta_gemma = consultar_gemma(user_prompt) 
            with st.chat_message("assistant"):
                st.markdown(respuesta_gemma)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_gemma})

