# Node.js Application - Docker Multi-Stage Build

## Project Overview

This project demonstrates how to containerize a Node.js application using Docker Multi-Stage Builds.

A multi-stage Docker build allows us to separate the dependency installation stage from the final application stage.

This helps create cleaner Docker images by copying only the required files and dependencies into the final image.

## Technologies Used

- Node.js (v18)
- Express
- Docker
- Docker Multi-Stage Build
- Linux

## Project Structure

```text
node-multistage/
│
├── server.js
├── package.json
├── Dockerfile
├── .dockerignore
└── README.md
```

## Step 1: Create Project Directory

```bash
mkdir node-multistage
cd node-multistage
```

## Step 2: Create Node.js Application

Create a file named `server.js`.

```javascript
const express = require("express");

const app = express();

const PORT = 3000;

app.get("/", (req, res) => {
  res.send("Hello from Node.js Multi-Stage Docker Build!");
});

app.get("/health", (req, res) => {
  res.json({
    status: "UP",
    message: "Application running successfully"
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
```

Our application has two endpoints:

```text
http://localhost:3000

http://localhost:3000/health
```

## Step 3: Create package.json

Create a file named `package.json`.

```json
{
  "name": "node-multistage-demo",
  "version": "1.0.0",
  "description": "Docker Multi Stage Build Practice - Node.js",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.21.2"
  }
}
```

Here:
- `express` is required to run the application.
- `start` script runs our Node.js application.

## Step 4: Create Dockerfile

Create a file named `Dockerfile`.

```dockerfile
# ==========================================
# STAGE 1: BUILDER
# ==========================================

FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first (layer caching)
COPY package*.json ./

# Install ALL dependencies (including devDependencies)
RUN npm install

# Copy source code
COPY . .

# ==========================================
# STAGE 2: PRODUCTION
# ==========================================

FROM node:18-alpine AS production

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ONLY production dependencies
RUN npm install --omit=dev

# Copy application from builder stage
COPY --from=builder /app/dist ./dist

# Expose application port
EXPOSE 3000

# Use non-root user for security
USER node

# Start application
CMD ["node", "server.js"]
```

### Dockerfile Explanation

#### Stage 1: Builder

```dockerfile
FROM node:18-alpine AS builder
```

Creates the builder stage using Node.js 18 Alpine.

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory.

```dockerfile
COPY package*.json ./
```

Copies `package.json` and `package-lock.json` into the container.

```dockerfile
RUN npm install
```

Installs all dependencies (including devDependencies for build).

```dockerfile
COPY . .
```

Copies source code into the container.

#### Stage 2: Production

```dockerfile
FROM node:18-alpine AS production
```

Starts a fresh Node.js image for production.

```dockerfile
RUN npm install --omit=dev
```

Installs only production dependencies. Development tools are excluded.

```dockerfile
COPY --from=builder /app/dist ./dist
```

**This is the most important instruction in a multi-stage build.**

It copies the application files from the builder stage into the production stage.

The final image does not contain the builder stage's complete filesystem.

```dockerfile
USER node
```

Runs the application as a non-root user for better security.

```dockerfile
CMD ["node", "server.js"]
```

Starts the Node.js application.

**Note:** This uses Node.js's built-in server and is intended for learning and development, not production deployment with process managers like PM2.

## Step 5: Create .dockerignore

Create `.dockerignore`.

```text
node_modules
npm-debug.log
.git
.gitignore
Dockerfile*
.dockerignore
```

This prevents unnecessary files from being included in the Docker build context.

## Step 6: Build Docker Image

Run:

```bash
docker build -t node-multistage:v1 .
```

Explanation:

- `docker build` builds the Docker image.
- `-t` assigns a name and tag.
- `node-multistage` is the image name.
- `v1` is the image tag.
- `.` specifies the current directory as the build context.

Check Docker images:

```bash
docker images
```

Expected format:

```text
REPOSITORY          TAG    SIZE
node-multistage     v1     ...
```

## Step 7: Run Docker Container

Run:

```bash
docker run -d \
  --name node-container \
  -p 3000:3000 \
  node-multistage:v1
```

Explanation:

- `-d` runs the container in detached mode.
- `--name` assigns a container name.
- `-p 3000:3000` maps host port 3000 to container port 3000.

Check running containers:

```bash
docker ps
```

Expected format:

```text
CONTAINER ID   IMAGE                 PORTS
abc123         node-multistage:v1    0.0.0.0:3000->3000/tcp
```

## Step 8: Test Application

### Home Endpoint

Open:

http://localhost:3000

Or execute:

```bash
curl http://localhost:3000/
```

Expected output:

```text
Hello from Node.js Multi-Stage Docker Build!
```

### Health Endpoint

```bash
curl http://localhost:3000/health
```

Expected output:

```json
{
  "status": "UP",
  "message": "Application running successfully"
}
```

## Step 9: Inspect Docker Container

Enter the running container:

```bash
docker exec -it node-container sh
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

Check Node.js version:

```bash
node --version
```

Check installed packages:

```bash
npm list
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
  -t node-builder:v1 \
  .
```

Check the image:

```bash
docker images
```

Inspect the builder image:

```bash
docker run -it --rm node-builder:v1 sh
```

Check installed dependencies:

```bash
ls node_modules
```

Exit:

```bash
exit
```

## Step 11: Check Container Logs

```bash
docker logs node-container
```

Follow logs in real time:

```bash
docker logs -f node-container
```

## Step 12: Check Docker Image Layers

```bash
docker history node-multistage:v1
```

This command displays the layers used to create the final Docker image.

## Step 13: Stop and Remove Container

Stop the container:

```bash
docker stop node-container
```

Remove the container:

```bash
docker rm node-container
```

Remove Docker image:

```bash
docker rmi node-multistage:v1
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
          |    Node.js 18            |
          |                          |
          |    package.json          |
          |                          |
          |    npm install           |
          |                          |
          |    node_modules          |
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
          |    Node.js 18            |
          |                          |
          |    Production deps       |
          |                          |
          |    server.js             |
          |                          |
          |    CMD node server.js    |
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
               localhost:3000
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
| `docker build -t node-multistage:v1 .` | Build Docker image |
| `docker images` | List Docker images |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker logs node-container` | View container logs |
| `docker exec -it node-container sh` | Enter container |
| `docker history node-multistage:v1` | View image layers |
| `docker stop node-container` | Stop container |
| `docker rm node-container` | Remove container |
| `docker rmi node-multistage:v1` | Remove image |

## Key Docker Concepts

### What is a Multi-Stage Docker Build?

A multi-stage Docker build uses multiple `FROM` instructions in a single Dockerfile.

Each `FROM` instruction starts a new build stage.

### What is the Builder Stage?

The builder stage is responsible for installing dependencies and preparing application files.

### What is the Production Stage?

The production stage contains the files and dependencies required to run the application.

### What is `COPY --from=builder`?

```dockerfile
COPY --from=builder /app/dist ./dist
```

It copies files from the builder stage into the production stage.

### What is CMD?

```dockerfile
CMD ["node", "server.js"]
```

It specifies the default command executed when the Docker container starts.

### What is EXPOSE?

```dockerfile
EXPOSE 3000
```

It documents the port used by the application.

Port publishing is configured separately using `docker run -p`.

## Conclusion

In this project, we successfully:

- Created a Node.js Express application.
- Created a Dockerfile using two stages.
- Installed Node.js dependencies in the builder stage.
- Copied dependencies into the final stage.
- Built a Docker image.
- Ran a Docker container.
- Tested Node.js API endpoints.
- Inspected Docker images and containers.

This project demonstrates the fundamentals of Docker Multi-Stage Builds using Node.js Express.

## Author

Docker Multi-Stage Build Practice Project

Technology: Node.js | Express | Docker | DevOps
