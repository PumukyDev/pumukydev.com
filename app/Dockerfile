FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Instala cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copia crontab
COPY crontab.txt /etc/cron.d/update-cron

# Aplica permisos y registra la crontab
RUN chmod 0644 /etc/cron.d/update-cron && crontab /etc/cron.d/update-cron

# Ejecuta el script al levantar y luego inicia cron + Flask en paralelo
CMD python update_projects.py && cron && flask --app main run --host=0.0.0.0
