# Do not modify the base image
FROM python:3.8-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# FROM django_exercise:latest

# Set the working directory inside the container
RUN mkdir /app
WORKDIR /app

# Copy the files from the current directory into the container's working directory
COPY . /app

# TODO: add dependencies
RUN pip install -r requirements.txt

# TODO: start the Django server
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
