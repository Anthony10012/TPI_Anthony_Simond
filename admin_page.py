"""
 Project name: TPI_Kaizen_Classroom
 File : admin_page.py
 Author : Anthony Simond
 description: the admin interface page
 Date : 2026/05/04
 last modified : 2026/05/05
 Version : 1.1
"""
import streamlit as st

from data_manager import save_follow_up,get_all_students, get_all_follow_ups,get_all_teachers


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


    with tabs[2]:
        st.subheader("Tous les suivis")

        c1, c2 , c3 = st.columns(3)

        with c1:
            # Retrieving students for the filter
            students = get_all_students()
            student_options = {f"{s['lastname']} {s['firstname']}": s['idStudents'] for s in students}
            sel_student = st.selectbox("Filtrer par élève",options=["Tous"] + list(student_options.keys()))
            id_student_filter = student_options[sel_student] if sel_student != "Tous" else None


        with c2:
            teachers = get_all_teachers()
            teachers_options = {f"{t['lastname']} {t['firstname']}": t['idUsers'] for t in teachers}
            sel_teacher = st.selectbox("Filtrer par enseignant", options=["Tous"] + list(teachers_options.keys()))
            id_teacher_filter = teachers_options[sel_teacher] if sel_teacher != "Tous" else None


        with c3:
            date_range = st.date_input("Période (du ... au ...)",value=())

        st.markdown("---")
        c4 , c5 , c6 = st.columns([1, 1, 1])
        with c4:
            start_filter = st.time_input("Après (Heure)",value=None)
        with c5:
            end_filter = st.time_input("Avant (Heure)",value=None)
        with c6:
            st.write("")
            st.write("")
            if st.button("Actualiser les filtres"):
                st.rerun()

        final_date_range = date_range if len(date_range) == 2 else None


        data = get_all_follow_ups(
            student_id=id_student_filter,
            teacher_id=id_teacher_filter,
            date_range=final_date_range,
            start_time= start_filter,
            end_time= end_filter
        )

        # Displaying results
        if not data:
            st.info("Aucun suivi ne correspond à ces critères.")
        else:
            header =["Date", "Élève", "Enseignant", "Présence", "Contenu", "Observations", "Début", "Fin"]

            formatted_data = []
            for row in data:
                new_row = []

                # Date
                date_value = row[0].strftime("%d/%m/%Y") if row[0] else ""
                new_row.append(date_value)

                # Student and Teacher
                new_row.append(str(row[1]))
                new_row.append(str(row[2]))

                # Presence
                presence = "✅ Présent" if row[3] == 1 else "❌ Absent"
                new_row.append(presence)

                # Content and Observations
                new_row.append(str(row[4]) if row[4] else "")
                new_row.append(str(row[5]) if row[5] else "")

                # Start and End hour
                # Help with IA
                # Convert the timedelta to a string and keep only the HH:MM part
                start_val = str(row[6])[:5] if row[6] is not None else ""
                end_val = str(row[7])[:5] if row[7] is not None else ""
                new_row.append(start_val)
                new_row.append(end_val)

                formatted_data.append(new_row)
            st.table([header] + formatted_data)

            st.write(f"**Total: {len(data)} suivi (s)**")

