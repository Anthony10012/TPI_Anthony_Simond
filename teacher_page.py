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

from data_manager import get_students_for_teacher, save_follow_up, get_teacher_follow_ups


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
                    h_debut = st.time_input("Heure de début", value=None)
                with c2:
                    date_seance = st.date_input("Date de la séance *")
                    h_fin = st.time_input("Heure de fin",value=None)

                presence = st.radio("Présence de l'élève *",["Présent","Absent"],horizontal=True)
                is_present = 1 if presence == "Présent" else 0

                reason = ""
                if presence == "Absent":
                    reason = st.text_input("Raison de l'absence")

                content = st.text_area("Contenu pédagogique abordé *")
                observations = st.text_area("Observations et remarques")

                if st.button(" 💾 Enregistrer le suivi",type="primary"):

                    if h_debut is None or h_fin is None:
                        st.error("Veuillez saisir l'heure de début et l'heure de fin.")

                    elif h_debut >= h_fin:
                        st.error("L'heure de fin doit être après l'heure de début !")

                    elif is_present == 1 and not content:
                        st.error("Veuillez remplir le contenu pédagogique")

                    elif is_present == 1 and not content:
                        st.error("Veuillez remplir le contenu pédagogique")
                    else:
                        success = save_follow_up(date_seance,is_present,reason,content,observations,dict_eleves[eleves_sel],teacher_id,h_debut,h_fin)
                        if success:
                            st.success("Suivi enregistré avec succès !")
                        else:
                            st.error("Erreur lors de l'enregistrement.")

    with tab_view:
        st.subheader("Mes suivis")
        teacher_id = st.session_state['user_info']['idUsers']


        # --- Filter bar ---
        col_f1, col_f2 = st.columns(2)

        with col_f1:
            liste_eleves = get_students_for_teacher(teacher_id)
            noms_eleves = ["Tous les élèves"] + [f"{e['lastname']} {e['firstname']}" for e in liste_eleves]
            filtre_nom = st.selectbox("Filtrer par élève",options=noms_eleves)

        with col_f2:
            filtre_date =  st.date_input("Filtrer par date",value=None)

        # Retrieving the ID of the student selected in the query
        id_sel = None
        if filtre_nom != "Tous les élèves":
            id_sel = next(e['idStudents'] for e in liste_eleves if f"{e['lastname']} {e['firstname']}" == filtre_nom)

        suivis = get_teacher_follow_ups(teacher_id,id_sel,filtre_date)

        if not suivis:
            st.info("Aucun suivi trouvé pour ces critères.")
        else:
            # Display transformation
            data_display = []
            for s in suivis:
                data_display.append({
                    "Date": s['session_date'].strftime("%d/%m/%Y"),
                    "Élève": f"{s['firstname']} {s['lastname']}",
                    "Présence": "✅ Présent" if s['is_present'] else f"❌ Absent ({s['reason_absence']})",
                    "Contenu": s['educational_content'],
                    "Observations": s['observations']
                })
            # Table view
            st.table(data_display)
            st.caption(f"Total : {len(suivis)} suivi(s)")
