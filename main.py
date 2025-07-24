import streamlit as st
from gradio_client import Client

# Configuración de la página
st.set_page_config(page_title="AREStudio AI - Asistente Multilingüe", layout="centered")
st.markdown("<h1 style='text-align: center;'>🌐 Idioma / Language / Llengua</h1>", unsafe_allow_html=True)

# Selector de idioma
idioma = st.selectbox("", ["es", "en", "ca"])

# Textos multilingües
textos = {
    "es": {
        "titulo": "AREStudio AI - Asistente Multilingüe",
        "descripcion": "🧠 Hola. Soy tu asistente de AREStudio. Puedes preguntarme sobre nuestros proyectos, IA, programación, y mucho más.",
        "input": "Escribe tu mensaje...",
        "enviar": "Enviar",
    },
    "en": {
        "titulo": "AREStudio AI - Multilingual Assistant",
        "descripcion": "🧠 Hello. I’m your AREStudio assistant. You can ask me about our projects, AI, programming, and more.",
        "input": "Type your message...",
        "enviar": "Send",
    },
    "ca": {
        "titulo": "AREStudio AI - Assistent Multilingüe",
        "descripcion": "🧠 Hola. Sóc el teu assistent d’AREStudio. Pots preguntar-me sobre els nostres projectes, IA, programació, i molt més.",
        "input": "Escriu el teu missatge...",
        "enviar": "Envia",
    }
}

# Mostrar textos en el idioma seleccionado
st.markdown(f"### {textos[idioma]['titulo']}")
st.info(textos[idioma]["descripcion"])

# Inicializar sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [{"role": "ai", "content": "Hola! ¿Qué puedo hacer por ti hoy?"}]

# Mostrar mensajes anteriores
for mensaje in st.session_state.mensajes:
    if mensaje["role"] == "user":
        st.markdown(f"**Tú:** {mensaje['content']}")
    else:
        st.markdown(f"**AREStudio AI:** {mensaje['content']}")

# Entrada del usuario
input_usuario = st.text_input(textos[idioma]["input"], key="input")

if st.button(textos[idioma]["enviar"]) and input_usuario:
    st.session_state.mensajes.append({"role": "user", "content": input_usuario})

    try:
        # Llamar a la API de Gradio (por ejemplo, Gemma-3)
        client = Client("https://gemma-3-r1984-27b-chatbot.hf.space/")
        respuesta = client.predict(
            input_usuario,
            api_name="/chat"
        )
        respuesta = respuesta.strip()

    except Exception as e:
        respuesta = "Lo siento, ha ocurrido un error al contactar con la IA."

    st.session_state.mensajes.append({"role": "ai", "content": respuesta})
    st.experimental_rerun()
