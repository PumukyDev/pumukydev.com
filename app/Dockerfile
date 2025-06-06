FROM python:alpine3.22

WORKDIR /app

RUN apk update && apk upgrade && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    py3-pip \
    dcron

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY crontab.txt /etc/crontabs/root

RUN chmod +x update_projects.py

CMD ["/bin/sh", "-c", "python update_projects.py && crond && gunicorn -b 0.0.0.0:5000 main:app"]
