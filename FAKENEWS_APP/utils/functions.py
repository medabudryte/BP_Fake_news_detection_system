import re
import os
import datetime
import time
import joblib
import streamlit as st
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from io import BytesIO
import nltk
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def explain_with_llm(prompt_text, prediction_label):
    headers = {
        "Authorization": f"Bearer {API_KEY}", 
        "Content-Type": "application/json"
    }

    if prediction_label == "netikras":
        system_message = "You are a helpful assistant in fake news detection. The news has been predicted as netikras (fake). In two short sentences In two short sentences, explain why the given text is fake in Lithuanian, and provide any relevant references from web resources or details to support your reasoning."
    else:
        system_message = "You are a helpful assistant in fake news detection. The news has been predicted as tikras (real). In two short sentences In two short sentences, explain why the given text is real in Lithuanian, and provide any relevant references from web resources or details to support your reasoning."

    data = {
        "model": "nousresearch/deephermes-3-mistral-24b-preview:free", 
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"This is the text to analyze:\n\n{prompt_text}\n\nProvide a brief explanation."}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.error(f"LLM klaida: {response.status_code}")
            return "Nepavyko gauti paaiškinimo iš LLM."
    except Exception as e:
        st.error(f"Klaida jungiantis prie LLM: {e}")
        return "Kilo netikėta klaida jungiantis prie LLM."
    
def load_resources():
    """Load the selected model, shared vectorizer, and label encoder."""
    try:
        model_path = st.session_state.get("selected_model")
        if not model_path:
            st.error("Prašome pasirinkti modelį.")
            return None, None, None

        model = joblib.load(model_path)

        vectorizer = joblib.load("/Users/medabudryte/Documents/4 kursas/8 semestras/bakis/FAKENEWS_APP/models/tfidf_vectorizer.pkl")
        label_encoder = joblib.load("/Users/medabudryte/Documents/4 kursas/8 semestras/bakis/FAKENEWS_APP/models/label_encoder.pkl")

        return model, vectorizer, label_encoder

    except Exception as e:
        st.error(f"❌ Klaida įkeliant modelio išteklius: {e}")
        return None, None, None


def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def save_pdf(title, label, pred_proba, chart_img, model_name):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/report_{timestamp}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Melagingu naujienu analizes ataskaita")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Prognoze: {label}")
    c.drawString(50, height - 110, f"FAKE tikimybe: {pred_proba[0]*100:.2f}%")
    c.drawString(50, height - 130, f"REAL tikimybe: {pred_proba[1]*100:.2f}%")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, height - 150, f"Irasymo data: {timestamp}")
    c.drawString(50, height - 170, f"Irasymo tipas: Tekstas")
    c.drawString(50, height - 260, f"Naudotas modelis: {model_name}")
    c.drawString(50, height - 280, f"Modelio versija: 1.0")

    if 'user' in st.session_state:
        c.drawString(50, height - 190, f"Sukure: {st.session_state.user['username']}")
        c.drawString(50, height - 210, f"Role: {st.session_state.user['role']}")

    c.drawString(50, height - 240, f"Straipsnio pavadinimas: {title}")

    img_buffer = BytesIO()
    chart_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    img_path = "/tmp/chart_image.png"
    with open(img_path, "wb") as f:
        f.write(img_buffer.read())

    c.drawImage(img_path, 50, 100, width=500, preserveAspectRatio=True)
    c.save()
    st.success(f"Ataskaita sėkmingai išsaugota į istoriją kaip {filename}")

def generate_probability_chart(pred_proba):
    fig, ax = plt.subplots()
    bars = ax.bar(['FAKE', 'REAL'], pred_proba, color=['red', 'green'])
    ax.set_ylabel("Tikimybė")
    ax.set_ylim(0, 1)

    for bar, prob in zip(bars, pred_proba):
        ax.annotate(f'{prob*100:.1f}%', 
                    xy=(bar.get_x() + bar.get_width()/2, prob),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

def check_login(username, password):
    if username == "admin" and password == "123":
        st.session_state.logged_in = True
        st.session_state.user_role = "admin"
        st.session_state.user = {"username": username, "role": "admin"}
    elif username == "user" and password == "123":
        st.session_state.logged_in = True
        st.session_state.user_role = "user"
        st.session_state.user = {"username": username, "role": "user"}
    else:
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user = None

def login():
    st.markdown("### Prašome prisijungti, kad galėtumėte naudotis sistema.")

    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        username = st.text_input("Vartotojo vardas", key="username")
        password = st.text_input("Slaptažodis", type="password", key="password")

        login_button = st.button("Prisijungti")

        if login_button:
            if username == "admin" and password == "123":
                st.session_state.user = {"username": "admin", "role": "administrator"}
                st.session_state.view = "main"
                st.rerun()
            elif username == "user" and password == "123":
                st.session_state.user = {"username": username, "role": "user"}
                st.session_state.view = "main"
                st.rerun()
            else:
                st.error("Neteisingas vartotojo vardas arba slaptažodis")

def display_metrics(file_path, title):
    if os.path.exists(file_path):
        metrics_df = pd.read_excel(file_path)
        if metrics_df.shape[1] != 2:
            st.error(f"{title}: Failas turi turėti tik du stulpelius.")
        else:
            st.subheader(title)
            metrics_df.columns = ["Metrika 📈", "Vertė"]
            st.table(metrics_df)
    else:
        st.error(f"{title}: Failas nerastas.")
def logout():
    """Atsijungia vartotojas ir grąžina į prisijungimo langą."""
    keys_to_keep = []

    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]

    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user = None
    st.success("Jūs atsijungėte.")
    time.sleep(1)
    st.rerun()
