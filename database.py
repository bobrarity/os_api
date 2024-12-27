import asyncpg

DB_NAME = 'os_dmdc'
DB_HOST = 'dpg-ctmsq69opnds73fidet0-a.oregon-postgres.render.com'
DB_PORT = '5432'
DB_USER = 'admin'
DB_PASSWORD = 'mBwDpERHwVgoA81scRY34prcBXpeN2Sr'

db_conn = None


async def init_db_connection():
    global db_conn
    if db_conn is None:
        db_conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )


async def check_user_credentials(user_id, password):
    global db_conn
    try:
        if db_conn is None:
            await init_db_connection()

        query = '''
        SELECT COUNT(*) FROM auth
        WHERE id = $1 AND auth_password = $2;
        '''
        result = await db_conn.fetchval(query, user_id, password)

        if not result:
            return False

        if str(user_id).startswith('S'):
            # Get all professors and their data along with courses they teach by department
            query = '''
            SELECT p.professor_id, p.name AS professor_name, p.department_name, c.course_id, c.name AS course_name, c.course_type
            FROM professor p
            INNER JOIN course c ON p.department_name = c.department_name;
            '''
            professors = await db_conn.fetch(query)

            professor_data = {}

            for record in professors:
                professor_id = record['professor_id']
                if professor_id not in professor_data:
                    professor_data[professor_id] = {
                        'name': record['professor_name'],
                        'department': record['department_name'],
                        'courses': []
                    }

                professor_data[professor_id]['courses'].append({
                    'course_id': record['course_id'],
                    'course_name': record['course_name'],
                    'course_type': record['course_type']
                })

            return {
                'role': 'staff',
                'professors': professor_data
            }

        elif len(str(user_id)) == 8:
            # Get all the courses for the student_id = user_id using joins
            query = '''
            SELECT c.course_id, c.name, c.course_type, c.department_name, c.credit
            FROM student s
            INNER JOIN section sec ON s.section_id = sec.section_id
            INNER JOIN timetable t ON sec.section_id = t.section_id
            INNER JOIN course c ON t.course_id = c.course_id
            WHERE s.student_id = $1;
            '''
            courses = await db_conn.fetch(query, user_id)

            courses_info = [
                {
                    'course_id': course['course_id'],
                    'name': course['name'],
                    'course_type': course['course_type'],
                    'department_name': course['department_name'],
                    'credit': course['credit']
                }
                for course in courses
            ]

            return {
                'role': 'student',
                'courses': courses_info
            }

        elif len(str(user_id)) == 7:
            # Get current lecture information for the professor
            query = '''
            SELECT t.lecture_num, t.section_id, t.course_id, t.date, t.start_time, t.end_time, c.name AS course_name
            FROM professor p
            INNER JOIN timetable t ON p.professor_id = t.professor_id
            INNER JOIN course c ON t.course_id = c.course_id
            WHERE p.professor_id = $1 AND t.date = CURRENT_DATE AND t.start_time <= CURRENT_TIME AND t.end_time >= CURRENT_TIME;
            '''
            current_lecture = await db_conn.fetchrow(query, user_id)

            if current_lecture:
                lecture_info = {
                    'lecture_num': current_lecture['lecture_num'],
                    'section_id': current_lecture['section_id'],
                    'course_id': current_lecture['course_id'],
                    'date': current_lecture['date'],
                    'start_time': current_lecture['start_time'],
                    'end_time': current_lecture['end_time'],
                    'course_name': current_lecture['course_name']
                }
                return {
                    'role': 'professor',
                    'lecture': lecture_info
                }
            else:
                return {
                    'role': 'professor',
                    'output': 'no_classes_currently'
                }

        else:
            return False

    except Exception as e:
        print(f'Error occurred while checking credentials for user_id {user_id}:', e)
        return False


async def fetch_course_data(course_id):
    global db_conn
    try:
        if db_conn is None:
            await init_db_connection()

        query = '''
        SELECT c.course_id, c.course_type, c.name, c.department_name, c.credit,
               array_agg(s.section_id) AS sections
        FROM course c
        LEFT JOIN timetable t ON c.course_id = t.course_id
        LEFT JOIN section s ON t.section_id = s.section_id
        WHERE c.course_id = $1
        GROUP BY c.course_id, c.course_type, c.name, c.department_name, c.credit;
        '''

        course = await db_conn.fetchrow(query, course_id)

        if not course:
            return None

        return {
            "course_id": course['course_id'],
            "course_type": course['course_type'],
            "name": course['name'],
            "department_name": course['department_name'],
            "credit": course['credit'],
            "sections": course['sections']
        }

    except Exception as e:
        print(f'Error occurred while fetching course details for course_id {course_id}:', e)
        return None


async def fetch_person_data(person_id):
    global db_conn
    try:
        if db_conn is None:
            await init_db_connection()

        if person_id.startswith('S'):
            query = '''
            SELECT staff_id AS id, name, email
            FROM aa
            WHERE staff_id = $1;
            '''
            result = await db_conn.fetchrow(query, person_id)
            role = 'staff'
        elif len(person_id) == 7:
            query = '''
            SELECT professor_id AS id, name, email, phone_number, designation, department_name
            FROM professor
            WHERE professor_id = $1;
            '''
            result = await db_conn.fetchrow(query, person_id)
            role = 'professor'
        elif len(person_id) == 8:
            query = '''
            SELECT student_id AS id, name, email, phone_number, branch_lvl, department_name, section_id
            FROM student
            WHERE student_id = $1;
            '''
            result = await db_conn.fetchrow(query, person_id)
            role = 'student'
        else:
            return None

        if not result:
            return None

        return {
            'role': role,
            'data': dict(result)
        }

    except Exception as e:
        print(f'Error occurred while fetching person data for id {person_id}:', e)
        return None
