# Use the base image for Django
FROM python:3.12-slim

# Install netcat-openbsd and other necessary tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app and the wait-for-it script into the container
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8000

# Set the entrypoint for Django, ensuring the database is ready
CMD ["sh", "-c", "/app/wait-for-it.sh db:5432 -- python manage.py migrate --noinput && python manage.py seed_cars && gunicorn djangobackend.wsgi:application --bind 0.0.0.0:8000"]
