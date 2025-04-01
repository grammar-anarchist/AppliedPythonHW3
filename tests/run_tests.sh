#!/bin/bash
cd "$(dirname "$0")/.."

alembic upgrade head

PYTHONPATH=src coverage run --parallel-mode --source=src src/main.py &
APP_PID=$!

PYTHONPATH=src coverage run --parallel-mode --source=src -m celery -A tasks.tasks.celery_app worker --loglevel=info &
CELERY_PID=$!

until curl -s http://localhost:8000/docs > /dev/null; do sleep 1; done;

pytest tests -v --color=yes

kill -SIGINT $APP_PID
kill -SIGINT $CELERY_PID
wait $APP_PID
wait $CELERY_PID

coverage combine
coverage report -m
coverage html
