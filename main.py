import streamlit as st
import requests
from bs4 import BeautifulSoup
from gradio_client import Client, handle_file
import random
import re

# --- CONFIGURACIÓN DEL MODELO GEMMA ---
GEMMA_MODEL_SPACE_ID = "VIDraft/Gemma-3-R1984-27B"
GEMMA_API_ENDPOINT = "/chat"
MAX_NEW_TOKENS = 1000
USE_WEB_SEARCH = False
USE_KOREAN = False

# --- IDIOMA UI ---
IDIOMAS = {
    "es": {
        "title": "AREStudio AI - Asistente Multilingüe",
        "intro": "🧠 Hola. Soy tu asistente de AREStudio. Puedes preguntarme sobre nuestros proyectos, IA, programación, y mucho más.",
        "input_placeholder": "Escribe tu pregunta aquí...",
        "load_error": "No he podido obtener los proyectos de itch.io. Error: ",
        "ai_error": "❌ Error al inicializar el cliente de Gemma:",
        "meaningless": "Lo siento, parece que no entendí eso. Por favor, haz una pregunta clara y con más detalles.",
        "no_projects": "Lo siento, no he podido obtener los proyectos de AREStudio en este momento.",
        "show_projects": "¡Claro! AREStudio tiene varios proyectos interesantes. ¿Te gustaría que te liste algunos o te dé el enlace a nuestra página de itch.io para que los veas todos?",
        "ai_down": "Lo siento, el modelo de IA no está disponible en este momento."
    },
    "en": {
        "title": "AREStudio AI - Multilingual Assistant",
        "intro": "🧠 Hello. I'm your assistant from AREStudio. You can ask me about our projects, AI, programming, and more.",
        "input_placeholder": "Type your question here...",
        "load_error": "I couldn’t load the itch.io projects. Error: ",
        "ai_error": "❌ Error initializing the Gemma client:",
        "meaningless": "Sorry, I didn't understand that. Please ask a clearer question.",
        "no_projects": "Sorry, I couldn't fetch AREStudio's projects at the moment.",
        "show_projects": "Sure! AREStudio has several interesting projects. Want me to list some or share the itch.io page?",
        "ai_down": "Sorry, the AI model is not available right now."
    },
    "ca": {
        "title": "AREStudio AI - Assistent Multilingüe",
        "intro": "🧠 Hola. Soc l'assistent d'AREStudio. Pots preguntar-me sobre els nostres projectes, IA, programació, i més.",
        "input_placeholder": "Escriu la teva pregunta aquí...",
        "load_error": "No he pogut carregar els projectes d'itch.io. Error: ",
        "ai_error": "❌ Error en iniciar el client de Gemma:",
        "meaningless": "Ho sento, no he entès això. Fes una pregunta més clara, si us plau.",
        "no_projects": "Ho sento, no he pogut obtenir els projectes d'AREStudio ara mateix.",
        "show_projects": "És clar! AREStudio té diversos projectes interessants. Vols que te'ls llisti o et passi l'enllaç a la nostra pàgina d'itch.io?",
        "ai_down": "Ho sento, el model d'IA no està disponible ara mateix."
    }
}

# Selección de idioma
lang = st.sidebar.selectbox("🌐 Idioma / Language / Llengua", options=["es", "en", "ca"], index=0)
T = IDIOMAS[lang]

# --- CONFIG STREAMLIT ---
st.set_page_config(page_title=T["title"], page_icon="🤖")
st.title(T["title"])
st.write(T["intro"])

# --- SCRAPING LEGAL ---
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
        st.warning(f"{T['load_error']}{e}")
        return []

# --- CLIENTE GEMMA ---
def get_gemma_client():
    try:
        return Client(GEMMA_MODEL_SPACE_ID)
    except Exception as e:
        st.error(f"{T['ai_error']} {e}")
        return None

gemma_client = get_gemma_client()

# --- CONSULTA GEMMA ---
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
        st.error(f"⚠️ Error al consultar la IA: {e}")
        return T["ai_down"]

# --- HISTORIAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "init_greeting_done" not in st.session_state:
    st.session_state.init_greeting_done = True
    saludo = random.choice([
        "¡Hola! Soy AREStudio AI, un asistente creado por AREStudio. ¿En qué puedo ayudarte hoy?",
        "¡Hola! Soy AREStudio AI. Estoy aquí para ayudarte con cualquier consulta sobre AREStudio o si tienes alguna pregunta general.",
        "¡Saludos! Soy AREStudio AI, tu asistente de AREStudio. ¿Cómo puedo asistirte hoy?"
    ])
    st.session_state.messages.append({"role": "assistant", "content": saludo})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- VALIDACIÓN DE ENTRADA ---
def is_meaningful_input(text):
    return len(text.strip()) >= 3 and bool(re.search(r'[a-zA-Z0-9]', text))

# --- INPUT DE USUARIO ---
user_prompt = st.chat_input(T["input_placeholder"])

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    if not is_meaningful_input(user_prompt):
        assistant_response = T["meaningless"]
    else:
        lower_prompt = user_prompt.lower()
        if any(k in lower_prompt for k in ["proyecto", "juego", "itch.io", "arestudio", "tuyo", "tu", "mi", "mis", "vuestro", "vuestros", "vuestra", "vuestras", "creador", "estudio"]):
            projs = get_arestudio_projects()
            if projs:
                assistant_response = T["show_projects"]
            else:
                assistant_response = T["no_projects"]
        else:
            assistant_response = consultar_gemma(user_prompt) if gemma_client else T["ai_down"]

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
