# Docker Compose Setup for Flask + MySQL Application

This guide explains how to create and run a Docker Compose setup for the Flask + MySQL two-tier application.

**Project Repository:**
[https://github.com/agravi987/docker-based-two-tier-flask-mysql-app](https://github.com/agravi987/docker-based-two-tier-flask-mysql-app)

## 1. Verify Docker Installation

First, check whether Docker is installed:

```bash
docker --version
```

Check running containers:

```bash
docker ps
```

Check available images:

```bash
docker images
```

## 2. Install Docker Compose

If the `docker compose` command does not work, install Docker Compose:

```bash
sudo apt update
sudo apt install docker-compose
```

Verify installation:

```bash
docker-compose --version
```

## 3. Navigate to Project Directory

Clone the repository (if not already cloned):

```bash
git clone https://github.com/agravi987/docker-based-two-tier-flask-mysql-app.git
```

Move into the project directory:

```bash
cd docker-based-two-tier-flask-mysql-app
```

Check project files:

```bash
ls
```

## 4. Create `docker-compose.yml` File

Create the compose file:

```bash
vim docker-compose.yml
```

Add the following configuration:

```yaml
version: "3.8"

services:

  mysql:
    image: mysql:8
    container_name: mysql-container
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: todo_db
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - two-tier-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  flask-app:
    build: .
    container_name: flask-container
    ports:
      - "8080:8080"
    environment:
      DB_HOST: mysql
      DB_USER: root
      DB_PASSWORD: password
      DB_NAME: todo_db
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - two-tier-network

volumes:
  mysql-data:

networks:
  two-tier-network:
```

Save the file:

```text
ESC → :wq
```

## 5. Verify `docker-compose.yml`

Check file content:

```bash
cat docker-compose.yml
```

## 6. Run Docker Compose (Using sudo)

Since the user may not have Docker socket permission, run Compose using `sudo`.

Start the application:

```bash
sudo docker-compose up -d
```

This will:
- Build Flask image
- Pull MySQL image
- Create network
- Create volume
- Start containers

## 7. Verify Running Containers

Check containers:

```bash
sudo docker ps
```

Expected containers:
- `mysql-container`
- `flask-container`

## 8. Test the Application

Run:

```bash
curl localhost:8080
```

Or open in browser:

```text
http://EC2-PUBLIC-IP:8080
```

Example:

```text
http://3.85.12.88:8080
```

## 9. Check Logs (If Needed)

Flask logs:

```bash
sudo docker logs flask-container
```

MySQL logs:

```bash
sudo docker logs mysql-container
```

## 10. Stop the Application

To stop containers:

```bash
sudo docker-compose down
```

## 11. Verify Volume Persistence

Check volumes:

```bash
sudo docker volume ls
```

Inspect volume:

```bash
sudo docker volume inspect mysql-data
```

This ensures MySQL data persists even if containers restart.

## 12. Clean Up (Optional)

Remove containers and volumes:

```bash
sudo docker-compose down -v
```