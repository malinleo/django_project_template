FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements/development.txt /code/
RUN pip install -r development.txt
COPY . /code/