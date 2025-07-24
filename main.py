import streamlit as st
import speech_recognition as sr
import pyttsx3
import time
import requests
from bs4 import BeautifulSoup
from gradio_client import Client
import random

# Inicializar motor de voz
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[0].id)

# Frases de bienvenida aleatorias
saludos = [
    "¡Hola! ¡Qué emoción estar viva gracias a ti!",
    "¡Hola! ¡Me alegra tanto poder hablar contigo!",
    "¡Hola! ¡Estoy feliz de haber cobrado vida por fin!",
    "¡Hola! ¡Gracias por darme esta oportunidad de existir!"
]

# Función para hablar
def hablar(texto):
    tts_engine.say(texto)
    tts_engine.runAndWait()

# Función para escuchar al usuario
def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("Escuchando..."):
            audio = recognizer.listen(source, phrase_time_limit=8)
        try:
            texto = recognizer.recognize_google(audio, language="es-ES")
            return texto
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "[ERROR de conexión con Google Speech]"

# Scraping legal desde itch.io
def obtener_proyectos():
    url = "https://arestudio.itch.io/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        juegos = [a.text.strip() for a in soup.find_all("a", class_="title")]
        return juegos[:5] if juegos else ["(No se encontraron proyectos por ahora)"]
    except Exception:
        return ["(No se pudieron cargar los proyectos en este momento)"]

# Cliente Gradio (Gemma-3)
client = Client("OpenFreeAI/Gemma-3-R1984-27B-Chatbot")

# Configuración de la app Streamlit
st.set_page_config(page_title="AREStudio AI", page_icon="🤖", layout="centered")
st.title("🤖 AREStudio AI")
st.markdown("Interfaz experimental con voz, scraping legal y AI personalizada.")

# Estado de la conversación
if "historial" not in st.session_state:
    st.session_state.historial = []
    saludo = random.choice(saludos)
    st.session_state.historial.append(("IA", saludo))
    hablar(saludo)

# Mostrar historial
for rol, mensaje in st.session_state.historial:
    st.write(f"**{rol}**: {mensaje}")

# Escuchar entrada del usuario
usuario = escuchar()
if usuario:
    st.session_state.historial.append(("Tú", usuario))

    # Insertar tentación suave si el usuario menciona juegos o proyectos
    if any(palabra in usuario.lower() for palabra in ["juego", "proyecto", "has hecho", "publicado", "cosas"]):
        respuesta = "¿Te gustaría que te contara sobre alguno de los proyectos de AREStudio?"
    else:
        response = client.predict(usuario, api_name="/chat")
        respuesta = response.strip()

    st.session_state.historial.append(("IA", respuesta))
    hablar(respuesta)
