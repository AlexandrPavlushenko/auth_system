import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Role, BusinessElement, AccessRoleRule, CustomUser


def populate_data():
    # Создаем роли
    admin_role, created = Role.objects.get_or_create(name='admin', defaults={'description': 'Администратор системы'})
    user_role, created = Role.objects.get_or_create(name='user', defaults={'description': 'Обычный пользователь'})
    manager_role, created = Role.objects.get_or_create(name='manager', defaults={'description': 'Менеджер'})

    # Создаем бизнес-элементы
    users_element, created = BusinessElement.objects.get_or_create(name='users',
                                                                   defaults={'description': 'Пользователи системы'})
    products_element, created = BusinessElement.objects.get_or_create(name='products',
                                                                      defaults={'description': 'Товары'})
    orders_element, created = BusinessElement.objects.get_or_create(name='orders', defaults={'description': 'Заказы'})
    access_rules_element, created = BusinessElement.objects.get_or_create(name='access_rules',
                                                                          defaults={'description': 'Правила доступа'})

    # Создаем правила доступа для администратора
    AccessRoleRule.objects.get_or_create(
        role=admin_role,
        business_element=users_element,
        defaults={
            'can_read': True, 'can_read_all': True,
            'can_create': True, 'can_update': True, 'can_update_all': True,
            'can_delete': True, 'can_delete_all': True
        }
    )

    AccessRoleRule.objects.get_or_create(
        role=admin_role,
        business_element=products_element,
        defaults={
            'can_read': True, 'can_read_all': True,
            'can_create': True, 'can_update': True, 'can_update_all': True,
            'can_delete': True, 'can_delete_all': True
        }
    )

    AccessRoleRule.objects.get_or_create(
        role=admin_role,
        business_element=access_rules_element,
        defaults={
            'can_read': True, 'can_read_all': True,
            'can_create': True, 'can_update': True, 'can_update_all': True,
            'can_delete': True, 'can_delete_all': True
        }
    )

    # Создаем правила доступа для менеджера
    AccessRoleRule.objects.get_or_create(
        role=manager_role,
        business_element=users_element,
        defaults={
            'can_read': True, 'can_read_all': True,
            'can_create': False, 'can_update': False, 'can_update_all': False,
            'can_delete': False, 'can_delete_all': False
        }
    )

    AccessRoleRule.objects.get_or_create(
        role=manager_role,
        business_element=products_element,
        defaults={
            'can_read': True, 'can_read_all': True,
            'can_create': True, 'can_update': True, 'can_update_all': True,
            'can_delete': False, 'can_delete_all': False
        }
    )

    # Создаем правила доступа для обычного пользователя
    AccessRoleRule.objects.get_or_create(
        role=user_role,
        business_element=products_element,
        defaults={
            'can_read': True, 'can_read_all': False,
            'can_create': False, 'can_update': False, 'can_update_all': False,
            'can_delete': False, 'can_delete_all': False
        }
    )

    AccessRoleRule.objects.get_or_create(
        role=user_role,
        business_element=orders_element,
        defaults={
            'can_read': True, 'can_read_all': False,
            'can_create': True, 'can_update': True, 'can_update_all': False,
            'can_delete': True, 'can_delete_all': False
        }
    )

    # Создаем тестового администратора
    if not CustomUser.objects.filter(email='admin@example.com').exists():
        admin_user = CustomUser.objects.create_user(
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True
        )
        admin_user.role = admin_role
        admin_user.save()

    # Создаем тестового менеджера
    if not CustomUser.objects.filter(email='manager@example.com').exists():
        manager_user = CustomUser.objects.create_user(
            email='manager@example.com',
            password='manager123',
            first_name='Manager',
            last_name='User'
        )
        manager_user.role = manager_role
        manager_user.save()

    # Создаем тестового пользователя
    if not CustomUser.objects.filter(email='user@example.com').exists():
        user_user = CustomUser.objects.create_user(
            email='user@example.com',
            password='user123',
            first_name='Regular',
            last_name='User'
        )
        user_user.role = user_role
        user_user.save()

    print("Данные успешно заполнены!")


if __name__ == '__main__':
    populate_data()
