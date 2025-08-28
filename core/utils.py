from .models import CustomUser, AccessRoleRule, BusinessElement
import jwt
from django.conf import settings


def get_user_from_token(request):
    """Получение пользователя из JWT токена"""
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]

    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        return CustomUser.objects.get(id=user_id, is_active=True)
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError):
        # Ошибки JWT токена
        return None
    except CustomUser.DoesNotExist:
        # Пользователь не существует
        return None
    except Exception as e:
        # Прочие ошибки
        print(e)
        return None


def check_permission(user, business_element_name, action):
    """Проверка прав доступа пользователя"""
    if not user or not user.is_active:
        return False

    # Суперпользователь имеет все права
    if user.is_superuser:
        return True

    # Получаем роль пользователя
    role = user.role
    if not role:
        return False

    # Получаем бизнес-элемент
    try:
        business_element = BusinessElement.objects.get(name=business_element_name)
    except BusinessElement.DoesNotExist:
        return False

    # Получаем правило доступа
    try:
        rule = AccessRoleRule.objects.get(role=role, business_element=business_element)
    except AccessRoleRule.DoesNotExist:
        return False

    # Проверяем права в зависимости от действия
    if action == 'read':
        return rule.can_read
    elif action == 'create':
        return rule.can_create
    elif action == 'update':
        return rule.can_update
    elif action == 'delete':
        return rule.can_delete
    elif action == 'read_all':
        return rule.can_read_all
    elif action == 'update_all':
        return rule.can_update_all
    elif action == 'delete_all':
        return rule.can_delete_all

    return False