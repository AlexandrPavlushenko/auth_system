from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .utils import get_user_from_token

class AuthenticationMiddleware(MiddlewareMixin):
    """Middleware для аутентификации пользователя по JWT токену"""

    # Пути, которые не требуют аутентификации
    PUBLIC_PATHS = [
        '/api/login/',
        '/api/register/',
        '/api/docs/',
        '/admin/',
    ]

    def process_request(self, request):
        # Пропускаем аутентификацию для публичных путей
        if any(request.path.startswith(path) for path in self.PUBLIC_PATHS):
            return None

        user = get_user_from_token(request)

        if user:
            request.user = user
            return None
        else:
            # Для всех остальных запросов требуется аутентификация
            return JsonResponse(
                {'error': 'Требуется аутентификация'},
                status=401
            )