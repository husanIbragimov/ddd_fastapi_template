- make migrations
```bash
alembic revision --autogenerate -m "add_category_model"
```

- apply migrations
```bash
alembic upgrade head
```

- run app
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- view swagger this path
```bash
http://127.0.0.1:8000/docs
```
