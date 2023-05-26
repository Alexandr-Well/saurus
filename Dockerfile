FROM python:3.10-slim

# set work directory
WORKDIR /src

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/src

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN chmod a+x /src/docker_commands/gunicorn.sh

