import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Configurare pagină (Titlu generic)
st.set_page_config(page_title="Design Studio", page_icon="🎨")

# Titlul mare de pe ecran
st.title("🎨 Design Studio")
st.write("Creează imagini AI instant!")

# Meniul din stânga
with st.sidebar:
    st.header("Setări")
    # Aici userul scrie ce vrea
    prompt_user = st.text_area("Ce vrei să desenezi?", "Un BMW futurist în oraș, noaptea")
    buton = st.button("Generează Imaginea")

# Partea principală (Logic)
if buton:
    st.info("⏳ Lucrez la imagine... Te rog așteaptă.")
    try:
        # Pregătim linkul
        prompt_url = prompt_user.replace(" ", "%20")
        url = f"https://image.pollinations.ai/prompt/{prompt_url}"
        
        # Luăm imaginea de pe internet
        raspuns = requests.get(url)
        
        if raspuns.status_code == 200:
            image = Image.open(BytesIO(raspuns.content))
            # Afișăm imaginea fără nume personal
            st.image(image, caption="Design Generat", use_column_width=True)
            st.success("✅ Gata! Imaginea a fost creată.")
        else:
            st.error("Eroare la server.")
            
    except Exception as e:
        st.error(f"Eroare: {e}")