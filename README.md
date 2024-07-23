# Djinni test

## Installation

### Prerequisites

- Docker: Engine: v27 Compose: v2.28

### Local setup

1. Clone this repo

2. Create the `.env` file:

  ```
  cp .env.example .env
  ```

3. Build and run the docker container:

```
docker compose build
docker compose up
```

Check if the installation succeeds by opening the http://localhost:8000/

4. Run migrations

```
docker compose exec web python3 app/manage.py migrate
```

5. Import database

Run `docker ps` and get the CONTAINER ID of the **postgres:image**.  

```
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS         PORTS                    NAMES
ba15bc763d0b   djinnitest-web    "python app/manage.p…"   16 minutes ago   Up 5 minutes   0.0.0.0:8000->8000/tcp   djinnitest-web-1
8c7c57d12f01   postgres:latest   "docker-entrypoint.s…"   2 hours ago      Up 5 minutes   
```

You should see something like this, the **8c7c57d12f01** here is the container id of the pg container.

Then run the following command to write backup.sql onto djinni_sandbox db. Replace <CONTAINER ID> with the id of the postgres container.

```
cat backup.sql | docker exec -i <CONTAINER ID> psql --user admin djinni_sandbox
```

👍👍 Good to go!
