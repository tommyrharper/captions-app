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
