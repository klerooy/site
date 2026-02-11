FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ENV PORT=8000 \
    MODULE_NAME=app.main \
    VARIABLE_NAME=app

WORKDIR /app

COPY app /app/app

EXPOSE 8000
