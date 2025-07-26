import streamlit as st
from gradio_client import Client, handle_file

# Inicializa el cliente de Gradio
client = Client("VIDraft/Gemma-3-R1984-27B", api_name="/chat")

# Título de la aplicación
st.title("Chat con Gemma-3")

# Inicializa el estado de la sesión si es la primera vez que se ejecuta
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy?"}]

# Muestra los mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Muestra el mensaje del usuario
    st.chat_message("user").markdown(prompt)

    # Añade el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepara los datos para la predicción
    inputs = {"text": prompt}
    if uploaded_file := st.file_uploader("Sube una imagen (opcional):", type=["jpg", "png"]):
        inputs["files"] = [handle_file(uploaded_file)]

    # Realiza la predicción
    with st.spinner("Pensando..."):
        try:
            response = client.predict(inputs, max_new_tokens=1000, use_web_search=False, use_korean=False)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").markdown(response)
        except Exception as e:
            st.error(f"Error al contactar con la IA: {e}")
