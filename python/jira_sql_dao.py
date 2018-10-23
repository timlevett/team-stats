import pymysql.cursors

from util import get_settings

def get_connection():
    settings = get_settings()

    # Connect to the database
    connection = pymysql.connect(host=settings['db']['host'],
                                user=settings['db']['user'],
                                password=settings['db']['pass'],
                                db=settings['db']['database'],
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

def insert_into_time_in_status(version, issueType, team, status_name, count, theSum, theMax, median, std_diff):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO time_in_status(version, issue_type, team, status_name, count, sum, max, median, std_diff) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (version, issueType, team, status_name, count, theSum, theMax, median, std_diff))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #     cursor.execute(sql, ('webmaster@python.org',))
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()