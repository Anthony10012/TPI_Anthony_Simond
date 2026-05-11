"""
 Project name: TPI_Kaizen_Classroom
 File : data_manager.py
 Author : Anthony Simond
 description:  Data manager that consolidates CRUD (Create, Read) operations
              for business features, including student management
              by teacher and the recording of educational progress.
 Date : 2026/04/29
 last modified : 2026/05/11
 Version : 1.3
"""
import bcrypt
from database import get_connection
import uuid


def get_students_for_teacher(teacher_id):
    """
    Retrieves the list of students assigned to a specific teacher.

    Perform a join between the ‘students’ and ‘assignments’ tables to
    filter students based on the user ID (teacher).
    :param teacher_id: Unique teacher ID.
    :return: List of dictionaries containing the ID, first name, and last name of the students
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT s.idStudents, s.firstname, s.lastname
        FROM students s
        JOIN assignments a ON s.idStudents = a.Students_idStudents 
        WHERE a.Users_idUsers = %s 
    """
    cursor.execute(query, (teacher_id,))
    students = cursor.fetchall()
    conn.close()
    return students

def save_follow_up(date,presence,reason_absence, content, observation, student_id,teacher_id, h_debut, h_final):
    """
    Record the follow-up, including the reason for the absence if necessary.

    :param date: Date of the session
    :param presence: 1 if present, 0 if absent.
    :param reason_absence: Text explaining the absence (can be None or “”)
    :param content: Educational content
    :param observation: Notes
    :param student_id: Student ID
    :param teacher_id: Teacher ID
    :param h_debut: start time of the session
    :param h_final: end time of the session
    :return: True if successful, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(tracking_number) FROM `follow-ups`")
    result = cursor.fetchone()

    last_number = result[0] if result[0] is not None else 0
    tracking_number = last_number + 1

    query = """
        INSERT INTO `follow-ups` 
        (tracking_number,session_date, is_present, reason_absence,educational_content, observations, start_hour,end_hour, Students_idStudents, Users_idUsers)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    
    """
    try :
        cursor.execute(query, (tracking_number,date, presence,reason_absence, content, observation,h_debut,h_final, student_id,teacher_id))
        conn.commit()
        return True
    except Exception as e :
        print(f"Erreur SQL : {e}")
        return False
    finally:
        conn.close()


def get_teacher_follow_ups(teacher_id,student_id=None,date_filter=None):
    """
    Retrieves the history of educational follow-ups created by a teacher.
    Allows results to be filtered by student or date. The function uses
    optional parameters to construct a dynamic SQL query.
    :param teacher_id: ID of the logged-in teacher (foreign key).
    :param student_id: (Optional) Student ID to filter the results.
    :param date_filter: (Optional) Specific date in YYYY-MM-DD format.
    :return: a list of records containing details of the sessions and the student's identity.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT f.session_date , s.firstname, s.lastname, f.is_present, 
           f.educational_content, f.observations, f.reason_absence
    FROM `follow-ups` f 
    INNER JOIN students s ON f.Students_idStudents = s.idStudents 
    WHERE f.Users_idUsers = %s 
    """
    params = [teacher_id]

    if student_id:
        query += " AND f.Students_idStudents = %s "
        params.append(student_id)
    if date_filter:
        query += " AND f.session_date = %s "
        params.append(date_filter)

    query += " ORDER BY  f.session_date DESC "

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


def get_all_students():
    """
    Retrieve the list of all students.
    :return: A list of dictionaries, where each dictionary contains ‘idStudents’, ‘firstname’, and ‘lastname’.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT s.idStudents, s.firstname, s.lastname,s.birthdate,s.is_active,p.lastname as parent_name
    FROM students s 
    LEFT JOIN parents p ON s.Parents_idParents = p.idParents 
    ORDER BY lastname
    
            """
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res

def get_all_teachers():
    """
    Retrieve the list of all teachers with the role of "Enseignant"
    :return: List of dictionaries containing the ‘idUsers’, ‘firstname’,‘lastname’, and 'email'.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT idUsers, firstname, lastname, email FROM users WHERE role = 'Enseignant' ORDER BY lastname")
    res = cursor.fetchall()
    conn.close()
    return res


def get_all_follow_ups(student_id=None,teacher_id=None,date_range=None, start_time=None, end_time=None):
    """
    Retrieves the list of educational progress reports from the database using optional filters.

    :param student_id: Student ID to filter follow-ups
    :param teacher_id: Teacher ID to filter follow-ups
    :param date_range: A tuple or list containing two dates (start, end) for filtering by time period
    :param start_time: (Optional) Start date in YYYY-MM-DD format.
    :param end_time: (Optional) End date in YYYY-MM-DD format.
    :return: A list of tuples containing the tracking data.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT f.session_date , s.lastname , u.lastname ,f.is_present, f.educational_content, f.observations, f.start_hour, f.end_hour
    FROM `follow-ups` f 
    JOIN students s ON f.Students_idStudents = s.idStudents 
    JOIN users u ON f.Users_idUsers = u.idUsers
    WHERE 1=1
    """
    params = []

    # Filter by start time
    if start_time:
        query += " AND f.start_hour >= %s "
        params.append(start_time)

    # Filter by end time
    if end_time:
        query += " AND f.end_hour <= %s "
        params.append(end_time)

    # Filter by student
    if student_id:
        query += " AND f.Students_idStudents = %s "
        params.append(student_id)

    # Filter by teacher
    if teacher_id:
        query += " AND f.Users_idUsers = %s "
        params.append(teacher_id)

    # Filter by date
    if date_range and len(date_range) == 2:
        query += " AND f.session_date BETWEEN %s AND %s "
        params.extend([date_range[0], date_range[1]])

    query += " ORDER BY  f.session_date DESC "

    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

def get_teacher_stats():
    """
    Calculates performance and activity statistics by teacher.
    :return: List of dictionaries containing ‘name’, ‘nb_seances’, ‘nb_eleves’, and ‘total_hours’.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Query that counts sessions and calculates duration# Query that counts sessions and calculates duration
    # We use TIMEDIFF to calculate the duration between start_hour and end_hour
    query = """
    SELECT
        u.lastname as name,
        COUNT(f.`idFollow-ups`) as nb_seances,
        COUNT(DISTINCT f.Students_idStudents) as nb_eleves,
        SUM(f.is_present) as nb_presences,
        IFNULL(ROUND(SUM(TIME_TO_SEC(TIMEDIFF(f.end_hour, f.start_hour))/3600), 1),0) as total_hours
    FROM users u
    LEFT JOIN `follow-ups` f ON u.idUsers = f.Users_idUsers
    WHERE u.role = 'Enseignant'
    GROUP BY u.idUsers
    """
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res

def get_available_months():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT DISTINCT DATE_FORMAT(session_date, '%m-%Y') as `value`,
                    DATE_FORMAT(session_date, '%M-%Y') as label
    FROM `follow-ups`
    ORDER BY `value` DESC
    """
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return {row['label']: row['value'] for row in res}


def add_student(lastname,firstname,birthdate,parent_id):
    """
    Adds a new student to the database.
    :param lastname: Lastname of the student.
    :param firstname: Firstname of the student.
    :param birthdate: Birthdate of the student.
    :param parent_id: Parent ID of the student.
    :return: True if the student was successfully added, False otherwise.
    """
    try :
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO students (lastname, firstname, birthdate,is_active, Parents_idParents)
            VALUES (%s, %s, %s,1, %s)
        """
        cursor.execute(query, (lastname, firstname, birthdate,parent_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error adding student:{e}")
        return False

def get_all_parents():
    """
    Retrieves all parents of the student.
    :return: A list of dictionaries, each containing 'idParents', 'lastname','firstname', and 'email'.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT idParents ,lastname , firstname,email,phone_number FROM parents ORDER BY lastname")
    res = cursor.fetchall()
    conn.close()
    return res

def delete_student(id_student):
    """
    Deletes a student from the database.
    :param id_student:  The id of the student to delete.
    :return: True if successful, False otherwise.
    """
    try :
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE idStudents = %s", (id_student,))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error deleting student:{e}")
        return False

def update_student(id_student, lastname, firstname, birthdate, is_active):
    """
    Updates a student from the database.
    :param id_student: ID of the student to update.
    :param lastname: Lastname of the student.
    :param firstname: Firstname of the student.
    :param birthdate: Birthdate of the student.
    :param is_active: True if the student is active, False otherwise.
    :return: True if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        UPDATE students
        SET lastname = %s, firstname = %s, birthdate = %s, is_active = %s
        WHERE idStudents = %s
        """
        cursor.execute(query, (lastname, firstname, birthdate, is_active, id_student))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error updating student:{e}")
        return False


def add_teacher(lastname,firstname,email,password_hash):
    """
    Adds a teacher with a hashed password to the database.
    :param lastname:  Lastname of the teacher.
    :param firstname:  Firstname of the teacher.
    :param email:  Email of the teacher.
    :param password_hash:  Password hashed of the teacher.
    :return: True if successful, False otherwise.
    """
    try:

        password_bytes = password_hash.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO users (lastname, firstname, email, password,role)
            VALUES (%s, %s, %s, %s,'Enseignant')
        """
        cursor.execute(query, (lastname, firstname, email, hashed_password.decode('utf-8')))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error hachage/insertion:{e}")
        return False

def delete_teacher(id_user):
    """
    Deletes a teacher from the database.
    :param id_user:  The id of the teacher.
    :return: True if successful, False otherwise.
    """
    try :
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE idUsers = %s AND role = 'Enseignant'"
        cursor.execute(query, (id_user,))
        conn.commit()

        # Checking whether a line has actually been deleted
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e :
        print(f"Error deleting teacher:{e}")
        return False

def update_teacher(id_user, lastname, firstname, email):
    """
    Updates a teacher from the database.
    :param id_user: The id of the teacher.
    :param lastname:  Lastname of the teacher.
    :param firstname:  Firstname of the teacher.
    :param email:  Email of the teacher.
    :return: True if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE users SET lastname = %s, firstname = %s, email = %s WHERE idUsers = %s"
        cursor.execute(query, (lastname, firstname, email, id_user))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error updating teacher:{e}")
        return False

def add_parent(lastname,firstname,phone_number,email):
    """
    Adds parents to the database.
    :param lastname: lastname of the parent.
    :param firstname: firstname of the parent.
    :param phone_number: phone number of the parent.
    :param email: email of the parent.
    :return: True if successful, False otherwise.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO parents (lastname, firstname, phone_number, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (lastname, firstname, phone_number, email))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error adding parents:{e}")
        return False

def update_parent(id_parent,lastname,firstname,phone_number,email):
    """
    Updates a parent to the database.
    :param id_parent: The id of the parent of the teacher.
    :param lastname:  lastname of the parent.
    :param firstname:  firstname of the parent.
    :param phone_number:  phone number of the parent.
    :param email:  email of the parent.
    :return:  True if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE parents SET lastname = %s, firstname = %s, phone_number = %s,email = %s WHERE idParents = %s"
        cursor.execute(query, (lastname, firstname, phone_number,email,id_parent))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error updating parent:{e}")
        return False

def delete_parent(id_parent):
    """
    Deletes a parent from the database.
    :param id_parent: The id of the parent to delete.
    :return: True if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM parents WHERE idParents = %s",(id_parent,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        # If a student is related, MySQL will block the deletion (foreign key)
        print(f"Error deleting parent:{e}")
        return False

def assign_student_to_teacher(student_id,teacher_id):
    """
    Assigns a student to a teacher.
    :param student_id: The unique id of the student.
    :param teacher_id: The unique id of the teacher.
    :return: True if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # We use IGNORE to avoid duplicates if the link already exists
        query = "INSERT IGNORE INTO assignments (Students_idStudents,Users_idUsers) VALUES (%s,%s)"
        cursor.execute(query, (student_id,teacher_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error assigning student:{e}")
        return False

def get_assignments_by_teacher():
    """
    Retrieve all teachers and the list of their students for the maps.
    :return: dict: A dictionary where the key is the teacher's formatted name (e.g., “J. Dupont”)
                   and the value is a list of students (a dictionary containing ‘id_student’ and ‘full_name’).
                   Returns an empty dictionary if an error occurs
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT u.idUsers, u.firstname AS prof_fn, u.lastname AS prof_ln,
               s.idStudents, s.firstname AS student_fn, s.lastname AS student_ln
        FROM users u 
        JOIN assignments a ON u.idUsers = a.Users_idUsers
        JOIN students s ON a.Students_idStudents = s.idStudents
        WHERE u.role = 'Enseignant'
        ORDER BY u.lastname, s.lastname
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        # Organizing data into a dictionary for Streamlit
        assignments = {}
        for row in rows:
            prof_name = f"{row['prof_fn'][0]}. {row['prof_ln']}"
            if prof_name not in assignments:
                assignments[prof_name] = []

            assignments[prof_name].append({
                "id_student": row['idStudents'],
                "full_name": f"{row['student_fn']} {row['student_ln']}"
            })
        return assignments
    except Exception as e :
        print(f"Error getting assignments:{e}")
        return {}

def remove_assignment(teacher_name,student_id):
    """
    Removes the link between a teacher and a student.

    This function identifies the teacher by their formatted name (e.g., ‘A. Simond’)
    and the student by their unique ID to delete the corresponding entry in
    the ‘assignments’ join table.

    :param teacher_name: str:  The formatted name of the teacher used in the interface.
    :param student_id: Student ID.
    :return: True if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
                DELETE FROM assignments 
                WHERE Students_idStudents = %s 
                AND Users_idUsers = (SELECT idUsers FROM users WHERE CONCAT(LEFT(firstname, 1), '. ', lastname) = %s LIMIT 1)
                """
        cursor.execute(query, (student_id,teacher_name))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print(f"Error removing assignment:{e}")
        return False