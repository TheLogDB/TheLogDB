# logdb_app/db_utils.py
from django.db import connection

def execute_query(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
        else:
            return None

def record_audit_log(user_id, action_type, action_details, ip_address):
    sql = """
        INSERT INTO AuditLogs (User_ID, Action_Type, Action_Details, IP_Address)
        VALUES (%s, %s, %s, %s)
    """
    params = [user_id, action_type, action_details, ip_address]
    execute_query(sql, params)

