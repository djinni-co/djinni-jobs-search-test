## Additional Instructions to `README.md`

Install the following extension to your database after the basic setup and BEFORE applying the migrations:

```bash
docker compose exec db psql -U admin -d djinni_sandbox -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
```