## Наш стек и пояснение к тестовому

Мы используем
1. Aiogram 3
2. Tortoise ORM + Aerich
3. Pydantic 2
4. FastAPI
5. Docker Compose + Docker
6. Gitlab CI/CD

Мы часто используем Telegram Webapps в наших ботах, тестовое задание как раз завязано на этом.

### Описание тестового задания

Ваша задача - разработать телеграм-бота, который будет взаимодействовать с пользователем и инициировать процесс регистрации.

Регистрация состоит из двух этапов:

1. Запрос у пользователя его настоящего имени.
2. Запрос у пользователя его настоящего возраста.

По завершении регистрации, бот должен отправить пользователю меню с Webapp. Эта веб-приложение должно отображать общее количество зарегистрированных пользователей, а также данные, введенные текущим пользователем во время регистрации.

---

## Local Environment Setup

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed on your system.
- Access to a domain managed by Cloudflare (if not, please contact your system administrator).

### 2. Interactive .env File Setup

```shell
python3 scripts/generate_env.py
````


------------------------------------------------------------------------------------------------------------------------

## Server Setup

### Prerequisites

- [Docker and Docker Compose](#1-docker-and-docker-compose-installation) installed on your server.

### 1. Docker and Docker Compose Installation

Copy `scripts/docker.sh` to the server. Then run:

```shell
sudo sh docker.sh
```