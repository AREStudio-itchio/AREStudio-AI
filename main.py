import streamlit as st
from gradio_client import Client
from bs4 import BeautifulSoup
import requests

# Interfaz traducible
st.set_page_config(page_title="AREStudio AI", layout="centered")

# Idiomas disponibles
languages = {
    "es": {
        "title": "AREStudio AI",
        "subtitle": "Asistente inteligente sobre mis proyectos",
        "input_placeholder": "Escribe tu mensaje aquí...",
        "button_label": "Enviar"
    },
    "en": {
        "title": "AREStudio AI",
        "subtitle": "Intelligent assistant about my projects",
        "input_placeholder": "Type your message here...",
        "button_label": "Send"
    },
    "ca": {
        "title": "AREStudio AI",
        "subtitle": "Assistent intel·ligent sobre els meus projectes",
        "input_placeholder": "Escriu el teu missatge aquí...",
        "button_label": "Envia"
    }
}

# Selección de idioma
lang = st.selectbox("Idioma / Language / Llengua", options=["es", "en", "ca"])
labels = languages[lang]

st.title(labels["title"])
st.subheader(labels["subtitle"])

# Conexión con Gradio Client
client = Client("VIDraft/Gemma-3-R1984-27B-Chatbot")

# Función de scraping legal
@st.cache_data(ttl=3600)
def get_itchio_projects():
    url = "https://arestudio.itch.io"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    projects = []
    for link in soup.find_all("a", class_="thumb_link"):
        href = link.get("href")
        title_tag = link.find("div", class_="game_title")
        title = title_tag.text.strip() if title_tag else "Sin título"
        if href:
            projects.append({"title": title, "url": href})

    return projects

# Mostrar proyectos si el usuario lo pide
def detect_interest(text):
    keywords = ["juegos", "proyectos", "games", "projects", "jocs"]
    return any(kw.lower() in text.lower() for kw in keywords)

# Chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input(labels["input_placeholder"])
if st.button(labels["button_label"]) and user_input.strip():
    with st.spinner("Pensando..."):
        response = client.predict(
            user_input,
            "Chat",
            0.9,
            0.95,
            2048,
            api_name="/chat"
        )

    st.session_state.chat_history.append(("👤", user_input))
    st.session_state.chat_history.append(("🤖", response))

# Mostrar historial
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}**: {msg}")

# Si el usuario muestra interés, la IA responde con los proyectos
if detect_interest(user_input):
    st.markdown("---")
    st.markdown("**🔍 Proyectos encontrados en [arestudio.itch.io](https://arestudio.itch.io):**")
    for p in get_itchio_projects():
        st.markdown(f"- [{p['title']}]({p['url']})")
