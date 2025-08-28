from django.contrib import admin
from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    UserProfileView, DeleteAccountView,
    UsersListView, ProductsListView,
    RoleListView, AccessRuleListView, AccessRuleDetailView
)

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Аутентификация
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/delete-account/', DeleteAccountView.as_view(), name='delete-account'),

    # Mock бизнес-объекты
    path('api/users/', UsersListView.as_view(), name='users-list'),
    path('api/products/', ProductsListView.as_view(), name='products-list'),

    # Административные эндпоинты
    path('api/admin/roles/', RoleListView.as_view(), name='roles-list'),
    path('api/admin/access-rules/', AccessRuleListView.as_view(), name='access-rules-list'),
    path('api/admin/access-rules/<int:pk>/', AccessRuleDetailView.as_view(), name='access-rule-detail'),
]