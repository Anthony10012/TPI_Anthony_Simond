"""
 Project name: TPI_Kaizen_Classroom
 File : admin_page.py
 Author : Anthony Simond
 Description: the admin interface page
 Date : 2026/05/04
 Last modified : 2026/05/13
 Version : 1.4
"""
import streamlit as st
import re
import datetime
from data_manager import *

def show_admin_page():
    """
    Renders the  administrative dashboard.

    this interface serves as the control center for the application, managing:
     - Business Intelligence : Calculates and displays real-time KPIs(attendance rate,active teachers,global hours) and detailed statistical tables.
     - Global Follow-up Oversight : Advanced multicriteria filtering system(by student,teacher,date range and time slots) to monitor all pedagogical activities
     - Entity Management (CRUD) : Full lifecycle management for students,teachers and parents using interactive popovers and forms.
     - Pedagogical Assignments: Logic for linking/unlinking students and teachers to define monitoring scopes.
    :return: None
    """
    user_info = st.session_state['user_info']

    teachers = get_all_teachers()
    teachers_options = {f"{t['lastname']} {t['firstname']}": t['idUsers'] for t in teachers}

    students = get_all_students()
    student_options = {f"{s['lastname']} {s['firstname']}": s['idStudents'] for s in students}
    # --- RED HEADER  (Admin style) ---
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

    with tabs[0]:
        st.subheader("Statistiques et gestion")

        month_db = get_available_months()

        if not month_db:
            month_db = {"Aucune donnée": "00-0000"}

        stats_data = get_teacher_stats()
        # Dynamic calcul
        total_followups = sum(row['nb_seances'] for row in stats_data)
        nb_teachers = len(stats_data)
        total_students = sum(row['nb_eleves'] for row in stats_data)

        # Attendance Rate Calcul
        total_presence = sum(row['nb_presences'] for row in stats_data if row['nb_presences'] is not None)

        if total_followups > 0:
            rate_value = (total_presence / total_followups) * 100
            attendance_rate = f"{rate_value:.1f}%"
        else:
            attendance_rate = "0%"

        # --- KPI DISPLAY ---
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.metric(label="Suivis ce mois",value=str(total_followups))
        with kpi2:
            st.metric(label="Enseignants actifs",value=str(nb_teachers))
        with kpi3:
            st.metric(label="Taux de présence",value=attendance_rate)
        with kpi4:
            st.metric(label="Élèves suivis",value=str(total_students))

        # --- DETAILED TABLE WITH FILTERS ---
        st.markdown("### Décompte des périodes par enseignant")
        with st.container(border=True):
            col_month, col_teacher = st.columns(2)
            with col_month:
                st.selectbox("Mois",options=list(month_db.keys()))
            with col_teacher:
                teacher_choice = st.selectbox("Teacher",options=["Tous les enseignants"] + list(teachers_options.keys()))

            if teacher_choice != "Tous les enseignants":
                stats_data = [row for row in stats_data if row['name'] in teacher_choice]

            header_stats = ["Enseignant","Nombre de séances","Élèves différents","Heures totales(h)"]

            formatted_stats = []
            for row in stats_data:
                # We convert EVERY value to a string to avoid the Arrow conversion error
                formatted_stats.append([
                    str(row['name']),
                    str(row['nb_seances']),
                    str(row['nb_eleves']),
                    f"{row['total_hours']}"
                    ])
            st.table([header_stats] + formatted_stats)

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

                    if h_debut is None or h_fin is None:
                        st.error("Veuillez saisir l'heure de début et l'heure de fin.")

                    elif h_debut >= h_fin:
                        st.error("L'heure de fin doit être après l'heure de début !")

                    elif is_present == 1 and not content:
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
            sel_student = st.selectbox("Filtrer par élève",options=["Tous"] + list(student_options.keys()))
            id_student_filter = student_options[sel_student] if sel_student != "Tous" else None


        with c2:
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

                # Attendance
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

    with tabs[3]:
        st.markdown("""
            <style>
            div.stButton > button[kind="primary"] {
                background-color: #5D5FEF;
                color: white;
                border-radius: 8px;
                border: none;
                padding: 0.5rem 1rem;
            }
            /*  Mouse-over effect */
            div.stButton > button[kind="primary"]:hover {
                background-color: #4547d1;
                color: white;
                border: none;
            }
            </style>
            """, unsafe_allow_html=True)
        st.header("Gestion des entités (CRUD)")

        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["👥 ÉLÈVES", "🎓 ENSEIGNANTS", "👪 PARENTS"])

        with sub_tab1:
            with st.popover("+ Ajouter un élève",type="primary",use_container_width=False):
                st.markdown("### Ajouter un élève")

                with st.form("form_add_student_clean",border=False):
                    full_name = st.text_input("Nom complet", placeholder="Ex: Jean Dupont")

                    min_date = datetime.date(1960,1,1)
                    max_date = datetime.date.today()
                    birth_date = st.date_input("Date de naissance", value=None, format="DD/MM/YYYY",min_value=min_date,max_value=max_date)

                    parents = get_all_parents()
                    parent_options = {f"{p['lastname']} {p['firstname']}": p['idParents'] for p in parents}
                    parent_sel = st.selectbox("Parent responsable", options=list(parent_options.keys()))

                    st.markdown("<br>", unsafe_allow_html=True)
                    col_space, col_annuler, col_ajouter = st.columns([0.5,1.5, 1.5])

                    with col_annuler:
                        cancel = st.form_submit_button("ANNULER")

                    with col_ajouter:
                        submit = st.form_submit_button("AJOUTER")

                    if submit:
                        if full_name and birth_date:
                            # Logic for separating the last name and first name
                            parts = full_name.split(" ", 1)
                            prenom = parts[0]
                            nom = parts[1] if len(parts) > 1 else ""

                            p_id = parent_options[parent_sel]

                            if add_student(nom, prenom, birth_date, p_id):
                                st.success("Élève ajouté avec succès !")
                                st.rerun()
                        else:
                            st.error("Le nom et la date de naissance sont obligatoires.")
                    elif cancel:
                        st.rerun()
            all_students = get_all_students()

            cols = st.columns([2, 1.5, 2, 1, 1.5])
            cols[0].write("**Nom**")
            cols[1].write("**Naissance**")
            cols[2].write("**Parent**")
            cols[3].write("**Statut**")
            cols[4].write("**Actions**")

            st.markdown("---")

            for student in all_students:
                c1, c2, c3, c4, c5 = st.columns([2, 1.5, 2, 1, 1.5])

                c1.write(f"{student['lastname']} {student['firstname']}")

                date_str = student['birthdate'].strftime("%d/%m/%Y") if student['birthdate'] else "N/A"
                c2.write(date_str)

                c3.write(student['parent_name'] if student['parent_name'] else "Aucun")

                statut = "✅ Actif" if student['is_active'] == 1 else "❌ Inactif"
                c4.write(statut)

                btn_edit,btn_delete = c5.columns(2)

                with btn_edit:
                    with st.popover("📝"):
                        st.write(f"Modifier {student['firstname']}")
                        with st.form(f"edit_form_{student['idStudents']}"):
                            new_nom = st.text_input("Nom", value=student['lastname'])
                            new_pre = st.text_input("Prénom", value=student['firstname'])
                            new_date = st.date_input("Naissance", value=student['birthdate'],disabled=True)
                            new_active = st.checkbox("Actif", value=bool(student['is_active']))

                            if st.form_submit_button("Sauvegarder"):
                                if update_student(student['idStudents'], new_nom, new_pre, new_date, int(new_active)):
                                    st.success("Modifié !")
                                    st.rerun()
                with btn_delete:
                    if st.button("🗑️",key=f"delete_{student['idStudents']}"):
                        if delete_student(student['idStudents']):
                            st.success("Élève supprimé")
                            st.rerun()
                        else:
                            st.error("Erreur")

        with sub_tab2:
            with st.popover("+ Ajouter un enseignant", type="primary", use_container_width=False):
                st.markdown("### Ajouter un enseignant")
                with st.form("form_add_teacher",border=False):
                    full_name = st.text_input("Nom complet",placeholder="Prénom Nom")
                    email = st.text_input("Email", placeholder="exemple@eduvaud.ch")
                    pwd = st.text_input("Mot de passe temporaire", type="password")

                    st.markdown("<br>", unsafe_allow_html=True)
                    c_space, c_annuler, c_ajouter = st.columns([1, 1.5, 1.5])

                    with c_annuler:
                        if st.form_submit_button("ANNULER"):
                            st.rerun()
                    with c_ajouter:
                        if st.form_submit_button("AJOUTER", type="primary"):
                            if full_name and email and pwd:
                                parts = full_name.split(" ", 1)
                                firstname = parts[0]
                                lastname = parts[1] if len(parts) > 1 else ""


                                if add_teacher(lastname, firstname, email,pwd):
                                    st.success("Enseignant ajouté !")
                                    st.rerun()
                            else:
                                st.error("Tous les champs sont obligatoires.")


            teachers = get_all_teachers()

            # Header
            h_cols = st.columns([2, 3, 1.5])
            h_cols[0].write("**Nom**")
            h_cols[1].write("**Email**")
            h_cols[2].write("**Actions**")
            st.divider()

            for teacher in teachers:
                col1, col2, col3 = st.columns([2,3,1.5])
                col1.write(f"{teacher['firstname']} {teacher['lastname'].upper()}")
                col2.write(teacher.get('email', 'N/A'))

                b_edit, b_del = col3.columns(2)
                with b_edit:
                    with st.popover("📝"):
                        st.write(f"Modifier {teacher['firstname']} {teacher['lastname']}")
                        with st.form(f"edit_teacher_{teacher['idUsers']}",border=False):
                            new_lastname = st.text_input("Nom", value=teacher['lastname'])
                            new_firstname = st.text_input("Prénom", value=teacher['firstname'])
                            new_email = st.text_input("Email", value=teacher['email'])

                            if st.form_submit_button("Sauvegarder"):
                                if update_teacher(teacher['idUsers'], new_lastname, new_firstname, new_email):
                                    st.success("Modifié !")
                                    st.rerun()
                with b_del:
                    if st.button("🗑️", key=f"del_{teacher['idUsers']}"):
                        if delete_teacher(teacher['idUsers']):
                            st.success("Enseignant supprimé")
                            st.rerun()
                        else:
                           st.error("Action impossible : cet utilisateur n'est pas un enseignant ou n'existe pas.")

        with sub_tab3:
            with st.popover("+ Ajouter un parent", type="primary", use_container_width=False):
                st.markdown("### Ajouter un parent")
                with st.form("form_add_parent",border=False):
                    full_name = st.text_input("Nom complet",placeholder="Prénom Nom")
                    email = st.text_input("Email", placeholder="exemple@eduvaud.ch")
                    phone = st.text_input("Téléphone")

                    st.markdown("<br>", unsafe_allow_html=True)
                    c_space, c_annuler, c_ajouter = st.columns([1, 1.5, 1.5])

                    with c_annuler:
                        if st.form_submit_button("ANNULER"):
                            st.rerun()
                    with c_ajouter:
                        if st.form_submit_button("AJOUTER", type="primary"):
                            if full_name and email and phone:

                                if not re.match(r'^[0-9+\s]+$',phone):
                                    st.error("Le numéro de téléphone est invalide (chiffres, '+' et espaces uniquement).")

                                else:
                                    parts = full_name.split(" ", 1)
                                    firstname = parts[0]
                                    lastname = parts[1] if len(parts) > 1 else ""

                                    if add_parent(lastname, firstname, phone,email):
                                        st.success("Parent ajouté !")
                                        st.rerun()
                            else:
                                st.error("Tous les champs sont obligatoires.")


            parents_list = get_all_parents()

            # Header
            h_cols = st.columns([2, 2,2, 1.5])
            h_cols[0].write("**Nom**")
            h_cols[1].write("**Email**")
            h_cols[2].write("**Téléphone**")
            h_cols[3].write("**Actions**")
            st.divider()

            for parent in parents_list:
                col1, col2, col3,col4 = st.columns([2, 2,2, 1.5])

                col1.write(f"{parent['lastname'].upper()} {parent['firstname']}")
                col2.write(parent.get('email','N/A')) # .get to avoid errors if the email is missing
                col3.write(parent.get('phone_number','N/A'))
                btn_edit, btn_del = col4.columns(2)

                with btn_edit:
                    with st.popover("📝"):
                        with st.form(f"edit_parent_{parent['idParents']}",border=False):
                            new_lastname = st.text_input("Nom",value=parent['lastname'])
                            new_firstname = st.text_input("Prénom",value=parent['firstname'])
                            new_email = st.text_input("Email",value=parent.get('email', ''))
                            new_phone = st.text_input("Téléphone", value=parent.get('phone_number', ''))

                            if st.form_submit_button("Sauvegarder",type="primary"):
                                if new_lastname and new_firstname and new_email and new_phone:
                                    if not re.match(r'^[0-9+\s]+$',new_phone):
                                        st.error("Le numéro de téléphone est invalide (chiffres, '+' et espaces uniquement).")

                                    else :
                                        if update_parent(parent['idParents'], new_lastname, new_firstname,new_phone,new_email):
                                            st.success("Modifié !")
                                            st.rerun()
                                else:
                                    st.error("Tous les champs sont obligatoires.")

                with btn_del:
                    if st.button("🗑️",key=f"del_parent_{parent['idParents']}"):
                        if delete_parent(parent['idParents']):
                            st.success("Supprimé !")
                            st.rerun()
                        else:
                            st.error("Erreur : Ce parent a probablement encore des élèves liés.")

        with tabs[4]:
            st.header("Attribution pédagogique")

            # ADDITION FORM
            with st.container(border=True):
                st.markdown("#### 🔗 Nouvelle affectation")
                c1 , c2, c3 = st.columns([2,2,1])

                with c1:
                    teacher_name = st.selectbox("Sélectionner l'enseignant",options=list(teachers_options.keys()))

                with c2:
                    student_name = st.selectbox("Sélectionner l'élève",options=list(student_options.keys()))

                with c3:
                    st.write(" ")
                    st.write(" ")
                    if st.button("➕ LIER", type="primary", use_container_width=True,key="btn_do_assign"):
                        teacher_id = teachers_options[teacher_name]
                        student_id = student_options[student_name]
                        if assign_student_to_teacher(student_id,teacher_id):
                            st.success("Lien créé !")
                        else:
                            st.error("Erreur ou lien déjà existant.")


                st.markdown("---")

                # MAP DISPLAY
                assignments = get_assignments_by_teacher()

                if not assignments:
                    st.info("Aucune affectation n'a été enregistrée pour le moment.")
                else:
                    rows = list(assignments.items())
                    for i in range(0, len(rows), 3):
                        cols = st.columns(3)
                        for j in range(3):
                            if i + j < len(rows):
                                prof_name, pupils = rows[i+j]
                                with cols[j]:
                                    with st.container(border=True):
                                        st.markdown(f"##### 👤 {prof_name}")
                                        st.caption(f"{len(pupils)} élève(s) suivi(s)")
                                        st.write("")

                                        for p in pupils:
                                            # Student view with delete button
                                            cell_name, cell_del = st.columns([0.8, 0.2])
                                            cell_name.write(f"• {p['full_name']}")
                                            if cell_del.button("🗑️", key=f"del_link_{prof_name}_{p['id_student']}"):
                                                if remove_assignment(prof_name, p['id_student']):
                                                    st.rerun()