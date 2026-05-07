# TPI_Anthony_Simond

# Description

Kaizen Classroom is an educational management application designed to facilitate student tracking among teachers, parents, and administrators. It allows:

Administration: Comprehensive management (CRUD) of students, teachers, and parents.

Teachers: Entering progress reports, managing attendance, and viewing history.

Security: Login system with password hashing (BCrypt) and role management.

# Technologies Used

- **Language** : Python 3.13
- **Interface** : Streamlit (Framework web)
- **Data Base** : MySQL
- **Security** : BCrypt
- **Database Management** : MySQL Connector Python

# Setup and Execution

**Prerequisites** 
* Python 3.13
* MySQL Installer

**Installation**

1. Clone the repository

`git clone https://github.com/Anthony10012/TPI_Anthony_Simond.git`

2. Setup the project

`pip install -r requirements.txt`

3. Database Configuration


    1.Import the Script_Create_DB.sql file into your MySQL management tool.

    2.Check the credentials in the database.py file (host, user, password, database).
    
    3.Run the following script to create the test accounts
    `python seed_users.py`
# Usage

To launch the application, run the following command from the project root directory:

`streamlit run login.py`

# Test credentials


| Role    |           Email | Password |
|:--------|:-------------:|---------:|
| Admin   | anthony.simond@eduvaud.ch | admin123 |
| Teacher | raphael.favre@eduvaud.ch  |    fr123 |