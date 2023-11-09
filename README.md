# climATe API: Climate Data API for Austria

[![CI](https://github.com/ilgatto88/climate_api/actions/workflows/test.yml/badge.svg)](https://github.com/ilgatto88/climate_api/actions/workflows/test.yml) [![codecov](https://codecov.io/github/ilgatto88/climate_api/branch/master/graph/badge.svg?token=CG91QI9FRV)](https://codecov.io/github/ilgatto88/climate_api) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)  
[![License: CC BY-NC SA 4.0](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-orange)](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode)

## CS50 Video Demonstration: [Link](https://www.youtube.com/watch?v=TJLsOpyqeDY)

## Project Description

The climATe API is a RESTful API that provides climate data for Austria. The original data is provided by the Zentralanstalt für Meteorologie und Geodynamik (ZAMG) through their data portal called [Datahub](https://data.hub.zamg.ac.at/). This data was processed into it's final form by the creator of the API. The API is written in Python using the [FastAPI](https://fastapi.tiangolo.com/) framework and the whole application is containerized using [Docker](https://www.docker.com/).

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage and API Documentation](#usage-and-api-documentation)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [License](#license)

## Requirements

For building the application you need:

- a host machine with Docker and Docker Compose installed
- network connection to the internet

## Installation

To build and start the application, make sure to create a `.env` file in the root directory based on the `.env.example` file. The `.env` file contains the environment variables that are used by the application. Regarding the MONGODB_HASHED_ROOT_PASSWORD environment variable in the `.env` file, you can use the following command to generate a hashed password for the MongoDB root user:  
`python3 -c 'import bcrypt; print(bcrypt.hashpw("<MONGODB_ROOT_PASSWORD>".encode(), bcrypt.gensalt()).decode())`

where `<MONGODB_ROOT_PASSWORD>` is the password you want to use for the MongoDB root user. The output of the command is the hashed password that you can use for the MONGODB_ROOT_HASHED_PASSWORD environment variable. If you don't have Python and bcrypt installed, you can also use an online bcrypt generator like [this one](https://bcrypt-generator.com/).

## Usage and API Documentation

If you have built the application locally, you can check if it is running by opening the following URL in your browser: `http://127.0.0.1:8000`. You will be automatically redirected to the Swagger UI documentation page of the API. If you want to use the Redoc documentation page, you can open the following URL in your browser: `http://127.0.0.01:8000/redoc`.  
As visible in the Swagger UI documentation page, the API has currently three endpoints:

- `/api/v1/municipalities/`
- `/api/v1/municipalitydata/historical/<parameter>/`
- `/api/v1/municipalitydata/scenario/<scenario}>/parameter>/`

POST, PUT or DELETE methods are only allowed for the admin user. The admin user is the user that is created when the MongoDB container is started for the first time. The admin user credentials are the ones that you have specified in the `.env` file. To authenticate using the Swagger UI, select the POST method at the Users section and click on the "Try it out" button. Then enter the following JSON in the Request Body field:

```json
{
  "username": "<MONGODB_ROOT_USER>",
  "password": "<MONGODB_ROOT_PASSWORD>"
}
```

where `<MONGODB_ROOT_USER>` and `<MONGODB_ROOT_PASSWORD>` are the credentials that you have specified in the `.env` file. After that, click on the "Execute" button. If the authentication was successful, you will receive a JSON Web Token (JWT) in the Response Body field. Copy the JWT and click on the "Authorize" button at the top of the page. In the popup window, enter the token in the Value field. After that, you can use the API as a root user.

## Examples

Examples are provided by the Swagger UI documentation page.

## About the output format

[Here](docs/climate_data.md) you can find a detailed description of the municipality data output format of the API.

## License

[CC BY-NC SA 4.0](LICENSE)

---

[Go to Top](#table-of-contents)
