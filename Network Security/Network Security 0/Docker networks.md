You have two directories with two images: frontend and backend.
You don’t (and you shouldn’t) need to see what is inside those directories, you just need to know there is a Dockerfile for each directory.
In order to get the flag you need to:
Build and deploy the frontend and backend images on the same network.
They need to communicate with each other.
Set the hostname of backend as backend.
Expose the frontend port 80 to any of your local ports.
Navigate (curl is enough) to ‘/flag‘ from your local pc to get the flag.
You can use docker-compose.
:warning: Warning: if you don’t use docker maybe you get the flag, but you miss the training objective.

```jsx
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"            
    networks:
      - app-network        

  backend:
    build: ./backend       
    hostname: backend
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

```jsx
docker-compose up --build
```

```jsx
curl http://localhost:80/flagNS_0.09 - Docker networks
```