FROM python:3.10.11-slim-bullseye

ENV PROJECT_DIR=/app
WORKDIR $PROJECT_DIR

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src
COPY resources resources

WORKDIR $PROJECT_DIR/src

ENTRYPOINT ["uvicorn", "project.server:app"]
