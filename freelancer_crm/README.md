# Freelancer CRM

Удобная CRM-система для фрилансеров и малого бизнеса.

## Установка
1. Создай виртуальное окружение:  
   `python -m venv .venv`
2. Активируй:  
   `.venv\Scripts\activate` (Windows)
3. Установи зависимости:  
   `pip install -r requirements.txt`
4. Примени миграции:  
   `python manage.py makemigrations`  
   `python manage.py migrate`
5. Создай суперпользователя:  
   `python manage.py createsuperuser`
6. Запусти:  
   `python manage.py runserver`

## Настройка MSSQL
Измени `DATABASES` в `settings.py` на свои параметры:
- HOST: например, `localhost\\SQLEXPRESS`
- USER: `sa`
- PASSWORD: ваш пароль

## Продажа
Можно продавать как:
- Готовое решение за $49–99
- SaaS с подпиской
- Базу для стартапа