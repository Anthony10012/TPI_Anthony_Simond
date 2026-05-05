"""
 Project name: TPI_Kaizen_Classroom
 File : data_manager.py
 Author : Anthony Simond
 description:  Data manager that consolidates CRUD (Create, Read) operations
              for business features, including student management
              by teacher and the recording of educational progress.
 Date : 2026/04/29
 last modified : 2026/04/05
 Version : 1.1
"""
from streamlit import cursor
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
    tracking_number = str(uuid.uuid4())[:8].upper()
    conn = get_connection()
    cursor = conn.cursor()
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
    JOIN students s ON f.Students_idStudents = s.idStudents 
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
    cursor.execute("SELECT idStudents, firstname, lastname FROM students ORDER BY lastname")
    res = cursor.fetchall()
    conn.close()
    return res

def get_all_teachers():
    """
    Retrieve the list of all teachers with the role of "Enseignant"
    :return: List of dictionaries containing the ‘idUsers’, ‘firstname’, and ‘lastname’ fields for teachers.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT idUsers, firstname, lastname FROM users WHERE role = 'Enseignant' ORDER BY lastname")
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
