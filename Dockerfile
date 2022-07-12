FROM python:3.9-alpine
EXPOSE 8000
RUN apk update
RUN apk add libpq-dev build-essential -y
RUN useradd -ms /bin/bash incidents

USER incidents
WORKDIR /app
ENV PATH="${PATH}:/home/incidents/.local/bin"
COPY LICENSE /app/LICENSE
COPY README.md /app/README.md
COPY manage.py /app/manage.py
COPY gunicorn.conf.py /app/gunicorn.conf.py
COPY requirements.txt /app/requirements.txt
COPY templates /app/templates

RUN pip install -r requirements.txt
COPY incidents /app/incidents
CMD gunicorn -c /app/gunicorn.conf.py