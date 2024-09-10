FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./clean_deals /app/clean_deals
COPY ./manage.py /app/
COPY ./start.sh /app/

RUN mkdir /app/staticfiles

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]