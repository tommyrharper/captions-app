# Captions App

## Docker container

Before hotmodule reloading it looked like this:
```yml
version: '3'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000" 
```

How to build and deploy on remote machine:

```bash
docker login -u username
docker build --platform linux/amd64 -t zeroknowledgeltd/captions-app-frontend:latest ./frontend
docker build --platform linux/amd64 -t zeroknowledgeltd/captions-app-backend:latest ./backend
docker push zeroknowledgeltd/captions-app-frontend:latest
docker push zeroknowledgeltd/captions-app-backend:latest
```