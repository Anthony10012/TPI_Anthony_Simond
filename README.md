# TPI_Anthony_Simond

# Description

Kaizen Classroom is an educational management application designed to centralize and simplify student tracking. Developed as part of my Individual Practical Project (TPI), it enables seamless collaboration between the administration and the teaching staff.

Administration: Full management (CRUD) of entities, real-time activity statistics, and assignment management.

Teachers: Quick entry of weekly progress reports, attendance management, and student history.

Security: Secure authentication, password hashing (BCrypt), and role-based access control.

# Technologies Used

- **Language** : Python 3.13
- **Interface** : Streamlit (Framework web)
- **DataBase** : MySQL 8.0
- **Security** : BCrypt
- **Database Management** : MySQL Connector Python
- **Dependency Manager** : pip

# Project Structure
```
├── database/               # SQL scripts
├── .env.example            # Template for environment variables
├── login.py                # Application entry point
├── data_manager.py         # CRUD Logic and SQL Queries
├── database.py             # Configuring the MySQL connection and managing the session
├── security.py             # Security logic (password hashing and verification using Bcrypt)
├── seed_users.py           # Utility script for initializing and injecting test data (Seeding)
├── admin_page.py           # Administrator Interface
├── teacher_page.py         # Teacher Interface
└── requirements.txt        # List of required Python libraries
```

# Setup and Execution

**Prerequisites** 
* Python 3.13
* Local MySQL server (WAMP, XAMPP, or MySQL Installer)

**Installation Steps**

1. Get the sources

    Option A : Clone the repository
    `git clone https://github.com/Anthony10012/TPI_Anthony_Simond.git`
    Option B : Extract the provided project ZIP archive and open the terminal in the root folder.


2. Install dependencies

`pip install -r requirements.txt`

3. Database Configuration
    
   3.1 **Schema :**

    - Import the Script_Create_DB.sql file into your MySQL management tool.

    - The file is located in the directory: /database.

    3.2 **Environment variables :**

    - Copy the .env.example file and rename it to .env.
    
    - Open the .env file and enter your local credentials (DB_HOST, DB_USER, etc.).

    3.3 **Initialisation :**

    - Run the following script to populate the database and create test accounts:

    `python seed_users.py`
# Usage

To launch the application, run the following command from the project root directory:

`streamlit run login.py`

# Test credentials


| Role    |           Email | Password |
|:--------|:-------------:|---------:|
| Admin   | anthony.simond@eduvaud.ch | admin123 |
| Teacher | raphael.favre@eduvaud.ch  |    fr123 |