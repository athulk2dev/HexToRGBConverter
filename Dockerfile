FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code/
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt

