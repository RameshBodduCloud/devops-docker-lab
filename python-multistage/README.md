# Python Flask Application - Docker Multi-Stage Build

## Project Overview

This project demonstrates how to containerize a Python Flask application using Docker Multi-Stage Builds.

A multi-stage Docker build allows us to separate the dependency installation stage from the final application stage.

This helps create cleaner Docker images by copying only the required files and dependencies into the final image.

## Technologies Used

- Python 3.12
- Flask
- Docker
- Docker Multi-Stage Build
- Linux

## Project Structure

```text
python-multistage/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## Step 1: Create Project Directory

```bash
mkdir python-multistage
cd python-multistage
```

## Step 2: Create Python Application

Create a file named `app.py`.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Python Multi-Stage Docker Build!",
        "status": "success"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "message": "Application is healthy"
    })

@app.route("/about")
def about():
    return jsonify({
        "application": "Python Flask App",
        "version": "1.0",
        "docker": "Multi-Stage Build"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## Step 3: Create requirements.txt

Create a file named `requirements.txt`.

```text
Flask==3.1.1
```

This file contains the Python dependencies required by our application.

## Step 4: Create Dockerfile

Create a file named `Dockerfile`.

```dockerfile
# ======================================
# STAGE 1: BUILDER
# ======================================

FROM python:3.12-slim AS builder

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir \
    --prefix=/dependencies \
    -r requirements.txt


# ======================================
# STAGE 2: PRODUCTION
# ======================================

FROM python:3.12-slim AS production

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /dependencies /usr/local

# Copy application
COPY app.py .

# Expose port
EXPOSE 5000

# Start Python application
CMD ["python", "app.py"]
```

### Dockerfile Explanation

#### Stage 1: Builder

```dockerfile
FROM python:3.12-slim AS builder
```

Creates the builder stage using Python 3.12.

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory.

```dockerfile
COPY requirements.txt .
```

Copies the Python dependency file into the container.

```dockerfile
RUN pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.txt
```

Installs dependencies into `/install`.

#### Stage 2: Production

```dockerfile
FROM python:3.12-slim AS production
```

Creates a fresh production stage.

```dockerfile
COPY --from=builder /install /usr/local
```

Copies installed Python dependencies from the builder stage.

```dockerfile
COPY app.py .
```

Copies the Flask application.

```dockerfile
EXPOSE 5000
```

Documents that the application listens on port 5000.

```dockerfile
CMD ["python", "app.py"]
```

Starts the Flask application using Python.

**Note:** This uses Flask's development server and is intended for learning and development, not production deployment.

## Step 5: Create .dockerignore

Create `.dockerignore`.

```text
__pycache__
*.pyc
*.pyo
.env
.venv
venv
.git
.gitignore
Dockerfile*
.dockerignore
```

This prevents unnecessary files from being included in the Docker build context.

## Step 6: Build Docker Image

Run:

```bash
docker build -t python-multistage:v1 .
```

Explanation:

- `docker build` builds the Docker image.
- `-t` assigns a name and tag.
- `python-multistage` is the image name.
- `v1` is the image tag.
- `.` specifies the current directory as the build context.

Check Docker images:

```bash
docker images
```

## Step 7: Run Docker Container

Run:

```bash
docker run -d \
  --name python-container \
  -p 5000:5000 \
  python-multistage:v1
```

Explanation:

- `-d` runs the container in detached mode.
- `--name` assigns a container name.
- `-p 5000:5000` maps host port 5000 to container port 5000.

Check running containers:

```bash
docker ps
```

## Step 8: Test Application

### Home Endpoint

Open:

http://localhost:5000/

Or execute:

```bash
curl http://localhost:5000/
```

Expected output:

```json
{
  "message": "Hello from Python Multi-Stage Docker Build!",
  "status": "success"
}
```

### Health Endpoint

```bash
curl http://localhost:5000/health
```

Expected output:

```json
{
  "message": "Application is healthy",
  "status": "UP"
}
```

### About Endpoint

```bash
curl http://localhost:5000/about
```

Expected output:

```json
{
  "application": "Python Flask App",
  "docker": "Multi-Stage Build",
  "version": "1.0"
}
```

## Step 9: Inspect Docker Container

Enter the running container:

```bash
docker exec -it python-container sh
```

Check the working directory:

```bash
pwd
```

Expected:

```text
/app
```

List application files:

```bash
ls
```

Check installed Python dependencies:

```bash
pip list
```

Check Python version:

```bash
python --version
```

Exit the container:

```bash
exit
```

## Step 10: Build Only the Builder Stage

Docker allows us to build a specific stage using `--target`.

```bash
docker build \
  --target builder \
  -t python-builder:v1 \
  .
```

Check the image:

```bash
docker images
```

Inspect the builder image:

```bash
docker run -it --rm python-builder:v1 sh
```

Check installed dependencies:

```bash
ls /install
```

Exit:

```bash
exit
```

## Step 11: Check Container Logs

```bash
docker logs python-container
```

Follow logs in real time:

```bash
docker logs -f python-container
```

## Step 12: Check Docker Image Layers

```bash
docker history python-multistage:v1
```

This command displays the layers used to create the final Docker image.

## Step 13: Stop and Remove Container

Stop the container:

```bash
docker stop python-container
```

Remove the container:

```bash
docker rm python-container
```

Remove Docker image:

```bash
docker rmi python-multistage:v1
```

## Docker Multi-Stage Build Architecture

```text
                  Docker Build
                       |
                       |
                       v
          +--------------------------+
          |                          |
          |    STAGE 1: BUILDER      |
          |                          |
          |    Python 3.12           |
          |                          |
          |    requirements.txt      |
          |                          |
          |    Install Flask         |
          |                          |
          |    /install              |
          |                          |
          +--------------------------+
                       |
                       |
                       | COPY --from=builder
                       |
                       v
          +--------------------------+
          |                          |
          |   STAGE 2: PRODUCTION    |
          |                          |
          |   Python 3.12            |
          |                          |
          |   Flask Dependencies     |
          |                          |
          |   app.py                 |
          |                          |
          |   CMD python app.py      |
          |                          |
          +--------------------------+
                       |
                       |
                       v
                 Docker Image
                       |
                       |
                       v
                Docker Container
                       |
                       |
                       v
               localhost:5000
```

## Advantages of Multi-Stage Docker Builds

1. Separates dependency installation and application stages.
2. Allows copying only required files into the final image.
3. Helps reduce unnecessary build dependencies.
4. Improves Dockerfile organization.
5. Can reduce final image size.
6. Supports different environments for building and running applications.

## Important Docker Commands

| Command | Description |
|---------|-------------|
| `docker build -t python-multistage:v1 .` | Build Docker image |
| `docker images` | List Docker images |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker logs python-container` | View container logs |
| `docker exec -it python-container sh` | Enter container |
| `docker history python-multistage:v1` | View image layers |
| `docker stop python-container` | Stop container |
| `docker rm python-container` | Remove container |
| `docker rmi python-multistage:v1` | Remove image |

## Key Docker Concepts

### What is a Multi-Stage Docker Build?

A multi-stage Docker build uses multiple `FROM` instructions in a single Dockerfile.

Each `FROM` instruction starts a new build stage.

### What is the Builder Stage?

The builder stage is responsible for installing dependencies and preparing application files.

### What is the Production Stage?

The production stage contains the files and dependencies required to run the application.

### What is COPY --from=builder?

```dockerfile
COPY --from=builder /install /usr/local
```

It copies files from the builder stage into the production stage.

### What is CMD?

```dockerfile
CMD ["python", "app.py"]
```

It specifies the default command executed when the Docker container starts.

### What is EXPOSE?

```dockerfile
EXPOSE 5000
```

It documents the port used by the application.

Port publishing is configured separately using `docker run -p`.

## Conclusion

In this project, we successfully:

- Created a Python Flask application.
- Created a Dockerfile using two stages.
- Installed Python dependencies in the builder stage.
- Copied dependencies into the final stage.
- Built a Docker image.
- Ran a Docker container.
- Tested Flask API endpoints.
- Inspected Docker images and containers.

This project demonstrates the fundamentals of Docker Multi-Stage Builds using Python Flask.

## Author
Ramesh Boddu
Docker Multi-Stage Build Practice Project

Technology: Python | Flask | Docker | DevOps
