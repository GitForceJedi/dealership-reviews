# For the Django service (using Gunicorn to serve the app)

web: gunicorn --bind 0.0.0.0:$PORT --workers 3 djangobackend.wsgi

# For the Node.js service (assuming entry point is get-dealership.js)

functions: node functions/get-dealership.js
