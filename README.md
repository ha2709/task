docker build -t task-api .
docker run -p 8000:8000 task-api


source env/bin/activate

uvicorn src.main:app --reload

 pytest -s src/test/test_api.py -k test_create_task_endpoint

alembic revision --autogenerate -m "Initial migration"

alembic upgrade head

