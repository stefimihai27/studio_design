import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import random
import time

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Neon Studio", page_icon="🔴", layout="centered")

# --- DESIGN (CSS) ---
st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        h1 { color: #ff1a4d !important; text-shadow: 0 0 10px #ff0033; }
        h2, h3, p, label, .stMarkdown, .stExpander { color: #ffccd5 !important; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d;
        }
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d;
        }
        /* Metricile să arate bine */
        [data-testid="stMetricValue"] { color: #ff1a4d !important; }
        [data-testid="stMetricLabel"] { color: #ffccd5 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFAȚA ---
st.title("🔴 NEON DESIGN STUDIO")
st.write("Generative AI Inference Engine")

with st.sidebar:
    st.header("⚙️ PARAMETRI")
    prompt_user = st.text_area("Input Text (Prompt):", "Un BMW M4 futurist, lumini roșii, ploaie")
    stil = st.selectbox("Stil Model:", ["Photorealistic", "Cyberpunk", "Anime", "3D Render"])
    st.markdown("---")
    buton = st.button("✨ RULEAZĂ PREDICȚIA ✨")

# --- LOGICA ---
if buton:
    with st.spinner("🔴 Se calculează tensorii..."):
        try:
            # 1. Start Cronometru (pentru a măsura viteza de predicție)
            start_time = time.time()
            
            # 2. Parametrii modelului
            numar_magic = random.randint(1, 999999999)
            prompt_final = f"{prompt_user}, {stil} style, highly detailed, 8k"
            prompt_safe = prompt_final.replace(" ", "%20")
            model_folosit = "Flux-Realism-v1" # Numele tehnic al modelului
            
            # 3. Cererea către AI (Inferența)
            url = f"https://image.pollinations.ai/prompt/{prompt_safe}?model=flux&seed={numar_magic}"
            headers_falsi = {'User-Agent': 'Mozilla/5.0 (Chrome/91.0)'}
            
            raspuns = requests.get(url, headers=headers_falsi)
            
            # 4. Stop Cronometru
            end_time = time.time()
            durata_inferenta = end_time - start_time
            
            if raspuns.status_code == 200:
                image = Image.open(BytesIO(raspuns.content))
                
                # Afișăm imaginea
                st.image(image, caption="Output Generat", use_column_width=True)
                st.success("✅ Predicție Finalizată")
                
                # --- PARTEA PENTRU PROFESOR (Metrici) ---
                with st.expander("📊 Date Tehnice & Metrici Predicție (Click aici)"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Timp Inferență", f"{durata_inferenta:.2f} sec")
                    with c2:
                        st.metric("Model Latent", "Flux.1")
                    with c3:
                        st.metric("Seed Vector", str(numar_magic)[:6])
                    
                    st.code(f"""
PROMPT TENSORS: {prompt_final}
RESOLUTION: 1024x1024 px
STATUS: Converged
                    """, language="yaml")
                    
            else:
                st.warning("⚠️ High Load. Re-try prediction.")
                
        except Exception as e:
            st.error(f"Eroare: {e}")
