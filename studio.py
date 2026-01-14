import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import random
import time  # <--- Am adus intăriri pentru a evita blocarea

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Neon Studio", page_icon="🔴", layout="centered")

# --- DESIGN PERSONALIZAT (CSS) ---
# Aici e doar machiajul site-ului (Vișiniu + Neon). Nu afectează pozele!
st.markdown("""
    <style>
        /* Fundalul principal */
        .stApp { background-color: #2c0710; }
        
        /* Sidebar-ul */
        [data-testid="stSidebar"] { background-color: #3d0a16; }

        /* Titlurile - Roșu Neon */
        h1 {
            color: #ff1a4d !important;
            text-shadow: 0 0 15px #ff0033;
        }
        
        /* Textul normal - Roz pal */
        h2, h3, p, label, .stMarkdown { color: #ffccd5 !important; }

        /* Căsuțele de text */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important;
             color: white !important;
             border: 1px solid #ff1a4d;
        }
        
        /* Butonul */
        .stButton > button {
            background-color: #ff1a4d !important;
            color: white !important;
            border: none;
            box-shadow: 0 0 10px #ff1a4d;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
    </style>
    """, unsafe_allow_html=True)

# --- APLICAȚIA ---

st.title("🔴 NEON DESIGN STUDIO")
st.write("Interfață Cyberpunk • Generare Nelimitată")

with st.sidebar:
    st.header("CONTROL PANEL")
    prompt_user = st.text_area("Descrie ideea ta:", "Un BMW albastru pe plajă")
    
    # Am simplificat meniul ca să nu încurce
    stil = st.selectbox("Stil (Opțional):", ["Realist (4k)", "Anime", "Cyberpunk", "Pictură Ulei", "3D Render"])
    
    st.markdown("---")
    buton = st.button("✨ ACTIVEAZĂ GENERAREA ✨")

if buton:
    with st.spinner("🔴 Se procesează..."):
        try:
            # --- SOLUȚIA ANTI-BLOCAJ ---
            # Combinăm un număr imens cu ora exactă. E imposibil să se repete.
            numar_magic = random.randint(1, 9999999)
            timp_exact = int(time.time())
            
            # --- SOLUȚIA PENTRU CULORI ---
            # Construim promptul FĂRĂ să adăugăm "red neon" forțat.
            prompt_final = f"{prompt_user}, {stil} style, detailed, 8k"
            prompt_safe = prompt_final.replace(" ", "%20")
            
            # Link-ul include acum și timpul (&t=...)
            url = f"https://image.pollinations.ai/prompt/{prompt_safe}?width=1024&height=1024&seed={numar_magic}&t={timp_exact}&nologo=true"
            
            raspuns = requests.get(url)
            
            if raspuns.status_code == 200:
                image = Image.open(BytesIO(raspuns.content))
                st.image(image, caption="Design Generat", use_column_width=True)
                st.success("✅ Generare reușită!")
            else:
                st.error("⚠️ Eroare server. Mai apasă o dată!")
                
        except Exception as e:
            st.error(f"Eroare: {e}")
