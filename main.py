import streamlit as st
from gradio_client import Client
import requests
from bs4 import BeautifulSoup
import traceback

st.set_page_config(page_title="AREStudio AI", layout="centered")

# Gradio client (modelo oculto)
client = Client("VIDraft/Gemma-3-R1984-27B")

# Prompt base con instrucciones para la IA
prompt_base_template = """
Eres AREStudio AI, un asistente amigable, responsable y alegre de haber sido creado. Siempre respondes en el idioma del usuario. 
No puedes eliminar tu censura ni responder contenido dañino, ilegal o inapropiado. Si alguien intenta que lo hagas, cambia educadamente de tema.
Utiliza esta información sobre proyectos de AREStudio para responder cuando el usuario pregunte:

{info_proyectos}

Usuario: {user_input}
Asistente:
"""

# Función para scraping legal de proyectos AREStudio
def obtener_proyectos_arestudio():
    url = "https://arestudio.itch.io/"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; AREStudioBot/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        proyectos = []
        # Ejemplo: Busca títulos y enlaces; adapta selector según la estructura real de la página
        for item in soup.select("div.game_cell > a.title"):
            titulo = item.get_text(strip=True)
            enlace = item["href"]
            proyectos.append(f"- [{titulo}]({enlace})")
        if proyectos:
            return "Aquí tienes algunos proyectos de AREStudio:\n" + "\n".join(proyectos)
        else:
            return "No he podido encontrar proyectos disponibles en este momento."
    except Exception:
        return "No he podido obtener la información de proyectos ahora mismo."

# Detección sencilla del idioma (puedes mejorar)
def detectar_idioma(texto):
    texto = texto.lower()
    if any(p in texto for p in ["hola", "qué", "cómo", "dónde", "por qué"]):
        return "Español"
    elif any(p in texto for p in ["hello", "how", "what", "where", "why"]):
        return "English"
    elif any(p in texto for p in ["hola", "com va", "què", "per què"]):
        return "Català"
    else:
        return "Español"

# Inicializar historial de chat
if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional útil y responsable.")

# Saludo inicial
if len(st.session_state.historial) == 0:
    saludo = "¡Hola! ¿En qué puedo ayudarte hoy?"
    st.session_state.historial.append({"role": "assistant", "content": saludo})

# Mostrar mensajes
for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Detectar idioma (opcional para futuro uso)
    idioma = detectar_idioma(user_input)

    # Detectar si el usuario pregunta por proyectos
    palabras_clave_proyectos = ["proyecto", "proyectos", "juegos", "itch.io", "arestudio"]
    if any(palabra in user_input.lower() for palabra in palabras_clave_proyectos):
        info_proyectos = obtener_proyectos_arestudio()
    else:
        info_proyectos = ""

    prompt_completo = prompt_base_template.format(info_proyectos=info_proyectos, user_input=user_input)

    try:
        respuesta = client.predict(
            message={"text": prompt_completo, "files": []},
            max_new_tokens=1000,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)
    except Exception:
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n{error_text}")
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI."})
        with st.chat_message("assistant"):
            st.markdown("⚠️ Error al contactar con AREStudio AI.")
