FROM python:3.10.13-alpine
#WORKDIR ./teste
#COPY ../src ./src
#COPY ../pyproject.toml ./
#COPY ../poetry.lock ./
#COPY ../README.md ./
WORKDIR /app
COPY ./src ./src
COPY ./pyproject.toml ./
COPY ./poetry.lock ./
COPY ./README.md ./

RUN pip install --upgrade pip
RUN pip install -U pip setuptools
RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction

CMD ["poetry", "run", "python", "src/connection.py"]

# docker build -t radar-do-congresso -f ./docker/Dockerfile .
# docker run radar-do-congresso
