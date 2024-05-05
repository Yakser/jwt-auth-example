FROM python:3.12
# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore
# Создание рабочего каталога
RUN mkdir /code
WORKDIR /code
# Копирование файлов проекта
COPY . /code/
COPY .env /code/
# Установка зависимостей проекта
RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN pip install --upgrade djangorestframework-simplejwt
RUN pip install djangorestframework
RUN pip install django
RUN pip install python-decouple
RUN pip install drf-yasg
RUN pip install django-cors-headers
RUN poetry lock --no-update
RUN poetry install --no-root
# Запуск сервера
CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000