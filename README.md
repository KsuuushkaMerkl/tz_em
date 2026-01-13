**Подготовка к запуску**:
1) В корне проекта создать файл `.env`
2) Сгенерировать JWT_SECRET_KEY командой `$ openssl rand -hex 32` и добавить Ваш ключ в файл `.env`
3) В файле `.env` задать креды главного админа: 
   1) ADMIN_EMAIL
   2) ADMIN_PASSWORD
   3) ADMIN_SURNAME
   4) ADMIN_NAME
   5) ADMIN_PATRONYMIC

4) В файл `.env` добавить настройку PostgreSQL: 
   1) POSTGRES_DB
   2) POSTGRES_USER
   3) POSTGRES_PASSWORD
   4) POSTGRES_HOST
   5) POSTGRES_PORT

**Запуск проекта**:
`$ docker-compose up --build`

**Swagger будет доступен по адресу**: `127.0.0.1:8085/docs`

Тестирование функционала рекомендуется через **Postman**

