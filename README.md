# FastAPI And Alembic Template Project
## Installation
```
git clone https://github.com/isOwn3n/fastapi_template.git
cd fastapi_template
pip install -r requirements.txt
```
## Configure

### Create Alembic Initial Migrations Using Async Template
```
alembic init -t async migrations
```

### Add SQLModel To Migrations
**`script.py.mako:`**
```
...
import sqlmodel # import sqlmodel library
${imports if imports else ""}
...
```

## Making Migrations in Alembic
### Create Migration
```
alembic revision --autogenerate -m "migration message"
```
### Migrate The Migration File
```
alembic upgrade head
```

## Run App
### Run App Using
```
python app.py
```
### Or
```
python3 app.py
```

## Notes

> [!NOTE]
> This Project is A Sample Structure FastAPI Project With Alembic and SQLModel and AsyncPG to Can Handle Database With Async.

> [!WARNING]
> Dont Publish This Template On Github.
