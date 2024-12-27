import psycopg2
from psycopg2 import sql
from database import DB_NAME, DB_PORT, DB_HOST, DB_USER, DB_PASSWORD

def create_tables():
    db_params = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'port': DB_PORT
    }

    create_table_queries = [
        """CREATE TABLE IF NOT EXISTS course (
            course_id VARCHAR(255) PRIMARY KEY,
            course_type VARCHAR(255),
            name VARCHAR(255) NOT NULL,
            department_name VARCHAR(255) NOT NULL,
            credit INT
        );""",

        """CREATE TABLE IF NOT EXISTS student (
            student_id VARCHAR(255) PRIMARY KEY,
            nfc_tag_id VARCHAR(255) UNIQUE,
            branch_lvl VARCHAR(255),
            name VARCHAR(255) NOT NULL,
            section_id INT,
            address VARCHAR(255),
            email VARCHAR(255),
            phone_number VARCHAR(255),
            department_name VARCHAR(255)
        );""",

        """CREATE TABLE IF NOT EXISTS section (
            section_id INT PRIMARY KEY,
            department_name VARCHAR(255),
            student_id VARCHAR(255),
            FOREIGN KEY (student_id) REFERENCES student(student_id)
        );""",

        """CREATE TABLE IF NOT EXISTS professor (
            professor_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            phone_number VARCHAR(255),
            designation VARCHAR(255),
            department_name VARCHAR(255)
        );""",

        """CREATE TABLE IF NOT EXISTS timetable (
            lecture_num VARCHAR(255) PRIMARY KEY,
            section_id INT NOT NULL,
            course_id VARCHAR(255) NOT NULL,
            professor_id VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            FOREIGN KEY (section_id) REFERENCES section(section_id),
            FOREIGN KEY (course_id) REFERENCES course(course_id),
            FOREIGN KEY (professor_id) REFERENCES professor(professor_id)
        );""",

        """CREATE TABLE IF NOT EXISTS attendance (
            student_id VARCHAR(255) NOT NULL,
            course_id VARCHAR(255) NOT NULL,
            lecture_date DATE NOT NULL,
            status BOOL,
            PRIMARY KEY (student_id, course_id, lecture_date),
            FOREIGN KEY (student_id) REFERENCES student(student_id),
            FOREIGN KEY (course_id) REFERENCES course(course_id)
        );""",

        """CREATE TABLE IF NOT EXISTS semester (
            course_id VARCHAR(255) NOT NULL,
            semester_id VARCHAR(255),
            PRIMARY KEY (course_id, semester_id),
            FOREIGN KEY (course_id) REFERENCES course(course_id)
        );""",

        """CREATE TABLE IF NOT EXISTS auth (
            id VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            auth_password VARCHAR(255) NOT NULL
        );""",

        """CREATE TABLE IF NOT EXISTS aa (
            staff_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            aa_auth_pass VARCHAR(255)
        );""",

        """CREATE TABLE IF NOT EXISTS aa_manager (
            manager_id INT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            aaManager_auth_pass VARCHAR(255)
        );"""
    ]

    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        for query in create_table_queries:
            cursor.execute(query)
            print(f"Executed: {query.splitlines()[0]}")

        conn.commit()
        print("All tables created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    create_tables()
