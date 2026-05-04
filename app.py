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

from database import verify_login
from teacher_page import show_teacher_page
from admin_page import show_admin_page


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
    div[data-testid="stForm"] button {
        background-color: #5c5ce0 !important;
        color: white !important;
        border-radius: 4px !important;
    }

    div[data-testid="stForm"] button:hover {
        background-color: #4a4ae2 !important;
        color: white !important;
    }
    

    div[data-testid="stTextInput"] button {
        background-color: transparent !important;
        color: #666 !important; 
        border: none !important;
        box-shadow: none !important;
    }

    div[data-testid="stTextInput"] button:hover {
        background-color: rgba(0,0,0,0.05) !important;
        color: #333 !important;
    }
    </style>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """, unsafe_allow_html=True)

# --- Interface ---

if st.session_state.get('auth'):
    role = st.session_state['user_info']['role']

    if role == "Enseignant":
        show_teacher_page()

    elif role == "Admin":
        show_admin_page()
else:
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
                    user = verify_login(email,password)
                    if user:
                        st.session_state['auth'] = True
                        st.session_state['user_info'] = user
                        st.success(f"Bienvenue {user['firstname']} !")
                        st.rerun()
                else:
                    st.error("Email ou mot de passe invalide")