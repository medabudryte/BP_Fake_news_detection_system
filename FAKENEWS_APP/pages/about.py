import streamlit as st

def run():
    st.title("📖 Apie sistemą")
    st.markdown("""
    **Prototipinė sistema sukurta bakalauro baigiamajam projektui:**
    **Melagingų naujienų atpažinimo metodų palyginamoji analizė.**

    **Sistemos ir projekto autorė:** Meda Budrytė  
    **Studijų programa:** Duomenų mokslas ir inžinerija  
    **Fakultetas:** Matematikos ir gamtos mokslų fakultetas, KTU

    ---
    ### Kaip veikia sistema?
    Ši sistema leidžia analizuoti naujienų tekstus ir nustatyti, ar jie yra **melagingi** ar **tikri**. Sistema naudoja kelis iš anksto apmokytus mašininio mokymosi modelius:  
    - **`nousresearch/deephermes-3-mistral-24b-preview:free`** – pažangus giliojo mokymosi modelis, kuris klasifikuoja tekstus pagal jų turinį.
    - **Logistinė regresija** ir **SVM** (atraminių vektorių mašina), kurie buvo apmokyti naudojant **NEWS** duomenų rinkinį, pasiekę **tikslumus virš 93%**.

    Modeliai remiasi natūralios kalbos apdorojimo (NLP) metodais ir įvairiais klasifikavimo algoritmais, leidžiančiais tiksliai atpažinti melagingas naujienas.

    Analizės rezultatai pateikiami su tikimybiniais įverčiais ir vizualizacijomis, kurios padeda geriau suprasti modelio sprendimus.

    ---
    ### Naudojami modeliai
    - **Modelis `nousresearch/deephermes-3-mistral-24b-preview:free`:** Giliojo mokymosi modelis, sukurtas su **Mistral 24B** architektūra. Modelis geba analizuoti tekstus ir nustatyti melagingas naujienas.
    - **Logistinė regresija** ir **SVM (Palaikomo vektoriaus mašinos):** Abu modeliai buvo apmokyti su **NEWS** duomenų rinkiniu ir pasiekė **tikslumus virš 93%**. Naudotojai gali pasirinkti, su kuriuo modeliu norėtų dirbti.

    ---
    ### Naudotojų vaidmenys ir funkcijos:
    **Administratorius:**
    - Gali peržiūrėti modelio tikslumo metrikas ir informaciją.
    - Gali naudotis visomis naudotojo funkcijomis, įskaitant naujienų analizę ir ataskaitų peržiūrą.

    **Naudotojas:**
    - Gali analizuoti naujienų tekstus.
    - Gali pasirinkti modelį (giliojo mokymosi, logistinę regresiją ar SVM).
    - Gali peržiūrėti išsaugotas analizės ataskaitas ir jas atsisiųsti.

    ---
    **Pastaba:** Prisijungimui naudokite atitinkamus vartotojo vardus ir slaptažodžius, kad galėtumėte pasiekti savo vaidmeniui skirtas funkcijas.
    """)
    st.markdown("**Kauno technologijos universitetas**")
    st.markdown("**Matematikos ir gamtos mokslų fakultetas**")
    st.markdown("**Duomenų mokslas ir inžinerija**")
    st.markdown("**2025 m.**")
    st.markdown("**Visos teisės saugomos © 2025 Meda Budrytė**")
