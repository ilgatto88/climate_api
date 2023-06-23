# climATe API: Climate Data API for Austria

[![Code quality and tests](https://github.com/ilgatto88/climate_api/actions/workflows/main.yml/badge.svg)](https://github.com/ilgatto88/climate_api/actions/workflows/main.yml) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Project Description

---

The climATe API is a RESTful API that provides climate data for Austria. The original data is provided by the Austrian Central Institute for Meteorology and Geodynamics (ZAMG) through their data portal called [Datahub](https://data.hub.zamg.ac.at/). This data was processed into it's final form by the creator of the API. The API is written in Python using the [FastAPI](https://fastapi.tiangolo.com/) framework and the whole application is containerized using [Docker](https://www.docker.com/).

## Table of Contents

---

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage and API Documentation](#usage-and-api-documentation)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [License](#license)

## Requirements

---

For building the application you need:

- a host machine with Docker and Docker Compose installed
- network connection to the internet

## Installation

---

To build and start the application, make sure to create a `.env` file in the root directory of the project and add the following environment variables:

- MONGO_INITDB_ROOT_USERNAME, example: `MONGO_INITDB_ROOT_USERNAME=root`
- MONGO_INITDB_ROOT_PASSWORD, example: `MONGO_INITDB_ROOT_PASSWORD=example`
- MONGODB_PORT, example: `MONGODB_PORT=27017`
- MONGODB_ROOT_USER, example: `MONGODB_ROOT_USER=root`
- MONGODB_ROOT_PASSWORD, example: `MONGODB_ROOT_PASSWORD=example`
- MONGODB_ROOT_HASHED_PASSWORD, (see instructions below) example: `MONGODB_ROOT_HASHED_PASSWORD=$2y$12$0J`
- JWT_SECRET, example: `JWT_SECRET=example`
- JWT_ALGORITHM, example: `JWT_ALGORITHM=HS256`

Further instructions for the MONGODB_ROOT_HASHED_PASSWORD environment variable.  
To generate a hashed password for the MongoDB root user, you can use the following command:

`python3 -c 'import bcrypt; print(bcrypt.hashpw("<MONGODB_ROOT_PASSWORD>".encode(), bcrypt.gensalt()).decode())`

where `<MONGODB_ROOT_PASSWORD>` is the password you want to use for the MongoDB root user. The output of the command is the hashed password that you can use for the MONGODB_ROOT_HASHED_PASSWORD environment variable. If you don't have Python and bcrypt installed, you can also use an online bcrypt generator like [this one](https://bcrypt-generator.com/).

## Usage and API Documentation

---

If you have built the application locally, you can check if it is running by opening the following URL in your browser: `http://127.0.0.1:8000`. You will be automatically redirected to the Swagger UI documentation page of the API. If you want to use the Redoc documentation page, you can open the following URL in your browser: `http://127.0.0.01:8000/redoc`.  
As visible in the Swagger UI documentation page, the API has currently two endpoints:

- `/api/v1/Municipalities/`
- `/api/v1/MunicipalityData/`

POST, PUT or DELETE methods are only allowed for the root user. The root user is the user that is created when the MongoDB container is started for the first time. The root user credentials are the ones that you have specified in the `.env` file. To authenticate using the Swagger UI, select the POST method at the Users section and click on the "Try it out" button. Then enter the following JSON in the Request Body field:

```json
{
  "username": "<MONGODB_ROOT_USER>",
  "password": "<MONGODB_ROOT_PASSWORD>"
}
```

where `<MONGODB_ROOT_USER>` and `<MONGODB_ROOT_PASSWORD>` are the credentials that you have specified in the `.env` file. After that, click on the "Execute" button. If the authentication was successful, you will receive a JSON Web Token (JWT) in the Response Body field. Copy the JWT and click on the "Authorize" button at the top of the page. In the popup window, enter the token in the Value field. After that, you can use the API as a root user.

## Examples

---

Examples are provided by the Swagger UI documentation page.

## License

---

[MIT](LICENSE)

---

[Go to Top](#table-of-contents)
