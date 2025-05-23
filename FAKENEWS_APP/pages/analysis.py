import streamlit as st
from utils.functions import preprocess_text, generate_probability_chart, save_pdf, load_resources, explain_with_llm

def run():
    model, tfidf, label_encoder = load_resources()

    st.title("📰 Melagingų naujienų patikrinimo sistema")
    st.markdown("Ši programa padeda nustatyti, ar naujienos tekstas yra **netikras** ar **tikras**.")
    model_options = {
        "Modelis 1 – Logistinė regresija": "/Users/medabudryte/Documents/4 kursas/8 semestras/bakis/FAKENEWS_APP/models/best_model.pkl",
        "Modelis 2 – SVM": "/Users/medabudryte/Documents/4 kursas/8 semestras/bakis/FAKENEWS_APP/models/best_model1.pkl"
    }

    selected_model_name = st.radio("Pasirinkite modelį:", list(model_options.keys()), index=0)

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = model_options["Modelis 1 – Logistinė regresija"] 
    st.session_state.selected_model = model_options[selected_model_name]

    model_file_name = st.session_state.selected_model.split("/")[-1].split(".")[0]

    col1, col2 = st.columns(2)
    with col1:
        st.header("📥 Įveskite straipsnio pavadinimą")

        title_input = st.text_input("Straipsnio pavadinimas:", value=st.session_state.get("title_input", ""), key="title_input")
        user_input = st.text_area("Tekstas:", value=st.session_state.get("user_input", ""), height=300, key="user_input")

        analyze_button = st.button("🔍 Analizuoti")

    with col2:
        if analyze_button:

            if title_input.strip() == "" or user_input.strip() == "":
                st.warning("⚠️ Prašome įvesti straipsnio pavadinimą ir tekstą.")
            elif model and tfidf and label_encoder:

                cleaned = preprocess_text(user_input)
                vectorized = tfidf.transform([cleaned])
                pred_proba = model.predict_proba(vectorized)[0]
                pred_label = model.predict(vectorized)[0]
                label_text = label_encoder.inverse_transform([pred_label])[0]

                if label_text == "REAL":
                    label_text = "tikras"
                elif label_text == "FAKE":
                    label_text = "netikras"

                chart_image = generate_probability_chart(pred_proba)

                with st.spinner("Kreipiamasi į LLM..."):
                    explanation = explain_with_llm(user_input, label_text)
                    st.markdown("### 🤖 Dirbtinio intelekto atsakymas:")
                    st.write(explanation)

                st.markdown(f"### 📝 Jūsų pateiktas tekstas yra **{label_text}**")
                st.image(chart_image, caption="Tikimybių grafikas", width=600)

                if 'user' in st.session_state:
                    save_pdf(title_input, label_text, pred_proba, chart_image, selected_model_name)

                else:
                    st.error("Nepavyko išsaugoti ataskaitos: vartotojas nėra prisijungęs.")
