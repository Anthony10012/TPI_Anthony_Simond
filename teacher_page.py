"""
 Project name: TPI_Kaizen_Classroom
 File : teacher_page.py
 Author : Anthony Simond
 description:
 Date : 2026/04/29
 last modified : 2026/04/29
 Version : 1.0
"""
import streamlit as st

from data_manager import get_students_for_teacher,save_follow_up

def show_teacher_page():
    user_info = st.session_state['user_info']


    # --- HEADER ---
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("Espace Enseignant")
        st.write(f"Connecté : {user_info['firstname']} {user_info['lastname']}")
    with col_logout:
        if st.button("Déconnexion ->"):
            st.session_state.clear()
            st.rerun()

    # --- CONTENU ---
    tab_create, tab_view = st.tabs(["+ SAISIR UN SUIVI"," MES SUIVIS"])

    with tab_create:
        st.subheader("Saisie du suivi hebdomadaire")
        teacher_id = user_info['idUsers']
        liste_eleves = get_students_for_teacher(teacher_id)

        if not liste_eleves:
            st.warning("Vous n'avez pas encore d'élèves attribués.")
        else:
            dict_eleves = {f"{e['lastname']} {e['firstname']}": e['idStudents'] for e in liste_eleves}

            with st.container(border=True):
                c1, c2 = st.columns(2)
                with c1:
                    eleves_sel = st.selectbox("Élève *",options=list(dict_eleves.keys()))

                with c2:
                    date_seance = st.date_input("Date de la séance *")

                presence = st.radio("Présence de l'élève *",["Présent","Absent"],horizontal=True)
                is_present = 1 if presence == "Présent" else 0

                reason = ""
                if presence == "Absent":
                    reason = st.text_input("Raison de l'absence")

                content = st.text_area("Contenu pédagogique abordé *")
                observations = st.text_area("Observations et remarques")

                if st.button(" 💾 Enregistrer le suivi",type="primary"):
                    if is_present == 1 and not content:
                        st.error("Veuillez remplir le contenu pédagogique")
                    else:
                        success = save_follow_up(date_seance,is_present,reason,content,observations,dict_eleves[eleves_sel],teacher_id)
                        if success:
                            st.success("Suivi enregistré avec succès !")
                        else:
                            st.error("Erreur lors de l'enregistrement.")

    with tab_view:
        st.write("Liste des suivis a venir")