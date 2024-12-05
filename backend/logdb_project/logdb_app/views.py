# logdb_app/views.py
import json
import jwt
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db_utils import execute_query, record_audit_log
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            role_id = data.get('role_id', 2)  # Default Role_ID=2 (Assuming 'Developer')

            if not all([username, email, password]):
                return JsonResponse({'error': 'Username, email, and password are required.'}, status=400)

            # Hash the password
            password_hash = make_password(password)

            # Insert the new user into the database
            sql = """
                INSERT INTO Users (User_Name, Email, PasswordHash, Role_ID)
                VALUES (%s, %s, %s, %s)
            """
            params = [username, email, password_hash, role_id]

            execute_query(sql, params)

            # Fetch the newly created user's ID
            sql_user = "SELECT User_ID, User_Name, Email, Role_ID, Created_At FROM Users WHERE Email = %s"
            user = execute_query(sql_user, [email])[0]

            # Record audit log
            ip_address = request.META.get('REMOTE_ADDR')
            record_audit_log(user_id=user['User_ID'], action_type='Register',
                             action_details=f"User {username} registered.", ip_address=ip_address)

            return JsonResponse({
                'userId': user['User_ID'],
                'username': user['User_Name'],
                'email': user['Email'],
                'roleId': user['Role_ID'],
                'createdAt': user['Created_At']
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return JsonResponse({'error': 'Email and password are required.'}, status=400)

            # Fetch user data from the database
            sql = "SELECT User_ID, User_Name, Email, PasswordHash, Role_ID FROM Users WHERE Email = %s"
            users = execute_query(sql, [email])

            if not users:
                return JsonResponse({'error': 'User not found.'}, status=404)

            user = users[0]

            if check_password(password, user['PasswordHash']):
                # Generate JWT token
                payload = {
                    'user_id': user['User_ID'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                    'iat': datetime.datetime.utcnow(),
                }
                token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

                # Record audit log
                ip_address = request.META.get('REMOTE_ADDR')
                record_audit_log(user_id=user['User_ID'], action_type='Login',
                                 action_details=f"User {user['User_Name']} logged in.", ip_address=ip_address)

                return JsonResponse({
                    'token': token,
                    'user': {
                        'userId': user['User_ID'],
                        'username': user['User_Name'],
                        'email': user['Email'],
                        'roleId': user['Role_ID']
                    }
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


@csrf_exempt
def create_project(request):
    if request.method == 'POST':
        try:
            user_id = getattr(request, 'user_id', None)
            if not user_id:
                return JsonResponse({'error': 'Authentication required.'}, status=401)

            data = json.loads(request.body)
            project_name = data.get('projectName')
            description = data.get('description')
            status = data.get('status', 'Planning')
            start_date = data.get('startDate')
            end_date = data.get('endDate')

            if not project_name:
                return JsonResponse({'error': 'Project name is required.'}, status=400)

            # Insert the new project into the database
            sql = """
                INSERT INTO Projects (Project_Name, Project_Description, Status, StartDate, EndDate, ProjectManager_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = [project_name, description, status, start_date, end_date, user_id]

            execute_query(sql, params)

            # Fetch the newly created project
            sql_project = "SELECT Project_ID, Project_Name, Project_Description, Status, StartDate, EndDate, ProjectManager_ID, Created_At FROM Projects WHERE Project_Name = %s AND ProjectManager_ID = %s"
            projects = execute_query(sql_project, [project_name, user_id])

            if not projects:
                return JsonResponse({'error': 'Project creation failed.'}, status=400)

            project = projects[0]

            # Record audit log
            ip_address = request.META.get('REMOTE_ADDR')
            record_audit_log(user_id=user_id, action_type='Create Project',
                             action_details=f"Project {project_name} created.", ip_address=ip_address)

            return JsonResponse({
                'projectId': project['Project_ID'],
                'projectName': project['Project_Name'],
                'description': project['Project_Description'],
                'status': project['Status'],
                'startDate': project['StartDate'],
                'endDate': project['EndDate'],
                'projectManagerId': project['ProjectManager_ID'],
                'createdAt': project['Created_At']
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


def view_logs(request):
    if request.method == 'GET':
        try:
            user_id = getattr(request, 'user_id', None)
            if not user_id:
                return JsonResponse({'error': 'Authentication required.'}, status=401)

            # Fetch query parameters
            project_id = request.GET.get('projectId')
            log_level = request.GET.get('logLevel')

            sql = "SELECT Log_ID, Project_ID, User_ID, Log_Level, Module, Log_Message, AdditionalData, Created_At FROM Logs WHERE 1=1"
            params = []

            # Optional filters
            if project_id:
                sql += " AND Project_ID = %s"
                params.append(project_id)
            if log_level:
                sql += " AND Log_Level = %s"
                params.append(log_level)

            # Ensure the user has access to the specified projects
            if project_id:
                sql_permission = """
                    SELECT * FROM UserProjects
                    WHERE User_ID = %s AND Project_ID = %s
                """
                permissions = execute_query(sql_permission, [user_id, project_id])
                if not permissions:
                    return JsonResponse({'error': 'Access denied to the specified project logs.'}, status=403)

            logs = execute_query(sql, params)

            # Convert JSON strings to JSON objects
            for log in logs:
                if log['AdditionalData']:
                    log['AdditionalData'] = json.loads(log['AdditionalData'])

            return JsonResponse({'logs': logs}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


def view_audit_logs(request):
    if request.method == 'GET':
        try:
            user_id = getattr(request, 'user_id', None)
            if not user_id:
                return JsonResponse({'error': 'Authentication required.'}, status=401)

            # Check if the user has admin privileges (assuming Role_ID=1 is Admin)
            sql_role = "SELECT Role_ID FROM Users WHERE User_ID = %s"
            roles = execute_query(sql_role, [user_id])

            if not roles or roles[0]['Role_ID'] != 1:
                return JsonResponse({'error': 'Access denied.'}, status=403)

            # Fetch audit logs
            sql = "SELECT Audit_ID, User_ID, Action_Type, Action_Details, Timestamp, IP_Address FROM AuditLogs"
            audit_logs = execute_query(sql)

            return JsonResponse({'auditLogs': audit_logs}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


@csrf_exempt
def submit_log(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = data.get('projectId')
            log_level = data.get('logLevel', 'INFO')
            message = data.get('message')
            module = data.get('module')
            timestamp = data.get('timestamp', datetime.datetime.utcnow().isoformat())
            additional_data = json.dumps(data.get('additionalData', {}))
            user_id = data.get('userId')  # Assuming the endpoint provides the user ID

            if not all([project_id, message]):
                return JsonResponse({'error': 'Project ID and message are required.'}, status=400)

            # Optionally, verify that the project exists
            sql_project = "SELECT * FROM Projects WHERE Project_ID = %s"
            projects = execute_query(sql_project, [project_id])
            if not projects:
                return JsonResponse({'error': 'Project not found.'}, status=404)

            # Insert the log into the database
            sql = """
                INSERT INTO Logs (Project_ID, User_ID, Log_Level, Module, Log_Message, AdditionalData, Created_At)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = [project_id, user_id, log_level, module, message, additional_data, timestamp]

            execute_query(sql, params)

            # Record audit log (if applicable)
            # Assuming that the submit_log endpoint might be called by authenticated users
            # If not authenticated, you might skip this
            # Uncomment below if authenticated
            """
            if user_id:
                ip_address = request.META.get('REMOTE_ADDR')
                record_audit_log(user_id=user_id, action_type='Submit Log',
                                 action_details=f"Log submitted to project {project_id}.", ip_address=ip_address)
            """

            return JsonResponse({'message': 'Log submitted successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

