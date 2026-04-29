"""
 Project name: TPI_Kaizen_Classroom
 File : app.py
 Author : Anthony Simond
 description: Login page
 Date : 2026/04/29
 last modified : 2026/04/29
 Version : 1.0
"""

import streamlit as st
from security import check_password


st.set_page_config(page_title="Connexion - Suivi Pédagogique",layout="centered",)

st.markdown("""
    <style>
    /* Center the content */
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        align-items: center;
    }

    /* Logo container style */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: -20px;
    }
    .logo-circle {
        background-color: #5c5ce0;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 40px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Titles */
    .login-title {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
        font-size: 32px;
        font-weight: 500;
        margin-top: 20px;
        margin-bottom: 0px;
    }
    .login-subtitle {
        text-align: center;
        color: #666;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Inputs */
    div[data-baseweb="input"] {
        border-radius: 4px;
    }

    /* Login Button */
    div.stButton>button:first-child {
        background-color: #5c5ce0 !important;
        color: red !important;
        width: 100%;
        border-radius: 4px;
        border: none;
        height: 45px;
        font-size: 18px;
        font-weight: 500;
        margin-top: 10px;
    }
    div.stButton>button:hover {
        background-color: #4a4ae2 !important;
        color: red !important;
    }
    </style>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """, unsafe_allow_html=True)

# --- Interface ---

st.markdown("""
        <div class="logo-container">
            <div class="logo-circle">
                <i class="fa-solid fa-graduation-cap"></i>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<h1 class="login-title">Suivi Pédagogique</h1>', unsafe_allow_html=True)
st.markdown('<p class="login-subtitle">Connectez vous à votre espace</p>', unsafe_allow_html=True)


# Login Form

col1,col2,col3 = st.columns([1,2,1])

with col2:
    with st.form("login_form",clear_on_submit=False):
        email = st.text_input("Email *",placeholder="Email *", label_visibility="collapsed")
        password = st.text_input("Mot de passe *",type="password",placeholder="Mot de passe *", label_visibility="collapsed")

        submit = st.form_submit_button("➔ Se connecter",use_container_width=True)

        if submit:
            if email and password:
                st.info("Tentative de connexion...")
                # user = verify_login(email,password)
                # if user:
                #       st.session_state['auth']
                #       st.rerun()
            else:
                st.error("Veuillez remplir tous les champs")