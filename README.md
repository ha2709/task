docker build -t task-api .
docker run -p 8000:8000 task-api


https://chatgpt.com/c/67414176-fca8-8004-8233-fafc03cdc0b7

`https://chatgpt.com/c/673f062a-7a78-8004-9002-8eb093159f4e`

source env/bin/activate

uvicorn src.main:app --reload

 pytest -s src/test/test_api.py -k test_create_task_endpoint

alembic revision --autogenerate -m "Initial migration"

alembic upgrade head

