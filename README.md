[![Build Status](https://github.com/tuncutku/Portfolio-Engineer/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/tuncutku/Portfolio-Engineer/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Table of Contents

* [About the Project](#about-the-project)
* [First time developer setup](#first-time-developer-setup)
* [Project Structure](#project-structure)
* [Work with ./doit.sh](#work-with-./doit.sh)
* [Work with CLI](#work-with-cli)
* [Work with Celery](#work-with-celery)
* [Docker commands](#docker-commands)
* [License](#license)


## About The Project


Portfolio engineer is an application for monitoring portfolio performance, conducting portfolio analytics as well as setting custom alerts.

Instrument coverage:
* Equities
* ETFs
* Options

Portfolio analytics coverage:
* Portfolio performance measures
* Scenario analysis
* Monte carlo simulation
* Risk metrics (VaR)
* Backtesting
* Portfolio optimization
* Factor analysis

Alert coverage:
* Price
* Return

## First time developer setup

1. To pull portfolio engineer repository:
   `git clone https://github.com/tuncutku/Portfolio-Engineer.git`
2. Create virtual environment and activate it:
   `./doit.sh`
3. Run unit tests:
   `./doit.sh run_tests`
4. Create a new branch:
   `git checkout <name of the user>-<git issue number>-<short description of the issue>`
4. Pull request naming:
   `<issue number>-<short description of the issue>`


## Project Structure

```bash
portfolio engineer/
├── src/
│   ├── analytics/                # Analytics library
│   ├── api/
│   ├── dashapp/
│   ├── environment/
│   ├── forms/
│   ├── market/                   # Instruments and other market components
│   ├── tasks/
│   ├── templates/
│   ├── views/
│   ├── cli.py
│   └── extensions.py/
├── tests/
│   └── conftest.py
│       ...
├── docker-compose.yml
├── Dockerfile
├── doit.sh
├── README.md
├── config.py
├── requirements.txt
├── run_app.py
└── run_celery.py
```


## Work with `./doit.sh`

Provide the `doit.sh` command with one of the following commands as an argument:

```bash
./doit.sh
```

| Argument                      | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| run_tests                     | Run unit tests.                                                            |
| init_db                       | Run linters against code and also check style.                             |


If you do not provide a command argument, the `doit.sh` command returns a list of them.

## Work with CLI

* `flask init_db`
* `flask seed_data`
* `flask clear_db`


## Work with Celery

* Run celery worker: `celery -A run_celery.celery worker --loglevel=info`
* Run celery beat: `celery -A run_celery.celery beat --loglevel=info`
* Run celery worker and beat at the same time: `celery -A run_celery.celery worker --loglevel=info -B `

## Docker commands

* Build image: `docker build . -t tuncutku/portfolio_engineer:latest`
* Run image in a container: `docker run -d -p 5001:5001 --env-file .env --name portfolio_engineer portfolio_engineer`
* Push image `docker push tuncutku/portfolio_engineer:latest`
* Run docker compose: `docker-compose --env-file .env -f "docker-compose.yml" up -d --build`

## License

Distributed under the MIT License. See `LICENSE` for more information.
