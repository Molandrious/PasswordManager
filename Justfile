set windows-shell := ["pwsh.exe", "-c"]
set dotenv-filename := ".env"

export PYTHONPATH := "src"

remove := if "$(expr substr $(uname -s) 1 5)" == "Linux" { "rm -rf" } else { "rmdir" }

run:
   uv run python src/main.py

run-docker:
   docker-compose up --build

start-tsk-worker:
    taskiq worker -fsd src.transport.taskiq.broker:broker  src  -w 1 --max-fails 1

start-tsk-scheduler:
    taskiq scheduler -fsd src.transport.taskiq.broker:scheduler

test path="tests":
    uv run pytest {{path}}

pre-commit-all:
    pre-commit run --all-files --show-diff-on-failure

alembic-gen:
    alembic revision --autogenerate

alembic-upg:
    alembic upgrade head

alembic-drop:
	alembic downgrade base

recreate-db: alembic-drop && alembic-gen
