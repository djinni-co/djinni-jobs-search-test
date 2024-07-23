FROM python:3.12.4-bookworm

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install postgresql-client -y

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

# Expose the port that the application will run on
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "localhost:8000"]
