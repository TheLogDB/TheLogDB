# logdb_app/middleware.py
import jwt
from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Paths that don't require authentication
        exempt_paths = [
            '/api/auth/register/',
            '/api/auth/login/',
        ]

        # If the path is exempt, skip authentication
        if any(request.path.startswith(path) for path in exempt_paths):
            return None

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
                request.user_id = payload['user_id']
                return None
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired.'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token.'}, status=401)
        else:
            return JsonResponse({'error': 'Authorization header missing or improperly formatted.'}, status=401)

