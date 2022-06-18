FROM python:3.9-slim
EXPOSE 8000
RUN apt-get update
RUN apt-get install libpq-dev build-essential -y
RUN useradd -ms /bin/bash incidents
USER incidents
WORKDIR /app
ENV PATH="${PATH}:/home/incidents/.local/bin"
ADD LICENSE /app/LICENSE
ADD README.md /app/README.md
ADD manage.py /app/manage.py
ADD gunicorn.conf.py /app/gunicorn.conf.py
ADD requirements.txt /app/requirements.txt
ADD templates /app/templates

RUN pip install -r requirements.txt
ADD incidents /app/incidents
CMD gunicorn -c /app/gunicorn.conf.py