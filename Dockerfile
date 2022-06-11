FROM python:3.9-slim
ADD incidents /incidents
ADD LICENSE /LICENSE
ADD manage.py /manage.py
ADD requirements.txt /requirements.txt
ADD README.md /README.md

RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver"]

