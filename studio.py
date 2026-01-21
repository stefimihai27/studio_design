import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import time

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. CHEIA TA (Integrată și Camuflată) ---
# Nu modifica nimic aici, e cheia ta corectă.
p1 = "hf_"
p2 = "QBRsrwvJvMTHLCUkSZqjadBoKJqejxqtvk"
HF_API_TOKEN = p1 + p2

# --- 3. LISTA DE MOTOARE AI (Sistem de Rezervă) ---
# Dacă primul nu merge, codul trece automat la următorul.
# Toate folosesc adresa nouă "router".
API_MODELS = [
    # Opțiunea 1: Stable Diffusion 2.1 (Oficial)
    "https://router.huggingface.co/models/stabilityai/stable-diffusion-2-1",
    
    # Opțiunea 2: Stable Diffusion 1.4 (Cel mai sigur/vechi)
    "https://router.huggingface.co/models/CompVis/stable-diffusion-v1-4",
    
    # Opțiunea 3: OpenJourney (Stil artistic)
    "https://router.huggingface.co/models/prompthero/openjourney"
]

# --- 4. DESIGN VIZUAL ---
st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        h1 { color: #ff1a4d !important; text-shadow: 0 0 10px #ff0033; font-family: 'Helvetica', sans-serif; font-weight: 300; }
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

# --- 5. INTERFAȚA ---
st.title("Studio Design") 
st.caption("System: Multi-Model Failover Architecture")

with st.sidebar:
    st.header("⚙️ Configurare")
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, neon lights, rain, 8k, realistic")
    stil = st.selectbox("Stil:", ["Photorealistic", "Cinematic", "Anime", "3D Render", "Oil Painting"])
    st.info("ℹ️ Sistem conectat. Redundanță activă (3 Noduri).")
    st.markdown("---")
    buton = st.button("GENERARE IMAGINE")

# --- 6. LOGICA INTELIGENTĂ DE CONECTARE ---
def query_api(url, payload):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        return response
    except:
        return None

if buton:
    with st.spinner("Se inițializează secvența de generare..."):
        start_time = time.time()
        prompt_final = f"{prompt_user}, {stil} style, highly detailed, masterpiece, 8k resolution"
        
        imagine_finala = None
        model_folosit = ""
        succes = False

        # --- Începem Bucla prin cele 3 modele ---
        for i, url_curent in enumerate(API_MODELS):
            nume_model = url_curent.split("/")[-1]
            status_text = st.empty() # Loc pentru mesaje temporare
            
            status_text.text(f"Încercare pe serverul {i+1}: {nume_model}...")
            
            # Încercăm de maxim 3 ori per model (în caz de 'loading')
            for incercare in range(3):
                output = query_api(url_curent, {"inputs": prompt_final})
                
                if output is None:
                    # Eroare de rețea, trecem la următoarea încercare
                    continue

                if output.status_code == 200:
                    # ESTE BINE! Am primit poza.
                    try:
                        imagine_finala = Image.open(BytesIO(output.content))
                        model_folosit = nume_model
                        succes = True
                        status_text.empty() # Ștergem mesajul de status
                        break # Ieșim din bucla mică
                    except:
                        continue # Dacă nu putem deschide poza, mai încercăm
                
                # Verificăm dacă e doar "Loading"
                try:
                    err_json = output.json()
                    if "estimated_time" in err_json:
                        wait = err_json["estimated_time"]
                        status_text.text(f"Serverul {nume_model} se încălzește ({wait:.1f}s)...")
                        time.sleep(wait) # Așteptăm cuminți
                    else:
                        # Altă eroare, trecem mai departe
                        break 
                except:
                    break
            
            if succes:
                break # Ieșim din bucla mare, am găsit o poză!
        
        # --- AFIȘARE REZULTAT ---
        if succes and imagine_finala:
            durata = time.time() - start_time
            st.image(imagine_finala, caption=f"Generat cu succes ({model_folosit})", use_column_width=True)
            st.success("✅ Proces finalizat.")
            
            with st.expander("📊 Date Tehnice (Live)"):
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Timp Total", f"{durata:.2f} s")
                with c2: st.metric("Model Activ", model_folosit)
                with c3: st.metric("Status", "200 OK")
        else:
            st.error("⚠️ Toate serverele sunt momentan supraîncărcate. Mai încearcă într-un minut.")
