import os
import streamlit as st
import base64
import json
from openai import OpenAI
from streamlit_lottie import st_lottie

# -------------------- CONFIGURACIÓN DE LA PÁGINA --------------------
st.set_page_config(
    page_title="Análisis de Imagen 🤖🏞️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------- FUNCIONES --------------------
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# -------------------- ESTILOS PERSONALIZADOS --------------------
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        color: #4CAF50;
        font-weight: bold;
        animation: glow 2s infinite alternate;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 10px #4CAF50;
        }
        to {
            text-shadow: 0 0 20px #81C784;
        }
    }

    .music-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #f50057;
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 30px;
        text-align: center;
        line-height: 60px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        cursor: pointer;
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- TÍTULO Y ANIMACIÓN --------------------
st.markdown('<div class="title">Análisis de Imagen 🤖🏞️</div>', unsafe_allow_html=True)
lottie_animation = load_lottie_file("robot.json")
st_lottie(lottie_animation, height=450, key="lottie")

# -------------------- INGRESO API --------------------
ke = st.text_input('🔑 Ingresa tu Clave de OpenAI', type="password")
if ke:
    os.environ['OPENAI_API_KEY'] = ke
    api_key = os.environ['OPENAI_API_KEY']
else:
    st.warning("Por favor ingresa tu clave de API de OpenAI.")
    api_key = None

# -------------------- SUBIDA DE IMAGEN --------------------
uploaded_file = st.file_uploader("📤 Sube una imagen (JPG, PNG o JPEG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("📸 Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# -------------------- DETALLES ADICIONALES --------------------
show_details = st.toggle("📝 ¿Quieres agregar detalles adicionales?", value=False)
if show_details:
    additional_details = st.text_area("✍️ Escribe aquí tu contexto:", disabled=not show_details)
else:
    additional_details = ""

# -------------------- ANÁLISIS DE IMAGEN --------------------
analyze_button = st.button("🔍 Analizar Imagen")

if uploaded_file is not None and api_key and analyze_button:
    client = OpenAI(api_key=api_key)
    with st.spinner("🧠 Analizando la imagen..."):
        try:
            base64_image = encode_image(uploaded_file)

            prompt_text = "Describe lo que ves en la imagen en español."
            if additional_details:
                prompt_text += f"\n\nDetalles adicionales del usuario:\n{additional_details}"

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        },
                    ],
                }
            ]

            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown("🗣️ " + full_response + "▌")

            message_placeholder.markdown("🗣️ " + full_response)

        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")

elif analyze_button and not uploaded_file:
    st.warning("🚨 Por favor, sube una imagen antes de analizar.")

st.markdown("""
    <style>
    /* Fondo negro con estrellas */
    .stApp {
        background-color: #000;
        position: relative;
        overflow: hidden;
    }

    .stApp::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(#ffffff 1px, transparent 1px),
            radial-gradient(#ffffff 1px, transparent 1px);
        background-size: 100px 100px;
        background-position: 0 0, 50px 50px;
        opacity: 0.2;
        animation: sparkle 60s linear infinite;
        z-index: 0;
    }

    @keyframes sparkle {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-50px, -50px); }
    }

    /* Título con brillo */
    .title {
        text-align: center;
        font-size: 40px;
        color: #4CAF50;
        font-weight: bold;
        animation: glow 2s infinite alternate;
        position: relative;
        z-index: 1;
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #4CAF50; }
        to { text-shadow: 0 0 20px #81C784; }
    }

    /* Botón flotante visible */
    .music-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #f50057;
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 30px;
        text-align: center;
        line-height: 60px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        cursor: pointer;
        z-index: 10;
    }

    /* Contenido claro */
    .stTextInput input,
    .stTextArea textarea,
    .stFileUploader,
    .stButton button,
    .stToggle {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #4CAF50 !important;
    }

    .stTextInput label,
    .stTextArea label,
    .stFileUploader label {
        color: white !important;
    }

    /* Textos del contenido */
    .stMarkdown, .st-bb {
        color: white !important;
        z-index: 1;
        position: relative;
    }
    </style>
""", unsafe_allow_html=True)

