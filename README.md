# Flask App with Celery and Redis

This is a sample application using Flask, Celery, and Docker. The application allows users to upload an image, which is then resized in the background using Celery. The resized image can be downloaded afterward.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Step 1: Clone the repository

```bash
git clone https://github.com/thiagojordao98/resize-img-upload
cd <resize-img-upload>
```

### Step 2: Build and run the Docker containers

```bash
docker-compose up --build -d
```

This will start three services:
1. `web` - The Flask application running on port 5000.
2. `worker` - The Celery worker to process background tasks.
3. `redis` - Redis server used as the message broker for Celery.

### Step 3: Access the application

Open your web browser and go to `http://localhost:5000`. You should see the application running.

### Step 4: Upload an image

1. Go to `http://localhost:5000/upload`.
2. Use the form to upload an image.

### Step 5: Download the resized image

Once the image is processed, you can download it from `http://localhost:5000/resized_<filename>`, replacing `<filename>` with the original filename of the uploaded image.

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── app.py
└── uploads/
```

- `Dockerfile`: Defines the Docker image for the Flask application.
- `docker-compose.yml`: Defines the services for Docker Compose.
- `app.py`: The Flask application code.
- `uploads/`: Directory where uploaded and resized images are stored.

### app.py

The `app.py` file contains the Flask application and Celery configuration.

- `/`: Serves the `index.html` file.
- `/upload`: Endpoint to upload an image.
- `/resized_<filename>`: Endpoint to download the resized image.

The `resize_image_task` function handles the image resizing process in the background using Celery.

## Conclusion

You have now set up a Flask application with Celery for background task processing, running inside Docker containers. This setup allows you to easily manage and scale the application.
