# Referal system project

Простой RESTful API сервис для реферальной системы.

### Настройка проекта

Для настройки проекта выполните следующие шаги:

1. Клонируйте репозиторий:
git clone https://github.com/Alina-mufler/referral_system_project.git
2. Перейдите в директорию проекта
3. Скопируйте `.env.example` в новый файл `.env` и заполните необходимые значения переменных окружения:
cp .env.example .env ([Как заполнить переменные окружения?](#Description) )
4. Установите зависимости: 
```pip install -r requirements.txt```
5. Выполните миграции:
```python manage.py migrate```
6. Запустите проект:
```python manage.py runserver```


#### <a id="description">Описание переменных окружения</a>
SECRET_KEY - для его получения необходимо запустить следующий код Python: 
```python
from django.core.management.utils import get_random_secret_key  
print(get_random_secret_key())
```
HUNTER_API_KEY - является уникальным ключом API 
для использования сервиса Hunter.io, который 
предоставляет возможности проверки email-адресов. 
Этот ключ необходим для выполнения запросов к API Hunter.io 
и получения информации об email-адресах.

**Как получить HUNTER_API_KEY:**

1. Перейдите на сайт Hunter.io и создайте учетную запись или войдите в уже существующую.
2. После регистрации или входа в систему перейдите в раздел API на Hunter.io.
3. Нажмите кнопку "Создать ключ API" ("Create API Key") и следуйте инструкциям.
4. Скопируйте созданный ключ API и сохраните его в переменную HUNTER_API_KEY в файле .env.


## Тестирование проекта 

| Действие                                        |                            Путь                            |
|-------------------------------------------------|:----------------------------------------------------------:|
| UI документация                                 |                          /redoc/                           |
| Регистрация                                     |                      /api/auth/users/                      |
| Получение токена                                |      /api/auth/jwt/create/<br/>/api/auth/token/login/      |
| Создание реферального кода                      |                       /api/referral/                       |
| Получение реферального кода по email            | /api/referral/get-by-email/?email=(тут email пользователя) |
| Получение информации о рефералах по id реферера |               /api/referral/{id}/referrals/                |
| Удаление реферального кода                      |                    /api/referral/{id}/                     |
| Регистрация через реферальный код               |   /api/sign_up/    |


