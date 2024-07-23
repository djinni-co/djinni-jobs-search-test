# Djinni test

## Installation

### Prerequisites

- Docker: Engine: v27 Compose: v2.28

### Local setup

#### 1. Clone this repo

```
git clone git@github.com:djinni-co/djinni-jobs-test.git
```

#### 2. Create the `.env` file:

```
cp .env.example .env
```

#### 3. Build and run the docker container:

```
docker compose build
docker compose up
```

You may now check if the installation succeeds by opening the http://0.0.0.0:8000/

#### 4. Run migrations

```
docker compose exec web python3 app/manage.py migrate
```

#### 5. Import database  
  
#### 5.1. Get the `<CONTAINER ID>` of the **postgres:image**.  

Run `docker ps` to see active containers list:  

```
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS         PORTS                    NAMES
ba15bc763d0b   djinnitest-web    "python app/manage.p…"   16 minutes ago   Up 5 minutes   0.0.0.0:8000->8000/tcp   djinnitest-web-1
8c7c57d12f01   postgres:latest   "docker-entrypoint.s…"   2 hours ago      Up 5 minutes   
```

In this example the **8c7c57d12f01** is the `<CONTAINER ID>` of the **postgres** container.  
  
#### 5.2 Import dump.sql into postgres database  
  
Replace `<CONTAINER ID>` with the id of the postgres container and run the command:

```
cat dump.sql | docker exec -i <CONTAINER ID> psql --user admin djinni_sandbox
```


Good to go! 👍👍
