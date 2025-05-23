import streamlit as st
from streamlit_option_menu import option_menu
from pages.history import show_history, show_report
from pages import analysis, models, about,  login 
from utils.functions import logout
st.set_page_config(
    page_title="Melagingų naujienų patikrinimo sistema",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_sidebar_style = """
    <style>
        /* Hide sidebar */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        /* Hide the hamburger menu */
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        /* Expand main content to full width */
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

def main():
    if not st.session_state.logged_in:
        login.run()
    else:
        menu_options = ["Analizė", "Istorija", "Apie", "Atsijungti"]
        menu_icons = ["newspaper", "folder", "info-circle", "logout"]

        if st.session_state.user_role == "admin":
            menu_options.insert(2, "Modelių informacija")
            menu_icons.insert(2, "bar-chart")

        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            key="main_menu"
        )
        if selected == "Analizė":
            analysis.run()
        elif selected == "Istorija":
            if 'viewing_report' in st.session_state:
                show_report()
            else:
                show_history()
        elif selected == "Modelių informacija":
            models.run()
        elif selected == "Apie":
            about.run()
        elif selected == "Atsijungti":
            logout()

if __name__ == "__main__":
    main()
