from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, UserSession, Role, AccessRoleRule
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserUpdateSerializer, RoleSerializer, AccessRoleRuleSerializer,
    AccessRoleRuleUpdateSerializer
)
from .utils import check_permission


class RegisterView(APIView):
    """Регистрация пользователя"""

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Пользователь успешно зарегистрирован',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Вход в систему"""

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = CustomUser.objects.get(email=email, is_active=True)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        # Генерируем JWT токен
        token = user.generate_jwt_token()

        # Сохраняем сессию
        from datetime import datetime, timedelta
        expires_at = datetime.now() + timedelta(days=1)
        UserSession.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })


class LogoutView(APIView):
    """Выход из системы"""

    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                session = UserSession.objects.get(token=token, is_active=True)
                session.is_active = False
                session.save()
            except UserSession.DoesNotExist:
                pass

        return Response({'message': 'Успешный выход из системы'})


class UserProfileView(APIView):
    """Профиль пользователя"""

    def get(self, request):
        serializer = UserUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    """Удаление аккаунта"""

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()

        # Деактивируем все сессии пользователя
        UserSession.objects.filter(user=user, is_active=True).update(is_active=False)

        return Response({'message': 'Аккаунт успешно удален'})


# Mock views для бизнес-объектов
class UsersListView(APIView):
    """Mock view для списка пользователей"""

    def get(self, request):
        if not check_permission(request.user, 'users', 'read'):
            return Response({'error': 'Доступ запрещен'}, status=403)

        # Mock данные
        mock_data = [
            {'id': 1, 'name': 'User 1', 'email': 'user1@example.com'},
            {'id': 2, 'name': 'User 2', 'email': 'user2@example.com'},
        ]
        return Response(mock_data)


class ProductsListView(APIView):
    """Mock view для списка товаров"""

    def get(self, request):
        if not check_permission(request.user, 'products', 'read'):
            return Response({'error': 'Доступ запрещен'}, status=403)

        # Mock данные
        mock_data = [
            {'id': 1, 'name': 'Product 1', 'price': 100},
            {'id': 2, 'name': 'Product 2', 'price': 200},
        ]
        return Response(mock_data)


# Административные views для управления правами доступа
class RoleListView(APIView):
    """Список ролей (только для администраторов)"""

    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Доступ запрещен'}, status=403)

        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Доступ запрещен'}, status=403)

        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AccessRuleListView(APIView):
    """Список правил доступа (только для администраторов)"""

    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Доступ запрещен'}, status=403)

        rules = AccessRoleRule.objects.all()
        serializer = AccessRoleRuleSerializer(rules, many=True)
        return Response(serializer.data)


class AccessRuleDetailView(APIView):
    """Детальное представление правила доступа (только для администраторов)"""

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Доступ запрещен'}, status=403)

        try:
            rule = AccessRoleRule.objects.get(pk=pk)
        except AccessRoleRule.DoesNotExist:
            return Response({'error': 'Правило не найдено'}, status=404)

        serializer = AccessRoleRuleUpdateSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)