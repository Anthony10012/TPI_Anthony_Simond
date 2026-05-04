"""
 Project name: TPI_Kaizen_Classroom
 File : admin_page.py
 Author : Anthony Simond
 description:
 Date : 2026/05/04
 last modified : 2026/05/04
 Version : 1.0
"""
import streamlit as st

from data_manager import save_follow_up,get_all_students


def show_admin_page():
    user_info = st.session_state['user_info']

    # --- HEADER ROUGE (Style Admin) ---
    st.markdown("""
        <style>
            .admin-header {
                background-color: #d32f2f;
                padding: 10px;
                border-radius: 5px;
                color: white;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.markdown(f'<div class="admin-header"><h3>Espace Administrateur - {user_info["firstname"]} {user_info["lastname"]}</h3></div>',unsafe_allow_html=True)
    with col_logout:
        if st.button("DÉCONNEXION ->"):
            st.session_state.clear()
            st.rerun()

    tabs = st.tabs(["📊 STATISTIQUES", " + SAISIR UN SUIVI","🕒 TOUS LES SUIVIS","👥 GESTION CRUD","📋 AFFECTATIONS"])


    with tabs[1]:
        st.subheader("Saisie du suivi hebdomadaire")

        liste_eleves = get_all_students()

        if not liste_eleves:
            st.warning("Aucun élève trouvé en base de données.")
        else:
            dict_eleves = {f"{e['lastname']} {e['firstname']}": e['idStudents'] for e in liste_eleves}
            with st.container(border=True):
                c1, c2 = st.columns(2)
                with c1:
                    eleves_sel = st.selectbox("Élève *", options=list(dict_eleves.keys()))
                    h_debut = st.time_input("Heure de début", value=None)
                with c2:
                    date_seance = st.date_input("Date de la séance *")
                    h_fin = st.time_input("Heure de fin", value=None)

                presence = st.radio("Présence de l'élève *", ["Présent", "Absent"], horizontal=True)
                is_present = 1 if presence == "Présent" else 0

                reason = ""
                if presence == "Absent":
                    reason = st.text_input("Raison de l'absence")

                content = st.text_area("Contenu pédagogique abordé *")
                observations = st.text_area("Observations et remarques")

                if st.button(" 💾 Enregistrer le suivi", type="primary"):
                    if is_present == 1 and not content:
                        st.error("Veuillez remplir le contenu pédagogique")
                    else:
                        id_admin = user_info['idUsers']
                        id_eleves_choisi = dict_eleves[eleves_sel]
                        success = save_follow_up(date_seance, is_present, reason, content, observations,
                                                 id_eleves_choisi, id_admin,h_debut, h_fin)
                        if success:
                            st.success("Suivi enregistré avec succès !")
                        else:
                            st.error("Erreur lors de l'enregistrement.")
