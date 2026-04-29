"""
 Project name: TPI_Kaizen_Classroom
 File : data_manager.py
 Author : Anthony Simond
 description:
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

