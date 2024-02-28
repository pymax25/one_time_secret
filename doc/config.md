# Configuration

The configuration for the `One time secret` service is managed through environment variables. Here are the available configuration options:

- `APP_HOST`: The host of the flask app. Default is local development server string empty string "0.0.0.0".
- `POSTGRES_USER`: The name of the PGSQL user. Required to be filled out to set up a custom database and its further usage. Default is an empty string.
- `POSTGRES_PASSWORD`: Password for PGSQL connection to a database. Required to be filled out to set up a custom database and its further usage. Default is an empty string.
- `POSTGRES_DB`: The name of the PGSQL database. Required to be filled out to set up a custom database and its further usage. Default is an empty string.
- `REQUESTS_PER_MINUTE_LIMIT`: A limit of incoming request from 1 user. Default is 600.
- `DB_LOGS`: This variable stands for enabling\disabling sql-alchemy engine live logs. If logs are required - it needs to be filled with any string. Default is False.