FROM python:3.12.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git libpq-dev gcc
RUN rm -rf /app/uba-leitor
RUN git clone https://github.com/vandersoncurty/uba-leitor.git .
RUN git pull origin main
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

