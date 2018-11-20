import datetime
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

    finally:
        connection.close()

def delete_planning_period(planning_period, team):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("delete from issue_duration_in_status where planning_period = %s and team = %s", (planning_period, team))

        connection.commit()

    finally:
        connection.close()

def insert_into_issue_duration_in_status(planning_period, team, issue_id, issue_type, status_list):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            for status in status_list:
                # 2018-09-25T15:24:31.825+0000'
                start = datetime.datetime.strptime(status['start'], '%Y-%m-%dT%H:%M:%S.%f%z')
                end = datetime.datetime.strptime(status['end'], '%Y-%m-%dT%H:%M:%S.%f%z')
                cursor.execute(
                    "insert into issue_duration_in_status(planning_period, issue_id, issue_type, status_name, status_start, status_end, status_duration_hours, team) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (planning_period, issue_id, issue_type, status['name'], start, end, status['duration_hours'], team)
            )
        connection.commit()
    finally:
        connection.close()
