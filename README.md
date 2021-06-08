[![Build Status](https://github.com/tuncutku/Portfolio-Engineer/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/tuncutku/Portfolio-Engineer/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
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


## Project Structure

```bash
falcon/
├── src/
│   ├── analytics/                # Analytics library
│   ├── api/
│   ├── dashapp/
│   ├── environment/
│   ├── forms/
│   ├── market/
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
├── run_app.py
├── run_celery.py
└── requirements.txt
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

## Deployment

### Docker
### Heroku





<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.
