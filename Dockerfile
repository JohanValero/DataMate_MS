FROM python:3.10.5-slim-bullseye

RUN mkdir wd
WORKDIR /wd

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir resources

COPY src/ ./

# docker build -t flask_app .
# docker image ls
# docker run -e DB_HOST=localhost -e DB_PORT=3306 -e DB_USER=DEV_USER -e DB_PASW=CalleFalsa123 -e DB_SCHM=DEV_SCHEMA -e PORT=80 -p 80:80 flask_app

CMD exec gunicorn --workers=2 --threads=2 -b :$PORT main:gApp