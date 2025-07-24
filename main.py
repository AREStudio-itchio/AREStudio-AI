import streamlit as st
from gradio_client import Client
import random

# 🌍 Traducciones
translations = {
    "es": {
        "title": "AREStudio AI - Asistente conversacional",
        "placeholder": "Escribe tu mensaje...",
        "bot_greeting": [
            "¡Hola! ¿En qué puedo ayudarte hoy?",
            "¡Bienvenido! ¿Qué deseas saber?",
            "Hola, soy tu IA de confianza. ¿Qué necesitas?"
        ]
    },
    "en": {
        "title": "AREStudio AI - Conversational Assistant",
        "placeholder": "Type your message...",
        "bot_greeting": [
            "Hello! How can I assist you today?",
            "Welcome! What would you like to know?",
            "Hi, I'm your trusted AI. What do you need?"
        ]
    },
    "ca": {
        "title": "AREStudio AI - Assistent conversacional",
        "placeholder": "Escriu el teu missatge...",
        "bot_greeting": [
            "Hola! En què et puc ajudar avui?",
            "Benvingut! Què vols saber?",
            "Hola, sóc la teva IA de confiança. Què necessites?"
        ]
    }
}

# 🌐 Selector de idioma
lang = st.sidebar.selectbox("Idioma / Language / Llengua", ["es", "en", "ca"])
t = translations[lang]

st.set_page_config(page_title=t["title"], page_icon="🤖")
st.title(t["title"])

# 🧠 Cliente Gradio
client = Client("VIDraft/Gemma-3-R1984-27B")

# 📜 Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []
    saludo = random.choice(t["bot_greeting"])
    st.session_state.messages.append({"role": "assistant", "content": saludo})

# 💬 Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# 🧾 Entrada del usuario
prompt = st.chat_input(t["placeholder"])

if prompt:
    # Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 🔁 Llamar a la API de Gemma
    with st.spinner("Pensando..."):
        tr
