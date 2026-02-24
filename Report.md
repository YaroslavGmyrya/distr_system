# Reverse-proxy с помощью Nginx

## Теория

**Nginx** - высокопроизводительный веб-сервер, обратный прокси-сервер (reverse proxy) и балансировщик нагрузки с открытым исходным кодом. Cлавится минимальным потреблением ресурсов, отличной работой со статикой и способностью обрабатывать тысячи одновременных запросов, являясь одним из самых популярных решений в мире. 

**Reverse-proxy** - сервер, который стоит перед вашими сервисами и защищает их. Клиент думает, что общается с прокси, а прокси "под капотом" ходит в бэкенд и возвращает ответ.

- **Upstream** — это "настоящий" сервис, куда прокси пересылает запрос.
- **Routing** (Маршрутизация) — правила: "если пришло `/users`, иди налево; если `/billing`, иди направо".

## Практика

Допустим, мы собираем приложение из двух сервисов: нашего REST API (2 реплики) и базы данных Postgresql:

```
version: "3.9"

services:
  db:
    image: postgres:alpine
    environment:
      POSTGRES_USER: postgress_user
      POSTGRES_PASSWORD: postgress_password
      POSTGRES_DB: books
      PGDATA: /var/lib/postgresql/data
    volumes:
      - pgdata:/var/lib/postgresql/data
  app1:
    build: .
    depends_on:
      - db
    environment:
      DB_NAME: books
      DB_USER: postgress_user
      DB_PASSWORD: postgress_password
      DB_HOST: db
      DB_PORT: 5432

  app2:
    build: .
    depends_on:
      - db
    environment:
      DB_NAME: books
      DB_USER: postgress_user
      DB_PASSWORD: postgress_password
      DB_HOST: db
      DB_PORT: 5432
```

Мы можем добавить в этот набор nginx, который бы проксировал запросы с хоста в контейнеры. Nginx будет спокойно видеть остальные 
контейнеры, т.к при сборке с помощью docker compose все контейнеры объединяются в одну сеть, а название сервисов резолвится в IP
контейнера (имеется свой DNS).

```
  nginx:
    image: nginx
    ports:
      - "8500:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
```

Берем дефолтный образ nginx, прокидываем порт 80 (на этом порте nginx работает внутри контейнера) на порт 8500 хоста.
Также делаем volume, чтобы nginx подхватывал конфиг "./nginx.conf" на хосте и писал его в /etc/nginx/conf.d/default.conf контейнера. default.conf сам по себе не является конфигом nginx, это просто файл, который с помощью include подключается в основной config nginx.

Дефолтный конфиг nginx:
```
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

Последней строчкой идет подключение конфига, который мы подменяем.


Теперь нужно написать конфиг nginx, который мы будем передавать в контейнер:


```
server {
    location /api/v1/resource/ {
        proxy_pass http://app1:8000/;
    }

    location /api/v1/other/ {
        proxy_pass http://app2:8000/;
    }
}
```

Делаем 2 точки входа: одна для одной реплики приложения, другая - для другой реплики. Если запустить n реплик с помощью
docker compose up --scale app=n и сделать одну точку входа для них, то Nginx будет работать еще и как балансир: он будет балансировать нагркузу, распределяя запросы по репликам.

Теперь, если перейти по адресу "http://localhost:8500" на хосте, то будет обращение к сервису в контейнере, причем контейнеры никак не выходят во внешний мир (я специально убрал проброс портов). Таким образом сами сервисы скрыты от пользователя.

[![image.png](https://i.postimg.cc/Cx0mDFt1/image.png)](https://postimg.cc/PP6Wnkds)