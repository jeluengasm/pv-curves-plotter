# Photovoltaic Plotter

## Description

This project is an extension to the development of the photovoltaic curve tracer, presented in the diploma course on photovoltaic installations, given by [LIATER](https://ingenieria.unal.edu.co/liater/) at [Universidad Nacional de Colombia](https://bogota.unal.edu.co/).

The objective of this project is the implementation of a web application that plots and manages I-V and P-V curves, obtained with the prototype curve tracer. This application requires a registration and authentication of the user who wants to use it. This application uses docker containers, in order to facilitate its development and deployment.

### Developers

- Johanna Milena Yama Mora ([@JohannaYama](https://github.com/JohannaYama))
- Juan Martin Vivas Camargo ([@JuanMartin1946](https://github.com/JuanMartin1946))
- Jhon Esteban Luengas Machado ([@jeluengasm](https://github.com/jeluengasm))


###Tools

- Front End:
    - HTML
    - CSS
    - Javascript with jQuery 3.4.1
    - Bootstrap 5.0

- Back End:
    - Python 3.9
    - Libraries/Frameworks: 
        - Django 4.0.7
        - Django REST Framework 3.13.1
        - Plotly 5.10
        - Pandas 1.5
        - Pytest 4.5.2
        - Dot env 0.21.0
        - psycopg2 2.9.3
        - Django ORM

- Database:
    - PostgreSQL 14.5 (stored in container)

- Development environment (required to be installed on your computer):
    - Docker 20.10.18
    - Docker Compose 2

## Installation

### For development

#### Environment setup

- To start the application in a development environment, it's necessary to create a file with the name `.env` in the `pv_plotter` folder of this project.
<br>
- In this file you'll add the environment variables that the application needs to start. It's necessary to add the following lines:

    ```yml
    DATABASE_URL=postgresql+psycopg2://postgres:123@db:5432/pv_db
    DB_NAME=pv_db
    DB_USER=postgres
    DB_PASSWORD=123
    DB_HOST=db
    DB_PORT=5432
    ```
The same credentials aren't necessary, they can be changed. However, if you want to restart the database, you must delete the `pv_plotter/data` folder.

- Open a terminal and go to the `pv_plotter/` folder.
<br>

- Execute the command:

    ```docker
    docker compose build
    ```

This command will create two containers of the `app` and `postgres` images (see `docker-compose.yml`). On the `app` image the environment variables are added to configure the database. In the case of the database, the variables to connect (or create) are configured, too. The `web` and `postgres_db` containers will be created.
    <br>

- Execute the command:

    ```docker 
    docker compose up
    ```
This command will start the containers and open a connection to the Django server (default is [http://localhost:8000](http://localhost:8000)). If the server doesn't respond, stop the containers and re-run them with the above command. If you want to change the port, edit line `14` in `docker-compose.yml`.

### Testing

The current proyect uses Pytest to run the tests, in order to verify that the API designed in the code works correctly. To perform the tests, execute the command:

   ```bash
    docker compose exec app pytest
   ```

### Open browser

The application will run in the following url: `http://localhost:8000`