import streamlit as st
import time
from streamlit_option_menu import option_menu
from utils.functions import check_login

def run():
    st.title("Melagingų naujienų patikrinimo sistema") 
    option = option_menu(
        menu_title=None,
        options=["Prisijungimas", "Registracija"],
        icons=["lock", "pen"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        key="login_registration_menu" 
    )

    if option == "Prisijungimas":
        username = st.text_input("Vartotojo vardas", key="username") 
        password = st.text_input("Slaptažodis", type="password", key="password") 

        if st.button("Prisijungti", key="login_button"): 
            check_login(username, password)
            if st.session_state.logged_in:
                st.success(f"Sveiki, {st.session_state.user_role}")
                time.sleep(1)
                st.rerun() 
            else:
                st.error("Neteisingas vartotojo vardas arba slaptažodis")

    elif option == "Registracija":
        st.info("Registracijos funkcionalumas dar nesukurtas.")

