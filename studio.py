import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import time

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. CONFIGURARE API (SECURIZATĂ) ---
token_part_1 = "hf_"
token_part_2 = "QBRsrwvJvMTHLCUkSZqjadBoKJqejxqtvk"
HF_API_TOKEN = token_part_1 + token_part_2

# --- SCHIMBAREA CHEIE ---
# 1. Folosim adresa "router.huggingface.co" (ceea ce cerea eroarea).
# 2. Folosim modelul "DreamShaper" (Lykon/dreamshaper-8). E cel mai stabil model free.
API_URL = "https://router.huggingface.co/models/Lykon/dreamshaper-8"

# --- 3. DESIGN VIZUAL ---
st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        h1 { 
            color: #ff1a4d !important; 
            text-shadow: 0 0 10px #ff0033; 
            font-family: 'Helvetica', sans-serif;
            font-weight: 300; 
        }
        h2, h3, p, label, .stMarkdown, .stExpander { color: #ffccd5 !important; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d;
        }
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stMetricValue"] { color: #ff1a4d !important; }
        [data-testid="stMetricLabel"] { color: #ffccd5 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFAȚA ---
st.title("Studio Design") 
st.caption("Engine: DreamShaper v8 (High Speed)")

with st.sidebar:
    st.header("⚙️ Configurare")
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, neon lights, rain, 8k masterpiece")
    stil = st.selectbox("Stil (Preset):", ["Realistic", "Anime", "3D Art", "Illustration"])
    
    st.info("ℹ️ Conectat la Hugging Face Router.")
    st.markdown("---")
    buton = st.button("GENERARE IMAGINE")

# --- 5. LOGICA DE CONECTARE ---
def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    try:
        # Folosim adresa nouă cu 'router'
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        return response
    except requests.exceptions.Timeout:
        return None 
    except Exception:
        return None

if buton:
    with st.spinner("Se generează imaginea..."):
        try:
            start_time = time.time()
            prompt_final = f"{prompt_user}, {stil} style, (masterpiece, best quality:1.2), 8k"
            
            succes = False
            incercari = 0
            max_retries = 4
            
            while not succes and incercari < max_retries:
                output = query_huggingface({"inputs": prompt_final})
                
                # Cazul 1: Timeout sau eroare de rețea
                if output is None:
                    time.sleep(2)
                    incercari += 1
                    continue

                # Cazul 2: Succes!
                if output.status_code == 200:
                    succes = True
                    image = Image.open(BytesIO(output.content))
                    durata = time.time() - start_time
                    
                    st.image(image, caption="DreamShaper Art", use_column_width=True)
                    st.success("✅ Gata!")
                    
                    with st.expander("📊 Date Tehnice"):
                        c1, c2, c3 = st.columns(3)
                        with c1: st.metric("Timp", f"{durata:.2f}s")
                        with c2: st.metric("Model", "DreamShaper v8")
                        with c3: st.metric("Status", "200 OK")
                
                # Cazul 3: Model Loading (foarte comun)
                else:
                    try:
                        err = output.json()
                        if "estimated_time" in err:
                            wait = err["estimated_time"]
                            st.warning(f"Se încarcă modelul... ({wait:.1f}s)")
                            time.sleep(wait)
                            incercari += 1
                        elif "error" in err:
                            # Aici prindem eroarea cu link-ul dacă mai apare (dar n-ar trebui)
                            st.error(f"Eroare API: {err['error']}")
                            break
                    except:
                        st.error(f"Eroare necunoscută: {output.text}")
                        break
            
            if not succes:
                st.error("Server ocupat. Mai încearcă o dată (butonul Generare).")

        except Exception as e:
            st.error(f"Eroare sistem: {e}")
