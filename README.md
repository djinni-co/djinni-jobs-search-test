# Djinni test

## Installation

### Prerequisites

- Docker: Engine: v27 Compose: v2.28

### Local setup

#### 1. Clone this repo

```
git clone git@github.com:djinni-co/djinni-jobs-test.git
cd djinni-jobs-test
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

If installation succeed you will see the following in the console:
```
web-1  | Django version 4.2.4, using settings 'djinnitest.settings'
web-1  | Starting development server at http://0.0.0.0:8000/
web-1  | Quit the server with CONTROL-C.
```

#### 4. Run migrations

```
docker compose exec web python3 app/manage.py migrate
```

#### 5. Import database  

See active containers list:  

```
docker ps
```
```
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS         PORTS                    NAMES
ba15bc763d0b   djinnitest-web    "python app/manage.p…"   16 minutes ago   Up 5 minutes   0.0.0.0:8000->8000/tcp   djinnitest-web-1
8c7c57d12f01   postgres:latest   "docker-entrypoint.s…"   2 hours ago      Up 5 minutes   
```

In this example the **8c7c57d12f01** is the `<CONTAINER ID>` of the **postgres** container.  
  
Replace `<CONTAINER ID>` with the id of the postgres container and run the command:

```
cat dump.sql | docker exec -i <CONTAINER ID> psql --user admin djinni_sandbox
```

Now open the http://0.0.0.0:8000 and you will see jobs list.

Good to go! 👍👍
