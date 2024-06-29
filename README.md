![repo size](https://img.shields.io/github/repo-size/foxygen-d/cat_charity_fund)
![py version](https://img.shields.io/pypi/pyversions/3)
-----
[![Python](https://img.shields.io/badge/Python-3.9|3.10|3.11-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![pydantic](https://img.shields.io/badge/pydantic-2.6.3-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/pydantic/2.6.3/)
[![backoff](https://img.shields.io/badge/backoff-2.2.1-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/backoff/2.2.1/)
[![elasticsearch](https://img.shields.io/badge/elasticsearch-8.12.1-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/elasticsearch/8.12.1/)
[![Fastapi](https://img.shields.io/badge/fastapi-0.110.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/fastapi/0.110.0/)
[![uvicorn](https://img.shields.io/badge/uvicorn-0.28.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/uvicorn/0.28.0/)
[![gunicorn](https://img.shields.io/badge/gunicorn-21.2.0-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/gunicorn/21.2.0/)
[![redis](https://img.shields.io/badge/redis-5.0.3-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/redis/5.0.3)
---
[![Poetry](https://img.shields.io/badge/Poetry-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/poetry/)
[![Ruff](https://img.shields.io/badge/Ruff-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/ruff/)
[![pre-commit](https://img.shields.io/badge/pre_commit-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/pre_commit/)
[![Mypy](https://img.shields.io/badge/Mypy-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/mypy/)


## Описание

Сервис выдачи контента


## Инструкция по развёртыванию проекта

* клонировать проект на компьютер
    ```bash
    git clone git@github.com:MultikPatin/content_service.git
    ```
* Установить менеджер зависимостей poetry
    ```bash
    python -m pip install poetry
    ```
* запуск виртуального окружения
    ```bash
    poetry shell
    ```
* установить зависимости
    ```bash
    poetry install --all-extras --with dev --with test
    ```
Сервис реализован в контейнерах Docker  

* запуск docker-compose
    ```bash
    docker-compose up -d -f docker-compose.local.yml
    ```
Для выполнения тестов в контейнерах Docker  

* запуск docker-compose
    ```bash
    docker-compose up -d -f docker-compose.test.yml
    ```
