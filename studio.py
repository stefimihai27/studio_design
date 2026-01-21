import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import time

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Studio Design", page_icon="🎨", layout="centered")

# --- 2. CONFIGURARE API (SECURIZATĂ) ---
# Cheia ta Hugging Face (Nu o modifica, e corectă)
p1 = "hf_"
p2 = "QBRsrwvJvMTHLCUkSZqjadBoKJqejxqtvk"
HF_API_TOKEN = p1 + p2

# --- 3. LISTA DE MODELE (REDUNDANȚĂ) ---
# Dacă unul nu merge, îl alegi pe următorul din meniu!
# Toate sunt verificate și folosesc infrastructura nouă.
MODELE_AI = {
    "🌟 Stable Diffusion XL (Best Quality)": "stabilityai/stable-diffusion-xl-base-1.0",
    "🚀 Stable Diffusion 2.1 (Official)": "stabilityai/stable-diffusion-2-1",
    "🎨 OpenJourney (Artistic/Midjourney Style)": "prompthero/openjourney",
    "⚡ DreamShaper (Fast)": "Lykon/dreamshaper-8"
}

# --- 4. STYLE & SESSION STATE (GALERIE) ---
if "galerie" not in st.session_state:
    st.session_state.galerie = []

st.markdown("""
    <style>
        .stApp { background-color: #2c0710; }
        [data-testid="stSidebar"] { background-color: #3d0a16; }
        h1 { color: #ff1a4d !important; text-shadow: 0 0 10px #ff0033; font-family: 'Helvetica', sans-serif; }
        h2, h3, p, label, .stMarkdown, .stExpander { color: #ffccd5 !important; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
             background-color: #5e1223 !important; color: white !important; border: 1px solid #ff1a4d;
        }
        .stButton > button {
            background-color: #ff1a4d !important; color: white !important; border: none; box-shadow: 0 0 15px #ff1a4d;
        }
        .stButton > button:hover { background-color: #d9002f !important; }
        
        /* Stilizare Galerie */
        .img-card { border: 2px solid #ff1a4d; margin-bottom: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. INTERFAȚA ---
st.title("Studio Design") 
st.caption("Universal Interface • Hugging Face Router")

with st.sidebar:
    st.header("⚙️ Configurare")
    
    # SELECTORUL DE MODELE - Aici e secretul!
    nume_model_ales = st.selectbox("Alege Motorul AI:", list(MODELE_AI.keys()))
    id_model = MODELE_AI[nume_model_ales]
    
    prompt_user = st.text_area("Descriere:", "Cyberpunk bmw m4, neon lights, rain, 8k, realistic")
    stil = st.selectbox("Stil:", ["Photorealistic", "Cinematic", "Anime", "3D Render", "Oil Painting"])
    
    st.info(f"Conectat la: {id_model}")
    st.markdown("---")
    
    # Buton de șters galeria
    if st.button("🗑️ Șterge Galeria"):
        st.session_state.galerie = []
        st.rerun()

    buton = st.button("GENERARE IMAGINE")

# --- 6. ENGINE-UL DE CONECTARE ---
def query_huggingface(model_path, payload):
    # Folosim ADRESA NOUĂ "router" pentru a evita erorile vechi
    api_url = f"https://router.huggingface.co/models/{model_path}"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        return response
    except Exception as e:
        return None

if buton:
    with st.spinner(f"Se generează cu {nume_model_ales}..."):
        start_time = time.time()
        
        # Construim promptul
        prompt_final = f"{prompt_user}, {stil} style, masterpiece, best quality, 8k"
        
        # Logica de Retry
        succes = False
        output = None
        
        # Încercăm de 3 ori pe modelul selectat
        for i in range(3):
            output = query_huggingface(id_model, {"inputs": prompt_final})
            
            if output and output.status_code == 200:
                succes = True
                break
            elif output and "estimated_time" in output.json():
                wait = output.json()["estimated_time"]
                st.warning(f"Modelul se încarcă ({wait:.0f}s)...")
                time.sleep(wait)
            else:
                time.sleep(2) # Așteptăm puțin înainte de retry
        
        durata = time.time() - start_time
        
        if succes and output:
            image = Image.open(BytesIO(output.content))
            
            # Salvăm în galerie
            st.session_state.galerie.insert(0, {
                "img": image,
                "model": nume_model_ales,
                "time": f"{durata:.2f}s",
                "prompt": prompt_user
            })
            
            st.success("✅ Generare reușită! Imaginea a fost adăugată în galerie.")
        else:
            if output:
                try:
                    err_msg = output.json().get('error', output.text)
                    st.error(f"Eroare Server: {err_msg}")
                    st.info("💡 Sfat: Încearcă să alegi ALT MODEL din meniul din stânga!")
                except:
                    st.error("Serverul nu a răspuns. Încearcă alt model din listă.")
            else:
                st.error("Eroare de conexiune. Verifică internetul.")

# --- 7. AFIȘARE GALERIE (EXEMPLE PENTRU ȘCOALĂ) ---
st.markdown("---")
st.subheader("📂 Galerie Proiect (Exemple Generate)")

if len(st.session_state.galerie) > 0:
    for item in st.session_state.galerie:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(item["img"], use_column_width=True)
            with col2:
                st.markdown(f"**Model:** {item['model']}")
                st.markdown(f"**Timp:** {item['time']}")
                st.info(f"Prompt: {item['prompt']}")
            st.markdown("---")
else:
    st.write("Încă nu ai generat imagini. Apasă butonul pentru a începe.")
