<hr>

<div align="center">

<img src="/static/img/logo.svg" alt="RAPID2 Logo" width="200px">

<h1 align="center">RAPID2</h1>

</div>

<pre align="center">Hydrologic routing application integrating discharge calculations in Python.</pre>

[![License (3-Clause BSD)](https://img.shields.io/badge/license-BSD%203--Clause-yellow.svg)](https://github.com/c-h-david/rapid2/blob/main/LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/c-h-david/rapid2/blob/main/CODE_OF_CONDUCT.md)
[![SLIM](https://img.shields.io/badge/Best%20Practices%20from-SLIM-blue)](https://nasa-ammos.github.io/slim/)


## Features

- Basin file processing
- Connectivity mapping
- Hydrologic routing with the Muskingum method
- NetCDF-based inflow and outflow file handling

## Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Quick Start

### Installation with Docker

The easiest way to install RAPID2 is via Docker. Follow these steps:

```bash
docker pull chdavid/rapid2
docker run --rm -it chdavid/rapid2
```

### Installation on Debian

For Debian users, follow these steps:

```bash
sudo apt-get install -y --no-install-recommends git

git clone https://github.com/c-h-david/rapid2
cd rapid2/

sudo apt-get install -y --no-install-recommends $(grep -v -E '(^#|^$)' requirements.apt)
```

Set up Python:

```bash
python3 -m venv $HOME/venv
export PATH=$HOME/venv/bin:$PATH
pip3 install --no-cache-dir -r requirements.pip
```

## Usage Examples

- Running basic hydrologic routing:

```bash
python3 run_rapid.py --input example_input.nc --output results.nc
```

## Changelog
See our [CHANGELOG.md](CHANGELOG.md) for the history of changes.

## Contributing
Interested in contributing? See our [CONTRIBUTING.md](CONTRIBUTING.md).

## License
This project is licensed under the [BSD 3-Clause License](LICENSE).

## Support
For questions and support, please contact [@c-h-david](https://github.com/c-h-david).
