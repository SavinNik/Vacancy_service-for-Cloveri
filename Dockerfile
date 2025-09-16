# Versions
ARG PYTHON=python:3.12-alpine
## Stage one ##
FROM $PYTHON AS build
WORKDIR /usr/app
ARG BUILD_VERSION

# Установка C зависимостей
RUN apk add --no-cache --update \
            gcc \
            g++ \
            libc-dev \
            linux-headers \
            libffi-dev \
            libstdc++

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV="/usr/app/venv"

# Установка зависимостей python
RUN pip install uv

RUN uv venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"
COPY requirements.txt .
RUN uv pip install --no-cache -r requirements.txt

## Stage two ##
FROM $PYTHON AS runtime
ARG BUILD_VERSION

RUN apk add --no-cache libstdc++

# Установка зависимостей C, создание пользователя
RUN adduser -D cobra \
 && mkdir /usr/app \
 && chown cobra:cobra /usr/app
WORKDIR /usr/app

# Подготовка кода и окружения
COPY --chown=cobra:cobra --from=build /usr/app/venv ./venv
COPY --chown=cobra:cobra . .

# Settings
USER cobra
ENV VIRTUAL_ENV="/usr/app/venv"
ENV PATH="/usr/app/venv/bin:$PATH"
EXPOSE 80

# Переменные среды
ENV BUILD_VERSION=${BUILD_VERSION:-noversion}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Metadata
LABEL app.version="${BUILD_VERSION}"

# Запуск
ENTRYPOINT ["uvicorn", "a.main:app", "--host", "0.0.0.0"]
CMD ["--port", "80", "--proxy-headers"]
