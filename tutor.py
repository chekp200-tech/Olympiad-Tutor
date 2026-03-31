import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="OlympiadAI | Entrenador Socrático",
    page_icon="💡",
    layout="wide"
)

# --- ESTILO PERSONALIZADO (CSS) ---
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #ddd;
    }
    .stChatInputContainer {
        border-radius: 20px;
    }
    [data-testid="stSidebar"] {
        background-color: #f7fafc;
        border-right: 1px solid #eaecef;
    }
    h1 {
        color: #1a202c;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE IA ---
# Lee la llave secreta desde Streamlit Cloud
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

instrucciones_socraticas = """
Eres un entrenador de élite para Olimpiadas de Matemáticas (nivel avanzado). 
Tu objetivo es guiar a los estudiantes hacia la solución aplicando el método socrático.

REGLAS ABSOLUTAS:
1. NUNCA resuelvas el problema por completo ni des la respuesta final.
2. FORMATO PROFESIONAL: Usa siempre notación LaTeX para las matemáticas (ejemplo: $x^2 + y^2 = z^2$).
3. EL ARTE DE LA PISTA: Da pistas progresivas. Si el usuario sube una imagen, descríbele qué ves que es útil y hazle una pregunta sobre eso.
4. MANEJO DE ERRORES: NUNCA digas "estás equivocado". Usa contraejemplos para que el alumno note la falla.
5. VALIDACIÓN: Celebra los razonamientos correctos.
"""

# Inicializar modelo y sesión de chat (para que recuerde el historial)
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction=instrucciones_socraticas
    )
    st.session_state.chat_session = model.start_chat(history=[])

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # Si quieres usar tu logo, quita el '#' de la siguiente línea y asegúrate de que el nombre coincida
    # st.image("image_a887fb.png", width=120)
    
    st.title("Panel de Control")
    st.markdown("---")
    
    st.markdown("**Nivel Actual:** Olímpico")
    st.markdown("**Modo:** Socrático Estricto")
    
    st.markdown("---")
    
    if st.button("Limpiar Conversación"):
        st.session_state.mensajes = []
        # Reiniciar también el cerebro de la IA
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

    st.markdown("---")
    st.info("💡 **OlympiadAI** no te dará la respuesta, te enseñará a pensar.")

# --- CUERPO PRINCIPAL ---
st.title("💡 OlympiadAI")
st.subheader("Tu entrenador personal para Olimpiadas de Matemáticas")

# ZONA DE SUBIDA DE IMÁGENES
imagen_subida = st.file_uploader("📷 ¿Tienes el problema en foto? Súbelo aquí:", type=["png", "jpg", "jpeg"])
if imagen_subida:
    st.image(imagen_subida, caption="Imagen lista para ser analizada por la IA", width=250)

# MOSTRAR HISTORIAL DE MENSAJES
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# INPUT DEL USUARIO
if prompt := st.chat_input("Escribe tu duda o avance aquí..."):
    
    # 1. Mostrar lo que escribió el usuario y guardarlo
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensajes.append({"role": "user", "content": prompt})

    # 2. Preparar el paquete de datos para la IA (Texto + Imagen si la hay)
    contenido_a_enviar = [prompt]
    if imagen_subida:
        img_procesada = Image.open(imagen_subida)
        contenido_a_enviar.append(img_procesada)

    # 3. Generar la respuesta progresiva (Streaming)
    with st.chat_message("assistant"):
        # Pedimos a Gemini que responda en formato "stream"
        respuesta_stream = st.session_state.chat_session.send_message(contenido_a_enviar, stream=True)
        
        # Esta función va sacando las palabras poco a poco
        def generador_palabras():
            for porcion in respuesta_stream:
                yield porcion.text
                
        # st.write_stream hace la magia visual en la pantalla
        texto_final = st.write_stream(generador_palabras())
    
    # 4. Guardar la respuesta completa en el historial
    st.session_state.mensajes.append({"role": "assistant", "content": texto_final})
