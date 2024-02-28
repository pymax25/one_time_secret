# one_time_secret
A small service that implements creation and acquiring secret data with its further deletion.

## Documentation

- [Configuration](doc/config.md)
- [Swagger](doc/swagger.yaml)

## Setting up project locally

- "git clone" this repository into your desired directory using the web URL
- fill out docker-compose.yml file with all the required environment variables that are listed in config.md file for both one-time-secret and postgresql containers
- type command "docker-compose build one-time-secret"
- type command "docker-compose up -d one-time-secret" 
- to apply all the required db migrations type "docker exec -it one-time-secret bash" and then type "alembic upgrade head"
- you are ready to go! your One time secret app is running and ready for requests (all available routes you can find in doc/swagger.yaml)

## Running tests

- to run tests type "docker-compose -f docker-compose.test.yml build" and then "docker-compose -f docker-compose.test.yml up"