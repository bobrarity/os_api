import psycopg2
from psycopg2 import sql

from database import DB_NAME, DB_PORT, DB_HOST, DB_USER, DB_PASSWORD

db_params = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}


queries = [
    """
    -- Insert data into course
INSERT INTO course (course_id, course_type, name, department_name, credit)
VALUES
('SOC3010', 'Major-Required', 'Operating System', 'SOCIE', 3),
('SOC3020', 'Major-Required', 'Database', 'SOCIE', 3),
('SOC3030', 'Major-Required', 'Computer Algorithm', 'SOCIE', 3);

-- Insert data into professor
INSERT INTO professor (professor_id, name, email, phone_number, designation, department_name)
VALUES
('U200002', 'Naseer Abdul Rahim', 'n.abdulrahim@inha.uz', '+998932345678', 'Ph.D. in Computer Science & Engineering', 'SOCIE'),
('U200005', 'Dragunov Andrei', 'a.dragunov@inha.uz', '+998935678901', 'Associate Professor in AI Systems', 'SOCIE');

-- Insert data into student
INSERT INTO student (student_id, nfc_tag_id, branch_lvl, name, section_id, address, email, phone_number, department_name)
VALUES
('U2210188', '1ee0616a', 'junior', 'Feruz Rakhimov', 3, 'buyuk ipak yoli', 'f.raximov@student.inha.uz', '+998935127697', 'SOCIE'),
('U2210183', '4e826a6a', 'junior', 'Azizjon Rakhmanov', 1, 'Aeroport', 'a.rakhmanov@student.inha.uz', '+998330019896', 'SBL'),
('U2210177', '7e0b626a', 'junior', 'Abrorkhon Ozodkhudjaev', 2, 'Yunusobod', 'a.ozodxojayev@student.inha.uz', '+998935886413', 'SOCIE');

-- Insert data into section
INSERT INTO section (section_id, department_name, student_id)
VALUES
(3, 'SOCIE', 'U2210188'),  -- Feruz Rakhimov
(1, 'SBL', 'U2210183'),    -- Azizjon Rakhmanov
(2, 'SOCIE', 'U2210177');  -- Abrorkhon Ozodkhudjaev

-- Insert data into timetable
INSERT INTO timetable (lecture_num, section_id, course_id, professor_id, date, start_time, end_time)
VALUES
('L001', 3, 'SOC3010', 'U200002', CURRENT_DATE, '09:00:00', '10:30:00'),
('L002', 2, 'SOC3020', 'U200005', CURRENT_DATE, '11:00:00', '12:30:00');

-- Insert data into attendance
INSERT INTO attendance (student_id, course_id, lecture_date, status)
VALUES
('U2210188', 'SOC3010', CURRENT_DATE, TRUE),
('U2210177', 'SOC3020', CURRENT_DATE, FALSE);

-- Insert data into auth
INSERT INTO auth (id, email, auth_password)
VALUES
-- Students
('U2210188', 'f.raximov@student.inha.uz', 'studentpass1'),
('U2210183', 'a.rakhmanov@student.inha.uz', 'studentpass2'),
('U2210177', 'a.ozodxojayev@student.inha.uz', 'studentpass3'),

-- Professors
('U200002', 'n.abdulrahim@inha.uz', 'professorpass1'),
('U200005', 'a.dragunov@inha.uz', 'professorpass2'),

-- Staff
('S0001', 'john.doe@email.com', 'staffpass1'),
('S0002', 'jane.smith@email.com', 'staffpass2');

-- Insert staff from aa table
INSERT INTO aa (staff_id, name, email, aa_auth_pass)
VALUES
('S0001', 'john', 'john.doe@email.com', 'password123'),
('S0002', 'jane', 'jane.smith@email.com', 'password456'),
('S0003', 'michael', 'michael.brown@email.com', 'password789'),
('S0004', 'emily', 'emily.davis@email.com', 'passwordabc');

-- Insert managers from aa_manager table
INSERT INTO aa_manager (manager_id, name, email, aaManager_auth_pass)
VALUES
(1, 'alice', 'alice.johnson@email.com', 'managerpass123'),
(2, 'bob', 'bob.white@email.com', 'managerpass456'),
(3, 'clara', 'clara.green@email.com', 'managerpass789');

    """,
]

try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    for query in queries:
        cursor.execute(query)

    conn.commit()
    print("Data inserted successfully!")
except Exception as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
