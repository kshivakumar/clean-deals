FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./clean_deals /app/clean_deals
COPY ./manage.py /app/

RUN mkdir /app/staticfiles

EXPOSE 8000

CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn --workers 3 --preload --bind 0.0.0.0:8000 --access-logfile - clean_deals.wsgi:application