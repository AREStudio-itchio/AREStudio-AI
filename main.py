import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
import time
from gradio_client import Client
import random

# ==== Idiomas disponibles ====
idiomas = {"es": "Español", "en": "English", "ca": "Català"}
st.set_page_config(page_title="AREStudio AI - Asistente Multilingüe", layout="centered")

# ==== Selección de idioma UI ====
lang = st.selectbox("🌐 Idioma / Language / Llengua", list(idiomas.keys()), format_func=lambda x: idiomas[x])

# ==== Traducción del texto según idioma ====
def t(text):
    traducciones = {
        "title": {
            "es": "AREStudio AI - Asistente Multilingüe",
            "en": "AREStudio AI - Multilingual Assistant",
            "ca": "AREStudio AI - Assistent Multilingüe",
        },
        "intro": {
            "es": "🧠 Hola. Soy tu asistente de AREStudio. Puedes preguntarme sobre nuestros proyectos, IA, programación, y mucho más.",
            "en": "🧠 Hello. I'm your AREStudio assistant. You can ask me about our projects, AI, programming, and more.",
            "ca": "🧠 Hola. Soc el teu assistent d'AREStudio. Pots preguntar-me sobre els nostres projectes, IA, programació i molt més.",
        },
        "start": {
            "es": "Haz clic en el botón para comenzar a hablar 🎤",
            "en": "Click the button to start speaking 🎤",
            "ca": "Fes clic al botó per començar a parlar 🎤",
        },
        "listen": {
            "es": "Escuchando...",
            "en": "Listening...",
            "ca": "Escoltant...",
        },
        "waiting": {
            "es": "Esperando tu voz...",
            "en": "Waiting for your voice...",
            "ca": "Esperant la teva veu...",
        },
        "no_voice": {
            "es": "No se detectó voz.",
            "en": "No voice detected.",
            "ca": "No s'ha detectat cap veu.",
        },
    }
    return traducciones[text][lang]

st.title(t("title"))
st.write(t("intro"))

# ==== Motor de voz ====
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

# ==== Cliente Gradio ====
client = Client("OpenFreeAI/Gemma-3-R1984-27B")

# ==== Saludos iniciales aleatorios ====
saludos = {
    "es": [
        "¡Hola! ¿Cómo puedo ayudarte hoy?",
        "Bienvenido a AREStudio AI. ¿Qué deseas saber?",
        "Estoy listo para ayudarte con tus preguntas.",
    ],
    "en": [
        "Hi! How can I help you today?",
        "Welcome to AREStudio AI. What would you like to know?",
        "I'm here and ready to assist you.",
    ],
    "ca": [
        "Hola! Com puc ajudar-te avui?",
        "Benvingut a AREStudio AI. Què vols saber?",
        "Estic aquí per ajudar-te.",
    ]
}

# ==== Reconocimiento de voz ====
reconocedor = sr.Recognizer()

def escuchar():
    with sr.Microphone() as source:
        st.write(t("listen"))
        audio = reconocedor.listen(source, timeout=5, phrase_time_limit=10)
    try:
        texto = reconocedor.recognize_google(audio, language=lang)
        return texto
    except:
        return None

# ==== Conversación IA ====
def responder(prompt_usuario):
    response = client.predict(prompt_usuario, api_name="/chat")
    return response

# ==== Conversación completa ====
if st.button(t("start")):
    saludo = random.choice(saludos[lang])
    st.write("🤖 " + saludo)
    hablar(saludo)

    while True:
        st.write("🎤 " + t("waiting"))
        entrada = escuchar()
        if entrada:
            st.write("🗣️ Tú: " + entrada)
            respuesta = responder(entrada)
            st.write("🤖 " + respuesta)
            hablar(respuesta)
        else:
            st.warning(t("no_voice"))
        time.sleep(1)
