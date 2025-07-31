import streamlit as st
import openai
import requests
import os
from dotenv import load_dotenv

# --- PAGE CONFIG ---
st.set_page_config(page_title="🎨 AI Image Generator", layout="centered")
# Load API key from Streamlit secrets or .env
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# --- API KEY SETUP ---
# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #141e30, #243b55);
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        font-size: 2.8em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
        color: #00c6ff;
    }
    .subtitle {
        font-size: 1.1em;
        text-align: center;
        color: #eeeeee;
        margin-bottom: 30px;
    }
    .image-box {
        text-align: center;
        padding: 20px;
        background-color: #ffffff10;
        border-radius: 12px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        margin-top: 20px;
    }
    .stButton > button {
        background-color: #00c6ff;
        color: #000000;
        border-radius: 8px;
        padding: 0.6em 1.4em;
        font-weight: bold;
        border: none;
        transition: background 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #7df9ff;
    }
    .footer {
        position: relative;
        text-align: center;
        font-size: 0.9em;
        margin-top: 50px;
        color: #bbbbbb;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown('<div class="title">AI Image Generator 🎨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Turn your ideas into images using OpenAI DALL·E</div>', unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("🛠️ Image Configuration")
    image_size = st.selectbox("Choose image size", ["256x256", "512x512", "1024x1024"], index=1)
    st.markdown("---")
    st.info("💡 Try prompts like:\n- A panda surfing a wave\n- Cyberpunk city at sunset\n- Astronaut playing guitar")

# --- PROMPT INPUT ---
prompt = st.text_area("📝 Describe your image", placeholder="e.g. A robot painting a portrait of a cat", height=100)

# --- IMAGE GENERATION LOGIC ---
image_url = None
image_data = None

if st.button("🚀 Generate Image"):
    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:
        with st.spinner("🧠 Thinking... Generating your artwork..."):
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size=image_size
                )
                image_url = response['data'][0]['url']
                image_data = requests.get(image_url).content

                # Display Image in Styled Box
                st.markdown('<div class="image-box">', unsafe_allow_html=True)
                st.image(image_url, caption="✅ Your AI-generated image", use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error generating image: {e}")

# --- DOWNLOAD BUTTON ---
if image_url and image_data:
    st.download_button(
        label="📥 Download Image",
        data=image_data,
        file_name="ai_image.png",
        mime="image/png"
    )

# --- FOOTER ---
st.markdown('<div class="footer">🚀 Created by PKK</div>', unsafe_allow_html=True)
