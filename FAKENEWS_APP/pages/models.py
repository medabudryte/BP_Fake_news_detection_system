import streamlit as st

from utils.functions import display_metrics

def run():
    st.title("📊 Modelių informacija")
    st.markdown("Pasirinkite modelį, kad galėtumėte matyti jo metrikų lentelę")

    model_options = {
        "Modelis 1 – Logistinė regresija": "/Users/medabudryte/Documents/4 kursas/8 semestras/bakis/FAKENEWS_APP/models/best_model.pkl",
        "Modelis 2 – SVM": "/Users/medabudryte/Documents/4 kursas/8 semestras/bakis/FAKENEWS_APP/models/best_model1.pkl"
    }

    # Display model selection dropdown
    selected_model = st.selectbox("Pasirinkite modelį:", list(model_options.keys()))

    if selected_model:
        display_metrics(
            "/Users/medabudryte/Documents/4 kursas/8 semestras/bakis/FAKENEWS_APP/models/model_info/model_metrics_1.xlsx" if selected_model == "Modelis 1 – Logistinė regresija" else "/Users/medabudryte/Documents/4 kursas/8 semestras/bakis/FAKENEWS_APP/models/model_info/model_metrics.xlsx",
            selected_model
        )

    deactivate_button = st.button(f"Deaktyvuoti šį modelį", key="deactivate_button")
    delete_button = st.button(f"Ištrinti šį modelį", key="delete_button")
    data_button = st.button(f"Tikrinti duomenų rinkinį", key="data_button")
    
    if deactivate_button:
        st.warning(f"⚠️ {selected_model} modelis deaktyvuotas. Funkcija dar nesukurta.") 
    if delete_button:
        st.warning(f"⚠️ {selected_model} modelis ištrintas. Funkcija dar nesukurta.") 
    if data_button: 
        st.warning(f"⚠️ {selected_model} Duomenų prieigos funkcija dar nesukurta.")