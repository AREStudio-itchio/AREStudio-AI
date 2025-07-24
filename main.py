import streamlit as st
from gradio_client import Client
import requests
from bs4 import BeautifulSoup

# ===== MULTILINGÜE =====
lang = st.sidebar.selectbox("🌐 Idioma / Language / Llengua", ["Español", "English", "Català"])

texts = {
    "Español": {
        "title": "AREStudio AI",
        "subtitle": "Tu asistente inteligente multilingüe",
        "input": "Escribe tu mensaje aquí:",
        "send": "Enviar",
        "output": "Respuesta de la IA:"
    },
    "English": {
        "title": "AREStudio AI",
        "subtitle": "Your multilingual smart assistant",
        "input": "Type your message here:",
        "send": "Send",
        "output": "AI Response:"
    },
    "Català": {
        "title": "AREStudio AI",
        "subtitle": "El teu assistent intel·ligent multilingüe",
        "input": "Escriu el teu missatge aquí:",
        "send": "Envia",
        "output": "Resposta de la IA:"
    }
}

# ===== TÍTULO Y SUBTÍTULO =====
st.title(texts[lang]["title"])
st.subheader(texts[lang]["subtitle"])

# ===== SCRAPING LEGAL A AREStudio.itch.io =====
def get_arestudio_projects():
    url = "https://arestudio.itch.io"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = [a.text for a in soup.find_all("div", class_="game_title")]
    return titles

with st.expander("🎮 Proyectos públicos en AREStudio.itch.io"):
    for title in get_arestudio_projects():
        st.markdown(f"- {title}")

# ===== GRADIO CLIENT CON GEMMA-3 SIN TOKEN =====
try:
    client = Client("VIDraft/Gemma-3-R1984-27B")
    msg = st.text_input(texts[lang]["input"])
    if st.button(texts[lang]["send"]) and msg:
        with st.spinner("Pensando..."):
            result = client.predict(
                msg,
                api_name="/chat"
            )
            st.success(texts[lang]["output"])
            st.markdown(result)
except Exception as e:
    st.error("⚠️ Error al conectar con el modelo Gemma-3.")
    st.code(str(e))
