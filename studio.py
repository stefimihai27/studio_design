import streamlit as st
import random
import urllib.parse

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. DESIGN VIZUAL (NEON-NOIR) ---
st.markdown("""
    <style>
        /* Fundal General */
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        
        /* Titluri */
        h1 { 
            color: #ff1a4d !important; 
            font-family: 'Helvetica', sans-serif; 
            font-weight: 300; 
            text-shadow: 0 0 10px rgba(255, 26, 77, 0.4); 
        }
        h2, h3, p, label, .stMarkdown { color: #ffccd5 !important; }
        
        /* Input-uri */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; 
             color: white !important; 
             border: 1px solid #ff1a4d; 
             border-radius: 8px;
        }
        
        /* Buton Principal */
        .stButton > button {
            background-color: #ff1a4d !important; 
            color: white !important; 
            border: none; 
            box-shadow: 0 0 15px #ff1a4d; 
            width: 100%; 
            font-weight: bold; 
            padding: 10px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover { 
            background-color: #d9002f !important; 
            box-shadow: 0 0 25px #ff1a4d; 
            transform: scale(1.02);
        }
        
        /* Container Rezultat */
        .result-container {
            background-color: #3d0a16;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #ff1a4d;
            box-shadow: 0 0 20px rgba(255, 26, 77, 0.2);
            margin-top: 20px;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFAȚA ---
st.title("Studio Design") 
st.caption("System Status: ONLINE | Engine: Pollinations Flux (Client-Side)")

with st.sidebar:
    st.header("⚙️ Configurare")
    # Input utilizator
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, neon lights, rain, 8k, realistic")
    stil = st.selectbox("Stil:", ["Photorealistic", "Cinematic", "Anime", "3D Render", "Oil Painting", "Cyberpunk"])
    
    st.markdown("---")
    st.caption("ℹ️ Randare directă în browser.")
    buton = st.button("GENERARE IMAGINE")

# --- 4. LOGICA DE GENERARE ---
if buton:
    # 1. Pregătim Prompt-ul
    # Adăugăm cuvinte cheie pentru calitate maximă
    prompt_final = f"{prompt_user}, {stil} style, masterpiece, 8k resolution, highly detailed"
    
    # 2. Codificăm textul pentru URL (URL Encoding)
    # Transformăm spațiile și caracterele speciale pentru a fi acceptate de link
    prompt_encoded = urllib.parse.quote(prompt_final)
    
    # 3. Generăm un Seed unic
    # Asta asigură că imaginea e diferită de fiecare dată
    seed = random.randint(0, 1000000)
    
    # 4. Construim Link-ul (SECRETUL ESTE AICI)
    # Folosim model='flux' care este GRATUIT.
    # Nu folosim 'turbo' (care cere bani).
    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?model=flux&width=1024&height=1024&seed={seed}&nologo=false"
    
    st.success("✅ Comandă trimisă! Imaginea se încarcă mai jos...")
    
    # 5. INJECTARE HTML (BYPASS COMPLET)
    # Browserul tău descarcă imaginea direct. Serverul Python nu se implică.
    st.markdown(
        f"""
        <div class="result-container">
            <h3 style="color: #ff1a4d; margin-bottom: 15px;">Rezultat Generat</h3>
            <div style="display: flex; justify-content: center;">
                <img src="{image_url}" 
                     alt="Se generează..." 
                     width="100%" 
                     style="border-radius: 10px; min-height: 300px; background-color: #2c0710;"
                />
            </div>
            <p style="color: #ffccd5; margin-top: 15px; font-size: 0.9em;">
                <em>Model: Flux (High Definition) | Seed: {seed}</em>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
