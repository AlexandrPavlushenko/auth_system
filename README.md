# Система аутентификации и авторизации
___
### Описание системы

Система реализует собственную аутентификацию и авторизацию с использованием JWT токенов и ролевой модели доступа.
___
### Структура базы данных

1. **CustomUser - Пользователи системы**
   - email: Email пользователя (уникальный)
   - first_name/last_name: Имя и фамилия
   - is_active: Активен ли пользователь
   - is_staff: Является ли сотрудником
   - role: Роль пользователя
2. **Role - Роли пользователей**
   - name: Название роли
   - description: Описание роли

3. **BusinessElement - Бизнес-элементы приложения**
   - name: Название элемента 
   - description: Описание элемента

4. **AccessRoleRule - Правила доступа**
   - role: Ссылка на роль
   - business_element: Ссылка на бизнес-элемент
   - права доступа: can_read, can_create, can_update, can_delete, can_*_all

5. **UserSession - Сессии пользователей**
   - user: Пользователь
   - token: JWT токен
   - expires_at: Время истечения
   - is_active: Активна ли сессия
---
### API Endpoints
**Аутентификация**

- POST /api/register/ - Регистрация
- POST /api/login/ - Вход
- POST /api/logout/ - Выход
- GET /api/profile/ - Профиль
- POST /api/delete-account/ - Удаление аккаунта

**Бизнес-объекты**

- GET /api/users/ - Список пользователей
- GET /api/products/ - Список товаров

**Администрирование**

- GET /api/admin/roles/ - Список ролей
- GET /api/admin/access-rules/ - Список правил
- PUT /api/admin/access-rules/<id>/ - Обновление правила
---
### Установка и запуск
1. **Установите зависимости:**
```
pip install -r requirements.txt
```
2. **Настройте базу данных PostgreSQL**

Создайте файл `.env` и заполните его данными согласно шаблону `.env.example`
3. **Примените миграции:**
```
python manage.py migrate
```
4. Заполните тестовыми данными:
```
python populate_data.py
```
5. Запустите сервер:
```
python manage.py runserver
```
---
### Тестовые пользователи

- **Администратор**: admin@example.com / admin123
- **Менеджер**: manager@example.com / manager123

- **Пользователь**: user@example.com / user123
---

### Примеры запросов

**Регистрация**

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "password_confirm": "password123"
  }'
```
**Вход**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```
**Получение профиля**
```bash
curl -X GET http://localhost:8000/api/profile/ \
  -H "Authorization: Bearer <your_jwt_token>"
```