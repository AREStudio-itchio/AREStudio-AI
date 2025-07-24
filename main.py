import streamlit as st
import requests
from bs4 import BeautifulSoup
from gradio_client import Client
import random
import re # Importar re para validación de entrada

# --- CONFIGURACIÓN DEL MODELO GEMMA-3 (Hugging Face Space) ---
# ID del Space de Hugging Face donde está el modelo Gemma
GEMMA_MODEL_SPACE_ID = "VIDraft/Gemma-3-R1984-27B"
# Punto de la API dentro del Space para el chat
GEMMA_API_ENDPOINT = "/chat"
# Máximo número de tokens que la IA puede generar en una respuesta
MAX_NEW_TOKENS = 1000
# Desactiva la búsqueda web por parte de la IA (si el modelo lo soporta)
USE_WEB_SEARCH = False
# Desactiva el uso de coreano (si el modelo lo soporta)
USE_KOREAN = False

# Define el límite de pares de mensajes (pregunta/respuesta) para el historial
# Esto ayuda a controlar el tamaño del contexto enviado a la IA y a evitar errores 422
# 5 pares = 5 preguntas del usuario + 5 respuestas de la IA = 10 mensajes en total
MAX_HISTORY_PAIRS = 5 

# --- FUNCIÓN PARA SCRAPING LEGAL DE PROYECTOS DE ITCH.IO ---
# La caché de Streamlit guarda los resultados durante 3600 segundos (1 hora)
# para evitar hacer peticiones constantes a itch.io
@st.cache_data(ttl=3600)
def get_arestudio_projects():
    url = "https://arestudio.itch.io"
    # Cabeceras para identificar la petición como un bot de AREStudio
    headers = {"User-Agent": "AREStudioBot/1.0"}
    try:
        # Realiza la petición GET a la URL
        resp = requests.get(url, headers=headers, timeout=10)
        # Lanza una excepción si la petición HTTP no fue exitosa (ej. 404, 500)
        resp.raise_for_status()
        # Parsea el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        projs = []
        # Busca todos los enlaces de proyectos de juegos en la página
        for a in soup.select("a.title.game_link"):
            title = a.text.strip() # Extrae el título del juego
            link = a.get("href")    # Extrae el enlace del juego
            if title and link:
                projs.append({"title": title, "url": link})
        return projs
    except Exception as e:
        # Si ocurre un error (ej. de red, timeout), muestra una advertencia en la UI
        st.warning(f"No he podido obtener los proyectos de itch.io en este momento. Error: {e}")
        return []

# --- CLIENTE GRADIO PARA CONECTARSE AL MODELO GEMMA-3 ---
# st.cache_resource asegura que el cliente se inicialice solo una vez por sesión
@st.cache_resource
def get_gemma_client():
    # Crea una instancia del cliente Gradio para el Space especificado
    return Client(GEMMA_MODEL_SPACE_ID)

# Inicializa el cliente Gradio al inicio de la aplicación
gemma_client = get_gemma_client()

# --- FUNCIÓN PARA CONSULTAR LA IA (GEMMA-3) ---
def consultar_gemma(user_prompt, chat_history):
    # Formatea el historial de chat para el cliente Gradio.
    # El cliente Gradio espera una lista de listas: [[pregunta_usuario, respuesta_ia], ...]
    
    formatted_chat_history = []
    # Itera sobre el historial de mensajes de Streamlit (st.session_state.messages)
    # y los convierte al formato que Gradio espera.
    # Empezamos desde el índice 1 para omitir el mensaje de bienvenida inicial del bot.
    # Asumimos que los mensajes se alternan entre usuario y asistente.
    for i in range(len(chat_history)):
        if chat_history[i]["role"] == "user":
            if i + 1 < len(chat_history) and chat_history[i+1]["role"] == "assistant":
                # Si hay un par completo (usuario y asistente)
                formatted_chat_history.append([chat_history[i]["content"], chat_history[i+1]["content"]])
            # else:
                # Si el último mensaje es del usuario y aún no hay respuesta del asistente,
                # se añade la pregunta del usuario y una cadena vacía para la respuesta.
                # Esto es importante para que la IA tenga el último prompt en su historial.
                # formatted_chat_history.append([chat_history[i]["content"], ""])

    # Limita el historial a los últimos MAX_HISTORY_PAIRS definidos
    limited_history = formatted_chat_history[-MAX_HISTORY_PAIRS:]

    try:
        # Realiza la predicción usando el cliente Gradio.
        # 'message' se pasa como string directo, 'history' como la lista de listas formateada.
        resp = gemma_client.predict(
            message=user_prompt, # El prompt del usuario actual
            history=limited_history, # El historial de la conversación limitada
            max_new_tokens=MAX_NEW_TOKENS,
            use_web_search=USE_WEB_SEARCH,
            use_korean=USE_KOREAN,
            api_name=GEMMA_API_ENDPOINT
        )
        # La respuesta puede venir como string o como una tupla/lista (toma el primer elemento si es así)
        return resp if isinstance(resp, str) else resp[0]
    except Exception as e:
        # Captura cualquier error durante la consulta a la IA y lo muestra en la UI
        st.error(f"⚠️ ¡Error de red o conexión con la IA! Por favor, inténtalo de nuevo. Detalles: {e}")
        return "Lo siento, hubo un problema al consultar la IA en este momento."

# --- CONFIGURACIÓN DE LA INTERFAZ DE STREAMLIT ---
st.set_page_config(page_icon="🤖", page_title="AREStudio AI")

# Inicializa el historial de chat en st.session_state si no existe
# st.session_state.messages guarda una lista de diccionarios: [{"role": "user/assistant", "content": "mensaje"}]
if "messages" not in st.session_state:
    st.session_state.messages = []

# Lógica para el saludo inicial de la IA
if "init_greeting_done" not in st.session_state:
    st.session_state.init_greeting_done = True
    saludo = random.choice([
        "¡Hola! Soy AREStudio AI, un asistente creado por AREStudio. ¿En qué puedo ayudarte hoy?",
        "¡Hola! Soy AREStudio AI. Estoy aquí para ayudarte con cualquier consulta sobre AREStudio o si tienes alguna pregunta general.",
        "¡Saludos! Soy AREStudio AI, tu asistente de AREStudio. ¿Cómo puedo asistirte hoy?"
    ])
    # Añade el saludo inicial al historial de mensajes de la IA
    st.session_state.messages.append({"role": "assistant", "content": saludo})

# Muestra todos los mensajes del historial en la interfaz de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- VALIDACIÓN BÁSICA DE ENTRADA DEL USUARIO ---
# Evita enviar entradas sin sentido o muy cortas a la IA
def is_meaningful_input(text):
    # Requiere al menos 3 caracteres no espaciales y que contenga al menos un carácter alfanumérico
    return len(text.strip()) >= 3 and bool(re.search(r'[a-zA-Z0-9]', text))

# Campo de entrada de texto para el usuario
user_prompt = st.chat_input("Escribe tu pregunta aquí...")

# Procesa la entrada del usuario si hay un prompt
if user_prompt:
    # Añade el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Muestra el mensaje del usuario en la interfaz inmediatamente
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Verifica si la entrada del usuario es significativa
    if not is_meaningful_input(user_prompt):
        assistant_response = "Lo siento, parece que no entendí eso. Por favor, haz una pregunta clara y con más detalles."
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        lower_prompt = user_prompt.lower()
        # --- LÓGICA DE PROMOCIÓN CONDICIONAL DE ARESTUDIO ---
        # La IA solo promociona si el usuario menciona AREStudio o temas relacionados,
        # y luego pregunta si quiere ver los proyectos en lugar de listarlos directamente.
        if any(k in lower_prompt for k in ["proyecto", "juego", "itch.io", "arestudio", "tuyo", "tu", "mi", "mis", "vuestro", "vuestros", "vuestra", "vuestras", "creador", "estudio"]):
            # Si el usuario pregunta por AREStudio o sus proyectos, intenta obtenerlos
            projs = get_arestudio_projects()
            if projs:
                response_text = "¡Claro! AREStudio tiene varios proyectos interesantes. ¿Te gustaría que te liste algunos o te dé el enlace a nuestra página de itch.io para que los veas todos?"
            else:
                response_text = "Lo siento, no he podido obtener los proyectos de AREStudio en este momento. Puede que haya un problema con la conexión a la página."
            
            with st.chat_message("assistant"):
                st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            # Si la pregunta no es sobre AREStudio, consulta a la IA con el historial completo
            respuesta_gemma = consultar_gemma(user_prompt, st.session_state.messages) # Pasa el historial completo
            with st.chat_message("assistant"):
                st.markdown(respuesta_gemma)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_gemma})

