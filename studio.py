import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import random

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Neon Studio", page_icon="🔴", layout="centered")

# --- DESIGN PERSONALIZAT (CSS) ---
# Aici e magia pentru culorile vișiniu și neon
st.markdown("""
    <style>
        /* 1. Fundalul principal (Vișiniu închis) */
        .stApp {
            background-color: #2c0710; /* Vișiniu foarte închis */
        }
        
        /* 2. Sidebar-ul (Meniul din stânga - puțin mai deschis pentru contrast) */
        [data-testid="stSidebar"] {
             background-color: #3d0a16;
        }

        /* 3. Titlurile (H1) să fie Roșu Neon strălucitor */
        h1 {
            color: #ff1a4d !important; /* Roșu neon */
            text-shadow: 0 0 15px #ff0033, 0 0 30px #ff0033; /* Efect de strălucire (Glow) */
            font-weight: bold;
        }
        
        /* 4. Subtitlurile și textul normal */
        h2, h3, p, label, .stMarkdown {
             color: #ffccd5 !important; /* Un roz palid ca să fie lizibil pe fundal închis */
        }

        /* 5. Căsuțele de text și butoanele */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; /* Vișiniu mediu */
             color: #ffffff !important; /* Text alb în căsuțe */
             border: 1px solid #ff1a4d; /* Margine roșu neon */
        }
        
        /* Butonul principal */
        .stButton > button {
            background-color: #ff1a4d !important;
            color: white !important;
            border: none;
            box-shadow: 0 0 10px #ff1a4d; /* Strălucire buton */
        }
        .stButton > button:hover {
             background-color: #d9002f !important; /* Mai închis când pui mouse-ul */
        }

    </style>
    """, unsafe_allow_html=True)

# --- APLICAȚIA PROPRIU-ZISĂ ---

st.title("🔴 NEON DESIGN STUDIO")
st.write("Generator Minimalist • Stil Cyberpunk • Nelimitat")

# Meniul din stânga
with st.sidebar:
    st.header("CONTROL PANEL")
    prompt_user = st.text_area("Descrie ideea ta:", "Un BMW futurist, lumini roșii neon, atmosferă întunecată")
    
    # Meniu stiluri (Actualizat pentru tema nouă)
    stil = st.selectbox("Stilul Neon:", ["Cyberpunk Dark", "Neon Noir", "Futuristic Glow", "Abstract Minimalist"])
    
    st.markdown("---") # O linie separator
    buton = st.button("✨ ACTIVEAZĂ GENERAREA ✨")

# Partea principală
if buton:
    # Folosim un spinner roșu
    with st.spinner("🔴 Se inițializează rețeaua neurală..."):
        try:
            # TRUCUL MAGIC (Seed aleatoriu)
            numar_magic = random.randint(1, 9999999)
            
            # Construim promptul final, forțând culorile cerute de tine
            # Adăugăm "dark background, neon red lights" la orice cere userul
            # ca să se potrivească cu site-ul.
            prompt_final = f"{prompt_user}, {stil} style, dark background, glowing neon red elements, minimalist"
            prompt_safe = prompt_final.replace(" ", "%20")
            
            # Link-ul special
            url = f"https://image.pollinations.ai/prompt/{prompt_safe}?width=1024&height=768&seed={numar_magic}&nologo=true"
            
            # Descărcăm
            raspuns = requests.get(url)
            
            if raspuns.status_code == 200:
                image = Image.open(BytesIO(raspuns.content))
                # Afișăm cu o margine neon
                st.image(image, caption=f"Rezultat: {prompt_user}", use_column_width=True)
                st.success("✅ Sistemul a generat imaginea cu succes.")
            else:
                st.error("⚠️ Eroare de conexiune la server.")
                
        except Exception as e:
            st.error(f"❌ Eroare critică: {e}")
