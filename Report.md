# Создание API на fastAPI + strawberry-graphql

## Определения

**strawberry-graphql** - современная, ориентированная на типы (code-first) библиотека для создания GraphQL API на Python, основанная на датаклассах (dataclasses) и аннотациях типов. Она ориентирована на удобство разработчиков, поддерживает асинхронность (asyncio) и легко интегрируется с фреймворками вроде FastAPI, Django и Flask.

![](https://thepythoncode.com/media/articles/build-a-graphql-api-with-fastapi-strawberry-and-postgres-python/img001.webp)

При работе с graphql сначала создается graphql-scheme, а потом делается реализация.

**Graphql scheme** — это структура всего GraphQL API. Она описывает типы данных (Type), способы получения данных (Query) и изменения данных (Mutation).

Пример схемы для API можно найти в /weeks/week_05/app

Реализация схемы находится в /weeks/week_05/app

