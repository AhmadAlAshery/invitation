FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y vim \
    gcc \
    build-essential \
    python3-dev \
    fonts-liberation

COPY ./app .

RUN pip install -r requirements.txt

CMD ["bash", "init.sh"]
# CMD ["tail", "-f", "/dev/null"]
