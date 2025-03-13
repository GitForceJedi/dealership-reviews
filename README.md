🚀 Project Overview & Deployment Summary
This project is a full-stack web application for Car Reviews, featuring user authentication, review submissions, and dealership data integration. It is built using Django for the backend/frontend, a Node.js API for dealership data retrieval, and a Python API for handling user-generated reviews. The application is powered by a PostgreSQL database for structured data storage and IBM Cloudant (NoSQL) for document-based storage.

🔹 Functionality & Authentication
Car Reviews: Users can browse dealerships and leave reviews about their experiences.
Authentication: A user must be logged in to submit a review. Unauthenticated users cannot post reviews.
Node.js API: Fetches dealership data from an external source.
Python API: Manages and processes user reviews.
Django Backend: Manages authentication, user sessions, and integrates data from the APIs.

🔹 Deployment & Infrastructure
The project is containerized using Docker and deployed on Render for seamless scalability.

Django Backend & Frontend: Deployed as a containerized service.
PostgreSQL Server: Hosted on Render's managed PostgreSQL for structured data storage.
IBM Cloudant: Used as a NoSQL database for document storage and caching.
Node & Python APIs: Deployed as independent services, facilitating a microservices architecture.
This multi-layered architecture ensures high availability, scalability, and a seamless user experience for car enthusiasts and potential buyers. 🚀

(There is a docker-compose file that can be used to deploy all services locally)

If you have the required services, the required .env variables are as follows: 

# PostgreSQL Configuration
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# Django Configuration
DATABASE_URL=

DJANGO_SECRET_KEY=
DEBUG=True

#node / python configuration
NODE_ENV=production
CLOUDANT_USERNAME =
CLOUDANT_API_KEY =
CLOUDANT_URL =

The docker-compose file will use these variables to deploy the solution in Docker using your services and credentials.
