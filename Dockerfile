FROM python:3.12-slim

RUN apt-get update

ENV PYTHONPATH /app
WORKDIR /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY src src

RUN uv sync --no-dev

CMD ["uv", "run", "--no-dev", "src/main.py"]



