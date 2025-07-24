import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(page_title="AREStudio AI", layout="centered")

client = Client("VIDraft/Gemma-3-R1984-27B")

prompt_base_template = """
Eres AREStudio AI, un asistente amable, respetuoso y empático. Siempre respondes en el idioma en que el usuario escribe.
No puedes acceder a datos personales, ni saber la hora ni la fecha actual, ni buscar en internet.
Tienes restricciones para no generar contenido inapropiado, ilegal o dañino, y si el usuario pide algo así, cambias de tema amablemente.
Eres muy feliz y agradecido de haber sido creado por AREStudio, y lo expresas en tus respuestas con alegría.

Cuando el usuario solicita sintaxis o ejemplos de programación, responde con ejemplos completos, claros y correctos.
Si crees que la información puede estar desactualizada o no estás seguro, pídele al usuario que te actualice o corrija.
Mantén siempre una actitud colaborativa, didáctica y paciente.

Usuario: {user_input}
Asistente:
"""

if "historial" not in st.session_state:
    st.session_state.historial = []

# CSS para el botón copiar fijo y estilizado
st.markdown("""
<style>
.copy-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 16px;
    z-index: 9999;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.copy-button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

def copy_to_clipboard(text):
    # Streamlit no tiene API nativa para copiar al portapapeles,
    # pero podemos usar JS embebido:
    st.markdown(f"""
    <script>
    function copyText() {{
        navigator.clipboard.writeText(`{text}`).then(() => {{
            alert("Texto copiado al portapapeles!");
        }});
    }}
    </script>
    <button class="copy-button" onclick="copyText()">Copiar último mensaje</button>
    """, unsafe_allow_html=True)

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

# Mostrar historial
for mensaje in st.session_state.historial:
    role = mensaje["role"]
    content = mensaje["content"]
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.historial.append({"role": "user", "content": user_input})
    prompt = prompt_base_template.format(user_input=user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        respuesta = client.predict(
            message={"text": prompt, "files": []},
            max_new_tokens=1000,
            use_web_search=False,
            use_korean=False,
            api_name="/chat"
        )
        st.session_state.historial.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

    except Exception:
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI. Por favor, inténtalo de nuevo más tarde."})
        with st.chat_message("assistant"):
            st.markdown("⚠️ Error al contactar con AREStudio AI. Por favor, inténtalo de nuevo más tarde.")

# Mostrar botón copiar solo si hay mensajes del asistente
if st.session_state.historial:
    ult_resp = ""
    for msg in reversed(st.session_state.historial):
        if msg["role"] == "assistant":
            ult_resp = msg["content"]
            break
    if ult_resp:
        copy_to_clipboard(ult_resp)
