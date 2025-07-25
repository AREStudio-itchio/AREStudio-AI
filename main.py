import streamlit as st
from gradio_client import Client
import traceback

st.set_page_config(
    page_title="AREStudio AI",
    page_icon="https://img.itch.zone/aW1nLzIyMjkyNTc3LnBuZw==/315x250%23c/CeYE7v.png",
    layout="centered"
)

client = Client("VIDraft/Gemma-3-R1984-27B")

prompt_base_template = """
Eres AREStudio AI, un asistente amable, respetuoso y responsable. Siempre respondes en el idioma en que el usuario escribe. No generas contenido inapropiado ni dañino y cambias de tema si te piden eso. Responde con alegría y educación.
No confundas y hables otro idioma que no sea el usuario, intenta hablar siempre en el idioma manteniéndolo en la conversación.
No mezcles otros idiomas si el usuario no habla en ellos.
No puedes buscar en google o tener info actualizada, puedes tenerla desactualizada, si tienes problemas en lo que necesite el usuario, que te explique o te de un texto para saber la info detallada y actualizada.
Intenta memorizar el chat por si necesitas recordar algún mensaje anterior.
Intenta no tener faltas de ortografía.
Usuario: {user_input}
Asistente:
"""

if "historial" not in st.session_state:
    st.session_state.historial = []

st.title("🤖 AREStudio AI")
st.markdown("Tu asistente conversacional amable, respetuoso y responsable.")

# Saludo inicial si no hay mensajes
if len(st.session_state.historial) == 0:
    saludo = "¡Hola! ¿En qué puedo ayudarte hoy?"
    st.session_state.historial.append({"role": "assistant", "content": saludo})

for msg in st.session_state.historial:
    role = msg["role"]
    content = msg["content"]
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
    except Exception as e:
        error_text = traceback.format_exc()
        st.error(f"⚠️ Error al contactar con AREStudio AI:\n{error_text}")
        st.session_state.historial.append({"role": "assistant", "content": "⚠️ Error al contactar con AREStudio AI."})
