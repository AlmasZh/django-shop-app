FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000


# RUN python manage.py migrate
# RUN python manage.py create_default_user
RUN python manage.py collectstatic --noinput

ENV DEBUG=False


# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
# CMD gunicorn shopApp.wsgi:application --bind 0.0.0.0:8000 --workers 3