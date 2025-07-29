FROM tiangolo/uvicorn-gunicorn:python3.11

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y curl

WORKDIR /project

RUN pip install poetry==2

ENV POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./
# RUN poetry add opentelemetry-distro opentelemetry-exporter-otlp
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

