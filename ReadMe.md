![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

# Wiser

## Установка

1. Инициализируйте репозиторий Git и настройте удаленный доступ:

   ```bash
   git init
   git config credential.helper '!aws codecommit credential-helper $@'
   git config credential.UseHttpPath true
   экспорт ключей
   git remote add origin <url>
   git pull origin main
   ```

2. Настройки окружения. Создайте файл `.env` в корне вашего проекта и добавьте следующие переменные окружения:

   ```dotenv
   SECRET_KEY=                 # Секретный ключ Django, используемый для безопасности
   
   ALLOWED_HOSTS=*             # Разрешенные хосты для вашего приложения Django
   DOMAIN_NAME=https://wiser.inclusivetec.com/  # Доменное имя вашего сайта
   
   REDIS_HOST=                 # Хост Redis для кэширования или очередей задач
   AWS_STORAGE_BUCKET_NAME=    # Имя бакета Amazon S3 для хранения статических файлов и медиафайлов
   
   DEBUG=True                  # Режим отладки Django (True для разработки, False для продакшена)
   USE_S3=True                 # Использовать ли хранилище Amazon S3 для статических файлов и медиафайлов
   LOGGING=False
   
   DATABASE_NAME=              # Имя базы данных
   DATABASE_USER=              # Имя пользователя базы данных
   DATABASE_PASSWORD=          # Пароль базы данных
   DATABASE_HOST=              # Хост базы данных
   DATABASE_PORT=5432          # Порт базы данных
   
   EMAIL_HOST=smtp.gmail.com   # SMTP-хост для отправки электронной почты
   EMAIL_PORT=587              # Порт SMTP-сервера
   EMAIL_HOST_USER=            # Имя пользователя SMTP-сервера
   EMAIL_HOST_PASSWORD=        # Пароль SMTP-сервера
   EMAIL_USE_TLS=True          # Использовать ли TLS для безопасной связи с SMTP-сервером
   EMAIL_USE_SSL=False         # Использовать ли SSL для безопасной связи с SMTP-сервером
   ```

3. Загрузите скрипт установки Docker:

   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   ```

4. Запустите скрипт установки Docker:

   ```bash
   sudo sh get-docker.sh
   ```

5. Добавьте текущего пользователя в группу Docker 

   ```bash
   sudo usermod -aG docker $USER
   sudo systemctl status docker
   sudo systemctl start docker
   ```

6. Установите Docker Compose:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   ```   
7. Дайте разрешение на выполнение файла Docker Compose:
   ```bash
   sudo chmod +x /usr/local/bin/docker-compose
   ```

8. Сборка и запуск Docker-контейнеров:

    ```bash
   docker-compose up -d --build
   ```

9. Запустите Docker-контейнеры (на переднем плане):

    ```bash
   docker-compose up
   ```

---

**Примечание.** Все конечные точки `GET` доступны любому пользователю, тогда как другие
методы (`POST`, `PUT`, `PATCH`, `DELETE`) доступны только администраторам. Это означает, что для использования этих
конечные точки требуется аутентификация с правами администратора.

# Токены доступа

Эти конечные точки предоставляют функционал для аутентификации и управления токенами доступа к API.

| Метод | Эндпоинт              | Описание                                                                               |
|-------|-----------------------|----------------------------------------------------------------------------------------|
| POST  | `/api/token/`         | Получение токена доступа. Пользователь должен предоставить свои учетные данные.        |
| POST  | `/api/token/refresh/` | Обновление токена доступа. Пользователь должен предоставить действующий refresh token. |

### Health Check

**URL:** `/v1/healthcheck/`

**Метод:** `GET`

**Описание:** Этот эндпоинт предназначен для проверки состояния сервера. При успешном запросе сервер возвращает JSON
объект с ключом `"status"` и значением `"ok"`, а также устанавливает статус ответа HTTP 200 OK.