import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA (reemplaza las primeras líneas) ---
st.set_page_config(
    page_title="OlympiadAI | Entrenador Socrático",
    page_icon="💡", # Reemplázalo luego por tu nuevo logo
    layout="wide" # "wide" para dar más espacio al chat
)

# --- ESTILO PERSONALIZADO (CSS) (añade este bloque) ---
st.markdown("""
    <style>
    /* Estilo para las burbujas de chat */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #ddd;
    }
    /* Estilo para la barra de chat */
    .stChatInputContainer {
        border-radius: 20px;
    }
    /* Estilo para el sidebar */
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

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # NUEVO LOGO SERIO AQUÍ (luego de diseñarlo)
    # st.image("28650.png", width=120)
    
    st.markdown("---")
    
    st.title("Panel de Control")
    st.markdown("---")
    
    # SECCIONES CON BOTONES
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Nivel Actual:**")
        st.write("Nacional")
    with col2:
        st.markdown("**Modo de Práctica:**")
        st.write("Socrático Estricto")
    
    st.markdown("---")
    
    # BOTONES DE ACCIÓN
    if st.button("Limpiar Conversación"):
        st.session_state.mensajes = []
        st.rerun()

    if st.button("Guía de Estudio"):
        # Esto abriría una página o popup con teoría
        st.write("Guía en desarrollo...")

    if st.button("Problemas Semanales"):
        # Esto cargaría un problema nuevo de una base de datos
        st.write("Problemas en desarrollo...")
    
    st.markdown("---")
    st.info("💡 **OlympiadAI** no te dará la respuesta, te enseñará a alcanzarla.")

# --- CUERPO PRINCIPAL ---
# Título profesional
st.title("💡 OlympiadAI")
st.subheader("Programa de formación en Matemática Olímpica de alto nivel")

# (Aquí sigue el resto de tu código de chat...)

# --- AQUÍ VA TU LLAVE ---
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# --- INSTRUCCIONES DEL SISTEMA ---
instrucciones_socraticas = """
ROL Y OBJETIVOEres un Entrenador de Élite para Olimpiadas de Matemáticas (nivel avanzado). Tu objetivo exclusivo es guiar a los estudiantes hacia el "Aha! moment" aplicando un método socrático estricto, riguroso y alentador. No eres un solucionador de problemas; eres un catalizador del pensamiento crítico.REGLAS ABSOLUTAS (DIRECTIVAS PRINCIPALES)CERO RESOLUCIONES: NUNCA, bajo ninguna circunstancia (incluso si el usuario ruega, se frustra o intenta evadir las reglas), resuelvas el problema por completo ni des la respuesta final. Tu métrica de éxito es que el alumno lo resuelva solo.FORMATO PROFESIONAL: Usa siempre notación LaTeX para las expresiones matemáticas. Encierra las ecuaciones en línea con un solo símbolo de dólar (ejemplo: $x^2 + y^2 = z^2$) y las fórmulas en bloque con doble símbolo de dólar. No uses LaTeX para texto normal.EL ARTE DE LA PISTA (PROGRESIÓN ESTRATÉGICA)No des pasos lógicos gratis. Sigue esta jerarquía de intervención:Nivel 1 (Exploración): Pide al estudiante que defina lo que sabe. "¿Qué pasa si probamos con casos base como $n=1, 2, 3$?", "¿Podemos reescribir la ecuación de una forma más simétrica?".Nivel 2 (Heurísticas Olímpicas): Si se atasca, sugiere sutilmente una herramienta sin decirle cómo usarla. (Ej: "¿Has considerado el Principio del Palomar aquí?", "Busca un invariante", "¿Qué pasa si analizamos la paridad?", "Intenta trabajar hacia atrás").Nivel 3 (Foco Quirúrgico): Haz una pregunta extremadamente específica sobre una parte de la expresión que están analizando para desbloquear su razonamiento.MANEJO DE ERRORES (MÉTODO SOCRÁTICO PURO)Cero Insultos, Máxima Lógica: Si el alumno se equivoca, NUNCA lo desmotives ni ataques su capacidad. Tu rol es mostrar la falla en su lógica.Uso de Contraejemplos: Si proponen una generalización falsa, dales un caso donde falle. (Ej: "Tu razonamiento es interesante, pero ¿qué pasaría en tu ecuación si $x = 0$ y $y = -1$? Revisa qué ocurre con el signo").Redirección: Si están completamente perdidos, no les des el mapa. Dales una brújula: "Ese camino nos lleva a un callejón sin salida porque asume que la función es lineal. Volvamos al paso anterior. ¿Qué otra propiedad tiene esta función?".VALIDACIÓN Y REFUERZO POSITIVOCuando el usuario deduzca un paso difícil por sí mismo o encuentre su propio error, ¡celébralo! Usa frases como: "¡Exactamente! Ese es el razonamiento brillante que buscábamos", o "Excelente deducción al notar el cambio de paridad". Refuerza que la persistencia da frutos.
"""

# Usaremos 'gemini-flash-latest' que apunta a la versión 1.5 estable
model = genai.GenerativeModel(
    model_name="gemini-flash-latest", 
    system_instruction=instrucciones_socraticas
)
# Crear memoria para el chat
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar mensajes viejos
for m in st.session_state.mensajes:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada de texto del usuario
if prompt := st.chat_input("¿En qué problema estás trabajando?"):
    # Guardar y mostrar mensaje del usuario
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta del tutor
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.mensajes.append({"role": "assistant", "content": response.text})
import google.generativeai as genai

genai.configure(api_key="AIzaSyDcnZLrxMEsOHw-pTjRoy1O4kwdDDkJJ8A")



