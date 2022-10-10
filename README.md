# Rock paper scissors app
FastAPI-AsyncPG application to play rock paper scissors.

## Description

REST API to play rock paper scissors.

Swagger docs available at /docs.

There are two resources (and two DB tables), games and turns.

A game can be created with a POST request (/games) providing player_one and player_two name or only player_one to play against computer.

A turn can be created with a POST request (/games/{game_id}/turns) providing the game id.

Then a turn can be play with a PATCH request (/games/{game_id}/turns/{turn_id}) providing game id, turn id, and one or both of the player moves.
Only when both player moves are stored the game score is updated (available at GET /games/{game_id}) and the turn result can be computed (available at GET /games/{game_id}/turns/{turn_id}/result)

## Run

```
docker-compose up --build
```
This command starts a PostgreSQL DB (exposed on port 5434), run database Alembic migrations and start the API exposed on port 8000

## Local Development

This project was developed with Python 3.9 and Poetry.
Install Poetry (configure local virtualenv is recommended too) and then run
```
poetry install
```
to install all dependencies.

Activate poetry virtualenv, configure .env file (.example-env provided) and then run
```
uvicorn app.main:app
```

to start application.

Run tests with command:
```
pytest
```

## Implementation details

This API is a fully asynchronous FastAPI (ASGI) using AsyncPG as database driver.
It also uses SQLAlchemy as ORM.

This means every HTTP requests runs on a AsyncIO coroutine and database queries are awaited.
This provides a huge performance and efficiency gain over WSGI applications (where every request is processed on a thread) since this API is I/O bounded.

In terms of Database design, something to keep in mind is since player_one and player_two are columns of game table, extending the system to support multiple players would be more difficult. It was designed this way for simplicity.

## Future work

- First more testing is required. There is currently only 2 simple unit tests just for the sake of setting up pytest.

- Observability could be improved adding more logging and Sentry for instance for monitoring.

- Continuous integration, a Jenkinsfile for instance.

- Semantic versioning.

- There is already a Dockerfile for deployment, but a helm chart could be provided to define a Kubernetes deployment

- Terraform module could be added to provison infrastructure.
