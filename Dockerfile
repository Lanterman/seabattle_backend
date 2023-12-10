# syntax=docker/dockerfile:1
FROM python:3.10

# work direction
WORKDIR /app/backend
RUN mkdir -p $WORKDIR/media

# enviroment to python
# don't create cash file .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# don't buffer stdout and stderr streams
ENV PYTHONUNBUFFERED=1

# update pip
RUN pip install --upgrade pip

# 
RUN pip install --default-timeout=100 future

# copy and install requirement
# caching dependencies and the layer will be reloaded when requiremtns.txt changes
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy what's left
COPY . .
