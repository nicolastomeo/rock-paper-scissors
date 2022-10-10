FROM python:3.9 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
COPY --from=requirements-stage /tmp/pyproject.toml /code/pyproject.toml
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./alembic.ini /code/alembic.ini
COPY ./.env /code/.env
CMD alembic upgrade head && \
    uvicorn --host=0.0.0.0 --port=80 app.main:app
