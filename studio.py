import streamlit as st
import random
import urllib.parse

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. DESIGN VIZUAL SIMPLU ---
st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        h1 { color: #ff1a4d !important; font-family: 'Helvetica', sans-serif; font-weight: 300; }
        h2, h3, p, label, .stMarkdown { color: #ffccd5 !important; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d;
        }
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d;
            width: 100%;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFAȚA ---
st.title("Studio Design") 
st.caption("Direct Browser Rendering • No Server Limits")

with st.sidebar:
    st.header("⚙️ Configurare")
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, neon lights, rain, 8k, realistic")
    stil = st.selectbox("Stil:", ["Photorealistic", "Cinematic", "Anime", "3D Render", "Illustration"])
    st.markdown("---")
    buton = st.button("GENERARE IMAGINE")

# --- 4. LOGICA "BROWSER-ONLY" ---
# Acest cod NU folosește serverul pentru a descărca poza (ceea ce cauza eroarea).
# Generează doar un link HTML pe care browserul tău îl deschide singur.

if buton:
    # 1. Pregătim link-ul
    seed = random.randint(0, 1000000)
    prompt_final = f"{prompt_user}, {stil} style"
    # Codificăm textul corect pentru URL (ca să nu avem erori la spații)
    prompt_encoded = urllib.parse.quote(prompt_final)
    
    # 2. Construim URL-ul către Pollinations (Model Turbo = Gratis)
    # Folosim nologo=false pentru a evita blocajele de plată
    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?model=turbo&seed={seed}&width=1024&height=1024&nologo=false"
    
    st.success("✅ Comandă trimisă! Imaginea se încarcă mai jos...")
    
    # 3. AFIȘARE DIRECTĂ PRIN HTML (BYPASS LA SERVER)
    # Asta face browserul tău să ia poza direct, ocolind serverul blocat.
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <img src="{image_url}" 
                 alt="Se generează..." 
                 width="100%" 
                 style="border-radius: 15px; box-shadow: 0 0 20px rgba(255, 26, 77, 0.5);"
            />
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Metrici simple (fictive, doar pentru aspect, că nu putem măsura HTML-ul)
    st.caption(f"Seed utilizat: {seed} | Model: Turbo")

