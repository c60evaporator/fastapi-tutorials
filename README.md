# fastapi-tutorials

This repository is for 

## Installation

- Clone this repository by `git clone https://github.com/c60evaporator/fastapi-tutorials.git` command
- Create config files (See the section below)

### Create config files

#### 2_fastapi_postgres_react_jwt

##### .env

```.env
POSTGRES_USER=User name of the DB (Please enter any user name you like)
POSTGRES_PASSWORD=Password of the DB (Please enter any password you like)
PGADMIN_EMAIL=E-mail address for PGAdmin (Please enter any E-mail address you like)
PGADMIN_PASSWORD=Password of PGAdmin (Please enter any password you like)
DB_HOST=PostgreSQL container name (Please enter any name you like, e.g., postgres-db)
DB_NAME=PostgreSQL database name (Please enter any name you like, e.g., fastapi_jwt_tutorial)
BACKEND_HOST=Backend container name (Please enter any name you like, e.g., app-server)
BACKEND_PORT=8000
SECRET_KEY=Secret key of JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=Expiration date of JWT token (Please enter any days you like, e.g., 30)
```

## Run the apps

#### 2_fastapi_postgres_react_jwt

Run the app by the following command.

```bash
docker compose -f 2_fastapi_postgres_react_jwt/docker-compose.yml up
```
