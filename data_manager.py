"""
 Project name: TPI_Kaizen_Classroom
 File : data_manager.py
 Author : Anthony Simond
 description:  Data manager that consolidates CRUD (Create, Read) operations
              for business features, including student management
              by teacher and the recording of educational progress.
 Date : 2026/04/29
 last modified : 2026/04/29
 Version : 1.0
"""
from database import get_connection


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

def save_follow_up(date,presence,reason_absence, content, observation, student_id,teacher_id):
    """
    Record the follow-up, including the reason for the absence if necessary.

    :param date: Date of the session
    :param presence: 1 if present, 0 if absent.
    :param reason_absence: Text explaining the absence (can be None or “”)
    :param content: Educational content
    :param observation: Notes
    :param student_id: Student ID
    :param teacher_id: Teacher ID
    :return: True if successful, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO `follow-ups` 
        (session_date, is_present, reason_absence,educational_content, observations, Students_idStudents, Users_idUsers)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    
    """
    try :
        cursor.execute(query, (date, presence,reason_absence, content, observation, student_id,teacher_id))
        conn.commit()
        return True
    except Exception as e :
        print(f"Erreur SQL : {e}")
        return False
    finally:
        conn.close()