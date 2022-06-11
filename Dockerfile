FROM python:3.9-slim
EXPOSE 8000
RUN useradd -ms /bin/bash incidents

USER incidents
WORKDIR /app
ENV PATH="${PATH}:/home/incidents/.local/bin"
ADD LICENSE /app/LICENSE
ADD README.md /app/README.md
ADD manage.py /app/manage.py
ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
ADD incidents /app/incidents
CMD python manage.py migrate ; gunicorn -b 0.0.0.0:8000 incidents.wsgi --access-logfile - --error-logfile -