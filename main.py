import streamlit as st
from gradio_client import Client, handle_file

# Selección de idioma para la UI
lang = st.sidebar.selectbox("🌐 Idioma / Language / Llengua", ["Español", "Català", "English"])

texts = {
    "Español": {
        "title": "AREStudio AI",
        "subtitle": "Tu asistente inteligente multilingüe",
        "input": "Escribe tu mensaje aquí...",
        "send": "Enviar",
        "thinking": "Pensando...",
    },
    "Català": {
        "title": "AREStudio AI",
        "subtitle": "El teu assistent intel·ligent multilingüe",
        "input": "Escriu el teu missatge aquí...",
        "send": "Envia",
        "thinking": "Pensa...",
    },
    "English": {
        "title": "AREStudio AI",
        "subtitle": "Your multilingual smart assistant",
        "input": "Type your message here...",
        "send": "Send",
        "thinking": "Thinking...",
    }
}

st.title(texts[lang]["title"])
st.caption(texts[lang]["subtitle"])

# Inicializamos cliente Gradio para Gemma-3
client = Client("VIDraft/Gemma-3-R1984-27B")

if "history" not in st.session_state:
    st.session_state.history = []

# Mostrar mensajes previos tipo chat
for entry in st.session_state.history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

# Entrada usuario
user_input = st.chat_input(texts[lang]["input"])

if user_input:
    # Agregamos mensaje usuario a historial
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown(f"⏳ {texts[lang]['thinking']}")
        try:
            response = client.predict(
                message={"text": user_input, "files": []},
                max_new_tokens=1000,
                use_web_search=False,
                use_korean=False,
                api_name="/chat"
            )
        except Exception as e:
            response = f"⚠️ Error: {e}"
        placeholder.markdown(response)
        st.session_state.history.append({"role": "assistant", "content": response})
