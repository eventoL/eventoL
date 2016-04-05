Proceso
=======

```bash
docker build -t eventol .
docker run --name eventol-postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_USER=eventol -e POSTGRES_DB=eventol -p 5432:5432 -d postgres
docker run -d -i --name="eventol" --hostname="eventol" -p 8000:8000 --link=eventol-postgres -e PSQL_HOST=eventol-postgres -t eventol:latest
```

Listo
-----
