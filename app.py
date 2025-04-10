import os
import streamlit as st
import base64
from openai import OpenAI

# ---------- CONFIGURACIÓN DE LA PÁGINA ----------
st.set_page_config(
    page_title="Análisis de Imagen ✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- ESTILOS PERSONALIZADOS ----------
st.markdown("""
    <style>
    body {
        background-color: #0d0d1a;
    }

    .main {
        color: #f2f2f2;
        font-family: 'Segoe UI', sans-serif;
    }

    .title {
        font-size: 48px;
        font-weight: bold;
        color: #ffcc00;
        text-align: center;
        margin-top: 20px;
        animation: glow 2s ease-in-out infinite alternate;
        text-shadow: 2px 2px 10px #ffcc00;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 10px #ffcc00;
        }
        to {
            text-shadow: 0 0 20px #ffaa00;
        }
    }

    .music-button {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background-color: #ffcc00;
        border: none;
        padding: 12px 18px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 50px;
        cursor: pointer;
        color: #000;
        z-index: 9999;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    .music-button:hover {
        background-color: #ffaa00;
        color: white;
    }

    .custom-box {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ffcc00;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- BOTÓN FLOTANTE PARA MÚSICA ----------
st.markdown("""
    <button class="music-button" onclick="document.getElementById('player').play()">🎵 Música</button>
    <audio id="player" src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"></audio>
""", unsafe_allow_html=True)

# ---------- TÍTULO CON ANIMACIÓN ----------
st.markdown('<div class="title">Análisis de Imagen 🤖🏞️</div>', unsafe_allow_html=True)

# ---------- API KEY ----------
ke = st.text_input('🔐 Ingresa tu Clave de OpenAI:', type='password')
if ke:
    os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key) if api_key else None

# ---------- SUBIR IMAGEN ----------
uploaded_file = st.file_uploader("📁 Sube una imagen", type=["jpg", "png", "jpeg"])
if uploaded_file:
    with st.expander("📸 Imagen subida", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# ---------- DETALLES ADICIONALES ----------
show_details = st.toggle("📝 ¿Deseas añadir contexto sobre la imagen?")
if show_details:
    additional_details = st.text_area("✍️ Describe el contexto de la imagen aquí:")

# ---------- BOTÓN DE ANÁLISIS ----------
analyze_button = st.button("🔍 Analizar imagen")

# ---------- FUNCIÓN DE ENCODE ----------
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# ---------- PROCESAMIENTO ----------
if uploaded_file and api_key and analyze_button:
    with st.spinner("🧠 Analizando la imagen..."):
        try:
            base64_image = encode_image(uploaded_file)

            prompt_text = "Describe lo que ves en la imagen en español."
            if show_details and additional_details:
                prompt_text += f"\n\nContexto adicional: {additional_details}"

            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                ],
            }]

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
                    message_placeholder.markdown(f'<div class="custom-box">{full_response}▌</div>', unsafe_allow_html=True)
            message_placeholder.markdown(f'<div class="custom-box">{full_response}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error durante el análisis: {e}")

elif analyze_button:
    if not uploaded_file:
        st.warning("📌 Por favor sube una imagen.")
    if not api_key:
        st.warning("🔐 No se ha ingresado la clave de API.")

