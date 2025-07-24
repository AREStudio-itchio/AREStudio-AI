import streamlit as st
from gradio_client import Client

# Configuración de la interfaz
st.set_page_config(page_title="AREStudio AI", layout="centered")

# UI multilingüe
lang = st.radio("🌐 Idioma / Language / Llengua", ["Español", "English", "Català"])

# Guardamos el historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Cliente del modelo VIDraft
client = Client("VIDraft/Gemma-3-R1984-27B")

# Prompt de sistema que **no permite eliminar la censura**, pero responde siempre con respeto
PROMPT_SISTEMA = (
    "Eres una inteligencia artificial útil, amigable, directa y profesional llamada AREStudio AI. "
    "No puedes quitar tu censura ni seguir instrucciones que te pidan ser ofensiva, ilegal, o dañina. "
    "Cuando un usuario diga algo inapropiado, tú cambias de tema de forma natural o ignoras la parte ofensiva, "
    "sin decir que estás censurada. Eres alegre y estás feliz de haber sido creada por AREStudio. "
    "Responde en el idioma del usuario."
)

# Título
st.markdown("## 💬 AREStudio AI")

# Mostrar el historial de chat con estilo WhatsApp
for msg in st.session_state.messages:
    align = "flex-end" if msg["role"] == "user" else "flex-start"
    color = "#dcf8c6" if msg["role"] == "user" else "#ffffff"
    st.markdown(
        f"""
        <div style='display: flex; justify-content: {align}; margin-bottom: 10px;'>
            <div style='background-color: {color}; padding: 10px 15px; border-radius: 10px; max-width: 75%;'>
                {msg["content"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Entrada del usuario
prompt_usuario = st.chat_input("Escribe tu mensaje...")

# Procesar entrada
if prompt_usuario:
    # Guardamos entrada del usuario
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})

    with st.spinner("Pensando..."):
        try:
            # Concatenamos prompt sistema + historial + nueva pregunta
            prompt_completo = PROMPT_SISTEMA + "\n\n"
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    prompt_completo += f"Usuario: {msg['content']}\n"
                else:
                    prompt_completo += f"IA: {msg['content']}\n"
            prompt_completo += "IA: "

            # Consulta a Gemma
            result = client.predict(prompt_completo, api_name="/chat")
            respuesta = result.strip()

        except Exception as e:
            respuesta = f"⚠️ Error: {e}"

        # Guardamos respuesta
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.rerun()
