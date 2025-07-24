import streamlit as st
from gradio_client import Client

# Estilo de la UI
st.set_page_config(page_title="AREStudio AI - Asistente Multilingüe")
st.title("🌐 Idioma / Language / Llengua")
idioma = st.selectbox("", ["es", "en", "ca"])

st.markdown("### AREStudio AI - Asistente Multilingüe")
st.markdown("""
🧠 Hola. Soy tu asistente de AREStudio. Puedes preguntarme sobre nuestros proyectos, IA, programación, y mucho más.
""")

# Instrucciones en cada idioma
if idioma == "es":
    saludo = "¡Hola! Soy AREStudio AI. Estoy aquí para ayudarte con cualquier consulta sobre AREStudio o si tienes alguna pregunta general."
elif idioma == "en":
    saludo = "Hi! I'm AREStudio AI. I'm here to help you with anything related to AREStudio or general questions."
else:
    saludo = "Hola! Sóc AREStudio AI. Sóc aquí per ajudar-te amb qualsevol dubte sobre AREStudio o preguntes generals."

st.info(saludo)

# Función para conectar con la API (modifica el espacio si cambias de modelo)
def consultar_IA(pregunta):
    client = Client("OpenFreeAI/Gemma-3-R1984-27B")
    respuesta = client.predict(
        pregunta,         # texto
        api_name="/chat"  # usa el endpoint correcto de tu Space
    )
    return respuesta

# Interfaz del chat
if "historial" not in st.session_state:
    st.session_state.historial = []

# Entrada del usuario
user_input = st.text_input("¿Qué quieres preguntar?", key="input")

if st.button("Enviar"):
    if user_input:
        st.session_state.historial.append(("Tú", user_input))
        with st.spinner("Pensando..."):
            respuesta = consultar_IA(user_input)
        st.session_state.historial.append(("AREStudio AI", respuesta))

# Mostrar conversación
for rol, texto in st.session_state.historial:
    if rol == "Tú":
        st.markdown(f"**🧑‍💻 {rol}:** {texto}")
    else:
        st.markdown(f"**🤖 {rol}:** {texto}")
