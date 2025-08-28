from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """Менеджер пользователя"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff', False):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser', False):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def set_password(self, raw_password):
        """Хеширование пароля с помощью bcrypt"""
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        """Проверка пароля"""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def generate_jwt_token(self):
        """Генерация JWT токена"""
        payload = {
            'user_id': self.id, # type: ignore
            'email': self.email,
            'exp': datetime.now() + timedelta(days=1),
            'iat': datetime.now()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def __str__(self):
        return self.email


class Role(models.Model):
    """Описание ролей"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    """Бизнес-элементы приложения"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AccessRoleRule(models.Model):
    """Правила доступа для ролей к бизнес-элементам"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    business_element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'business_element')

    def __str__(self):
        return f'{self.role} access to {self.business_element}'


class UserSession(models.Model):
    """Модель для хранения сессий пользователей"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        return datetime.now() > self.expires_at

    def __str__(self):
        return f'{self.user.email} - {self.created_at}'