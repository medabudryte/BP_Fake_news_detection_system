import streamlit as st
import os
import zipfile
import base64
from datetime import datetime

def show_history():
    st.title("📄 Išsaugotos analizės ataskaitos")

    if not os.path.exists("reports"):
        st.info("Nėra išsaugotų ataskaitų.")
        return

    files = sorted(os.listdir("reports"), reverse=True)
    pdfs = [f for f in files if f.endswith(".pdf")]

    if not pdfs:
        st.info("Nėra išsaugotų PDF ataskaitų.")
        return

    st.markdown("### Ataskaitų istorija")
    selected_pdfs = []

    for pdf in pdfs:
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            checkbox = st.checkbox(f"{pdf}", key=pdf)
            if checkbox:
                selected_pdfs.append(pdf)
        with col2:
            if st.button(f"👁️ Peržiūrėti", key=f"view_{pdf}"):
                st.session_state.viewing_report = pdf
                st.rerun()
        with col3:
            if 'confirm_delete' not in st.session_state:
                st.session_state.confirm_delete = None

            if st.button(f"🗑️ Ištrinti", key=f"delete_{pdf}"):
                st.session_state.confirm_delete = pdf

            if st.session_state.confirm_delete == pdf:
                st.warning(f"Ar tikrai norite ištrinti ataskaitą '{pdf}'?")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ Taip, ištrinti", key=f"confirm_yes_{pdf}"):
                        try:
                            os.remove(f"reports/{pdf}")
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.success(f"Ataskaita '{pdf}' sėkmingai ištrinta {timestamp}.")
                        except Exception as e:
                            st.error(f"Klaida trinant ataskaitą: {e}")
                        st.session_state.confirm_delete = None
                        st.rerun()
                with col_no:
                    if st.button("❌ Ne", key=f"confirm_no_{pdf}"):
                        st.session_state.confirm_delete = None
                        st.info("Ištrynimas atšauktas.")
                        st.rerun()

    if selected_pdfs:
        st.markdown("### Atsisiųsti pasirinktas ataskaitas")
        with zipfile.ZipFile("/tmp/selected_reports.zip", "w") as zipf:
            for pdf in selected_pdfs:
                zipf.write(f"reports/{pdf}", pdf)

        with open("/tmp/selected_reports.zip", "rb") as f:
            st.download_button(
                label="📥 Atsisiųsti pažymėtas ataskaitas",
                data=f,
                file_name="pasirinktos_ataskaitos.zip",
                mime="application/zip"
            )
        st.success("Pasirinktos ataskaitos paruoštos atsisiųsti.")

def show_report():
    if 'viewing_report' in st.session_state:
        report_name = st.session_state.viewing_report
        report_path = f"reports/{report_name}"

        st.title("📄 Peržiūrėti ataskaitą")

        try:
            with open(report_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                pdf_display = f"""
                    <iframe src="data:application/pdf;base64,{base64_pdf}" 
                            width="100%" height="800px" 
                            style="border: none;">
                    </iframe>
                """
                st.markdown(pdf_display, unsafe_allow_html=True)

            if st.button("🔙 Grįžti į ataskaitų sąrašą"):
                del st.session_state.viewing_report
                st.rerun()

        except FileNotFoundError:
            st.error("Nepavyko rasti pasirinktos ataskaitos.")
            del st.session_state.viewing_report
            st.rerun()
    else:
        st.error("Nepavyko atidaryti ataskaitos. Grįžkite į istoriją.")
