#!/bin/bash

read -rp "registry: " registry
read -rp "domain: " domain
read -rp "bot token: " bot_token
read -rp "service chat id [0]: " service_chat_id
service_chat_id=${service_chat_id:-0}
read -rp "backend port [5000]: " backend_port
backend_port=${backend_port:-5000}
read -rp "db user [user]: " postgres_user
postgres_user=${postgres_user:-user}
read -rp "db password [generated]: " postgres_password
postgres_password=${postgres_password:-$(openssl rand -hex 16)}
read -rp "db name [postgres]: " postgres_db
postgres_db=${postgres_db:-postgres}
read -rp "db port [5432]: " postgres_port
postgres_port=${postgres_port:-5432}

env_file=".env"

cat <<EOF >$env_file
REGISTRY=$registry
BOT_TOKEN=$bot_token
SERVICE_CHAT_ID=$service_chat_id
DOMAIN=$domain
BACKEND_PORT=$backend_port
POSTGRES_USER=$postgres_user
POSTGRES_PASSWORD=$postgres_password
POSTGRES_DB=$postgres_db
POSTGRES_PORT=$postgres_port
EOF
