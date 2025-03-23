set windows-shell := ["pwsh.exe", "-c"]
set dotenv-filename := ".env"

export PYTHONPATH := "src"

run:
    uv run python src/main.py

run-docker:
    docker-compose up --build

start-tsk-worker:
    taskiq worker -fsd src.integrations.taskiq.broker:taskiq_broker  src.integrations.taskiq.worker_tasks  -w 1 --max-fails 2

start-tsk-scheduler:
    taskiq scheduler -fsd src.integrations.taskiq.broker:taskiq_scheduler src.integrations.taskiq.scheduled_tasks

test path="tests":
    uv run pytest {{ path }}

pre-commit-all:
    pre-commit run --all-files --show-diff-on-failure

alembic-gen:
    alembic revision --autogenerate

alembic-upg revision="head":
    alembic upgrade {{ revision }}

alembic-drop revision="base":
    alembic downgrade {{ revision }}

recreate-db: alembic-drop && alembic-gen
