# SQL Intern Challenge Environment

This repository contains the environment and datasets used for the SQL intern challenges.

The goal of this project is to provide a fully reproducible SQL learning environment where interns can practice querying realistic datasets without needing to install or configure a database manually.

The database is delivered through a Dockerized PostgreSQL instance, so everyone runs the exact same environment locally.

All datasets are automatically loaded when the container starts.

## What You Will Learn

Through the exercises you will practice:

- SQL joins
- filtering and aggregations
- window functions
- query optimization
- indexing
- working with event data
- querying JSON data
- debugging queries

## Requirements

Before starting, install the following tools.

### Docker Desktop

Docker is used to run the database locally.

Download:  
https://www.docker.com/products/docker-desktop/

### Git

Git is used to clone the repository.

Download:  
https://git-scm.com/downloads

### DBeaver

DBeaver is the SQL client used to query the database.

Download:  
https://dbeaver.io/download/

## Repository Structure

```text
sql-intern-challenges/
├── README.md
├── docker-compose.yml
├── tasks/
│   ├── case1_questions.md
│   └── case2_questions.md
└── ...
```

## First Time Setup

Follow these steps when running the environment for the first time.

### 1. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/YOUR_ORG/sql-intern-challenges.git
```

Enter the repository folder:

```bash
cd sql-intern-challenges
```

### 2. Start the database

Run:

```bash
docker compose up -d
```

Docker will automatically:

1. download the prepared database image
2. start PostgreSQL
3. load all datasets

The first run may take 10–20 seconds.

### 3. Verify the container is running

Run:

```bash
docker ps
```

You should see something similar to:

```text
PORTS
0.0.0.0:55432->5432/tcp
```

This means the PostgreSQL server is available on port `55432`.

## Connect Using DBeaver

Open DBeaver and create a new PostgreSQL connection.

Use the following settings:

| Field | Value |
|------|------|
| Host | localhost |
| Port | 55432 |
| Database | intern_challenges |
| Username | intern |
| Password | intern |

Click **Test Connection**, then **Finish**.

## Verify the Environment

Once connected, open a SQL editor and run:

```sql
SELECT COUNT(*) FROM case1.users;
SELECT COUNT(*) FROM case1.orders;
SELECT COUNT(*) FROM case2.events;
```

If rows are returned, the environment is working correctly.

## Database Structure

The database contains two schemas.

### Schema: `case1`

This schema is used for basic to intermediate SQL exercises.

Tables include:

- `users`
- `products`
- `subscriptions`
- `orders`
- `order_items`
- `returns`
- `campaign_attribution`

This dataset represents a simplified e-commerce subscription platform.

You will practice joins, aggregations, and business metrics.

### Schema: `case2`

This schema is used for advanced SQL and performance exercises.

Tables include:

- `accounts`
- `app_users`
- `events`
- `tickets`
- `ticket_events`

This dataset simulates product analytics and support ticket systems.

You will practice:

- event analysis
- JSON queries
- window functions
- query optimization
- indexing strategies

## Challenge Instructions

The exercises are located in:

```text
tasks/case1_questions.md
tasks/case2_questions.md
```

Complete **Case 1** first, then move to **Case 2**.

## Daily Usage

You do not need to recreate the database every day.

Once the container has been created, the data persists in the Docker volume.

### If the container is already running

Simply open DBeaver and start querying.

### If the container is stopped

Start it with:

```bash
docker compose start
```

or

```bash
docker compose up -d
```

Both commands will start the database.

## Stopping the Database

When you finish working, you can stop the container:

```bash
docker compose stop
```

This frees system resources but keeps the data intact.

## Resetting the Database

If something breaks or you want to reset the environment:

```bash
docker compose down -v
docker compose up -d
```

This will:

1. delete the database volume
2. recreate the container
3. reload the datasets

## Useful Docker Commands

### View running containers

```bash
docker ps
```

### View database logs

```bash
docker compose logs db
```

### Restart the database

```bash
docker compose restart
```

### Stop the database

```bash
docker compose stop
```

### Reset the entire environment

```bash
docker compose down -v
docker compose up -d
```

## Common Issues

### Port already in use

If Docker cannot start the database because the port is already in use, another PostgreSQL instance may already be running locally.

Stop the local database or change the port mapping in `docker-compose.yml`.

### Container conflict

If Docker reports that a container already exists, run:

```bash
docker compose down
```

and start again:

```bash
docker compose up -d
```

### Docker not running

Make sure Docker Desktop is open and running before executing Docker commands.

## SQL Tips

Tables belong to different schemas, so queries should include the schema name.

Example:

```sql
SELECT *
FROM case1.orders
LIMIT 10;
```

## Learning Goals

This environment simulates a simplified data platform workflow.

You will gain experience with:

- real-world SQL datasets
- schema exploration
- query performance
- analytical thinking
- debugging data issues

## Questions

If you run into issues setting up the environment, please reach out to your mentor.
