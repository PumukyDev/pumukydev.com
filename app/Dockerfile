FROM python:alpine3.22

WORKDIR /app

COPY crontab.txt /etc/crontabs/root

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    py3-pip \
    dcron

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x update_projects.py entrypoint.sh

CMD ["./entrypoint.sh"]

