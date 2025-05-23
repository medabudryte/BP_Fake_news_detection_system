import streamlit as st

def run():
    st.title("Melagingų Naujienų Analizė")
    
    st.write("Sveiki atvykę į melagingų naujienų analizės sistemą!")
    
    if st.button("Prisijungimas"):
        from pages import login
        login.run()
    if st.button("Registracija"):
        st.write("Registracija dar nepasiekiama.")
