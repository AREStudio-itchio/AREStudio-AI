import streamlit as st
from gradio_client import Client
import threading

# Inicializar el cliente de Gradio
client = Client("VIDraft/Gemma-3-R1984-27B", api_name="/chat")

# Función para procesar la respuesta de la IA en segundo plano
def procesar_respuesta(prompt):
    try:
        response = client.predict(message={"text": prompt}, max_new_tokens=600)
        st.session_state.hist_assist.append(response.strip())
    except Exception as e:
        st.session_state.hist_assist.append(f"⚠️ Error al contactar con la IA: {e}")

# Configuración de la página
st.set_page_config(page_title="AREStudio AI", page_icon="🤖")

# Inicializar el historial si no existe
if "hist_user" not in st.session_state:
    st.session_state.hist_user = []
    st.session_state.hist_assist = []

# Mostrar el historial de la conversación
for u, a in zip(st.session_state.hist_user, st.session_state.hist_assist):
    with st.chat_message("user"):
        st.markdown(u)
    with st.chat_message("assistant"):
        st.markdown(a)

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Mostrar el mensaje del usuario inmediatamente
    st.session_state.hist_user.append(user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir el prompt para la IA
    prompt = "\n".join(st.session_state.hist_user) + "\n\nAssistant:\n"

    # Procesar la respuesta de la IA en segundo plano
    threading.Thread(target=procesar_respuesta, args=(prompt,)).start()

    # Mostrar un mensaje de espera
    with st.chat_message("assistant"):
        st.markdown("Pensando...")

    # Mostrar la respuesta de la IA una vez procesada
    if st.session_state.hist_assist:
        with st.chat_message("assistant"):
            st.markdown(st.session_state.hist_assist[-1])
