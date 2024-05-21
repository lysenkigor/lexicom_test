FROM python:3.12.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR on
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV POETRY_VERSION 1.7.1

WORKDIR /app

RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-root
COPY . .
ENTRYPOINT gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind unix:/tmp/fastapi.sock src.entrypoint:app