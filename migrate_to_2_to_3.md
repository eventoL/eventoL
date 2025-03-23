# Migrate EventoL 2.x to 3.x

## Migrating PostgreSQL from Version 9 to 14

This guide explains how to migrate your PostgreSQL database from version 9 to version 14 using Docker Compose in a Linux environment of EventoL 2.x to 3.x.

### Prerequisites

- Ensure you have Docker and Docker Compose installed.
- Backup your current data directory before proceeding.
- Use the provided `deploy/docker/docker-compose.prod.yml` file.

---

### Steps

#### 1. Create a Backup of the PostgreSQL 9 Database

First, create a backup of your PostgreSQL 9 database to ensure you can restore it if needed.

```bash
cd deploy/docker
docker compose -f docker-compose.prod.yml exec postgres bash
pg_dump -U <username> -F c -b -v -f /eventol2.backup <database_name>
```

Replace `<username>` with your PostgreSQL username and `<database_name>` with your database name.

#### 2. Copy the Backup File to the Host Machine

Copy the backup file from the PostgreSQL container to your host machine.

```bash
docker cp docker_postgres_1:/eventol2.backup /tmp/
```

#### 3. Stop and Remove the Current Containers

Stop and remove the running containers to prepare for the upgrade.

```bash
docker compose -f docker-compose.prod.yml stop
docker compose -f docker-compose.prod.yml down
```

#### 4. Backup the Existing Data Directory

Move the current PostgreSQL data directory to a safe location. This ensures you can revert if the migration fails.

```bash
mv /srv/deploys/eventoldata/postgres /srv/deploys/eventoldata/postgres9_backup
```

#### 5. Update and Rebuild the Docker Compose Environment

Pull the latest images and rebuild the services to use PostgreSQL 14.

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```

#### 6. Rollback the Migrations to the Last Version of EventoL 2.x

Access the web container and rollback the migrations to the last version of EventoL 2.x.

```bash
docker compose -f docker-compose.prod.yml exec web bash
cd eventol/
./manage.py migrate manager 0047_remove_place_from_required_fields
```

#### 7. Restore the Backup to PostgreSQL 14

Access the PostgreSQL 14 container and restore the backup.

```bash
docker compose -f docker-compose.prod.yml exec postgres bash
psql -h postgres -d <database_name> -U <username> -f /eventol2.backup
```

Replace `<username>` and `<database_name>` with the appropriate values.

#### 8. Apply Django Migrations

Run the necessary Django migrations to ensure compatibility with the new database.

```bash
docker compose -f docker-compose.prod.yml exec worker bash
cd eventol/
./manage.py migrate
```

#### 9. Restart All Services

Restart all services to apply the changes.

```bash
docker compose -f docker-compose.prod.yml restart
```

### Notes

- Ensure the `.env` file is correctly configured for the new PostgreSQL version.
- Test the application thoroughly after the migration to confirm everything works as expected.
