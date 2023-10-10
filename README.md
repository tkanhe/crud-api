### Sample fastapi CRUD project with mongodb

### Quickstart
```
git clone https://github.com/tkanhe/crud-api
cd crud-api
pip install -r requirements.txt
uvicorn main:app --host "localhost" --port 8088
```

- Application will be available on localhost:8088 or 127.0.0.1:8088 in your browser.
- All routes & docs are available on localhost:8088/docs or localhost:8088/redoc paths with Swagger or ReDoc.

### Requirements:
- Python 3.9+
- MongoDB server (running locally, you can modify its host & port in the config.ini)

### How to test:
```
pytest test_main.py
```

