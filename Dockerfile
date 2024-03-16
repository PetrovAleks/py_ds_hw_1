FROM python:3.10

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry install

COPY . /app/

CMD ["poetry", "run", "start"]