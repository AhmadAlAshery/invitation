FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y vim \
    gcc \
    build-essential \
    python3-dev \
    fonts-liberation

COPY ./app .

RUN pip install -r requirements.txt

# RUN alembic revision --autogenerate -m "Start"
# RUN alembic upgrade head


# CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
CMD ["bash", "init.sh"]
