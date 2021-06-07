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





<!-- ABOUT THE PROJECT -->
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

* src/services contains implementation of the cloud services used to run the build system and demo the products
* src/packages contains python packages that are deliverable to a clients
* src/infra contains python packages that are shared across different projects, but are only for internal use

Directory structure, key locations:

```bash
falcon/
├── src/
│   ├── services/                # SDK customer trials infrastructure
│   └── packages/
│       ├── fincad_f3/           # `fincad.f3` python-package
│       ...
│   └── infra/
│       ├── fincad_devdocs/       # `fincad.devdocs` python-package
│       ...
├── conftest.py
├── scripts
├── dodo.py
├── doit.sh
├── README.md
├── dev_packages.txt
├── requirements_dev.in
└── requirements_dev.txt
```


## Work with `./doit.sh`

Provide the `doit.sh` command with one of the following commands as an argument:

```bash
./doit.sh
```

| Argument                      | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| unit_tests                    | Run unit tests.                                                            |
| check_code                    | Run linters against code and also check style.                             |
| compile_dependencies          | Generate requirements files.                                               |
| analytics_instrument_coverage | Generate analytics instrument coverage report.                             |
| analytics_profile_tests       | Profile analytics unit-tests.                                              |
| analytics_profiler_report     | Generate profiler report based on results under analytics.                 |
| fincad_f3_build_whl           | Make wheel-file from fincad.f3 package.                                    |
| fincad_f3_download_core       | Download F3 core library.                                                  |
| fincad_f3_generate_python_api | Generate python API for F3 core library.                                   |
| fincad_sdk_build_zip          | Make the installer of FINCAD SDK.                                          |
| fix_style                     | Fix code style.                                                            |
| generate_docs                 | Generate Sphinx Documentation.                                             |
| install_dev                   | Install development and production requirements and configure the VS Code. |
| run_codeclimate_cli           | Run CodeClimate CLI for modified files. (Note: Works with WSL 2)           |
| test_docs                     | Test docs against the style guide.                                         |

If you do not provide a command argument, the `doit.sh` command returns a list of them.

## Deployment







<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.
