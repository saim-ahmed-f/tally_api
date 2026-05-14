# decorators.py

import jwt
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

User = get_user_model()

def Auth_decorator_App(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'detail': 'Authorization header missing or invalid'}, status=401)

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')

            if user_id is None:
                return JsonResponse({'detail': 'Invalid token payload'}, status=401)

            # For UUID primary key field:
            user = User.objects.get(salesmanId=user_id)
            request.user = user  # Attach user to request
        except ExpiredSignatureError:
            return JsonResponse({'detail': 'Token has expired'}, status=401)
        except (InvalidTokenError, User.DoesNotExist):
            return JsonResponse({'detail': 'Invalid token'}, status=401)

        return view_func(request, *args, **kwargs)
    return _wrapped_view
