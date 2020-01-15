# Система переводов
## Задание
### Описание проекта    
Проект представляет из себя REST API, которое позволяет  выполнять следующие действия:
* зарегистрировать пользователя с указанием
    * начальный баланс
    * валюта счета
    * email (уникальный; используется для входа)
    * пароль
* аутентифицировать пользователя по почте и паролю
* перевести средства со своего счета на счет другого пользователя (используйте формулу конвертации, если валюты счетов отличаются)
* просмотреть список всех операций по своему счету
* обновлять курсы валют со стороннего ресурса (например, exchangeratesapi.io) раз в N времени (например, раз в 3 минуты)

Система должна поддерживать следующие валюты: EUR, USD, GPB, RUB, BTC

### Требования к системе
* система должна быть реализована на любом python-фреймворке на ваш выбор: Django, Flask, aiohttp, Sanic, Bottle и пр
* для хранения данных должна использоваться СУБД Postgres
* код должен запускаться в Docker-контейнерах
* код должен быть покрыт unit-тестами

### Несистемные требования
* на проект отводится 4-8 часов
* проект должен содержать README, где будет описано как запускать проект
* проект должен быть залит на GitHub/GitLab/BitBucket
* проект должен содержать осмысленные комиты

## Installation and Run
Clone the repository, build and run containers
```
git clone https://github.com/thunderamur/exchange_system
cd exchange_system
docker-compose build
docker-compose up
```
Run bash on web container, make and migrate migrations 
```
docker-compose exec web bash
python manage.py makemigrations
python manage.py migrate
```
Load demo data. All users have the same password is '123'
* admin@mail.local
* eur@mail.local
* usd@mail.local
* rub@mail.local
```
python manage.py start_demo
```
That's it! Now you can check the tasks.
