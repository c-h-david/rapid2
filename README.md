# RAPID

<!-- pyml disable-num-lines 2 no-inline-html -->
<!-- pyml disable-num-lines 1 line-length -->
<img src="https://raw.githubusercontent.com/c-h-david/rapid2/main/img/icon_rapid_network.svg" alt="RAPID network icon" width="128"/>

[![DOI][BDG_ZENODO]][URL_ZENODO]

[![Python versions][BDG_PY_VSN]][URL___PYPI]
[![PyPI version][BDG_PYPI_V]][URL___PYPI]
[![PyPI downloads][BDG_PYPI_D]][URL___PYPI]

[![Run Docker][BDG_DKRRUN]][URL_DKRIMG]
[![Docker pulls][BDG_DKRPUL]][URL_DKRIMG]

[![CI (integration)][BDG_GHA_CI]][URL_GHA_CI]
[![Last commit][BDG_GH_LST]][URL_GHREPO]

[![lint: ruff][BDG___RUFF]][URL___RUFF]
[![type: mypy][BDG___MYPY]][URL___MYPY]
[![test: doctest][BDG_DOCTST]][URL_DOCT]

[![License (3-Clause BSD)][BDG_BSD3CL]][URL_BSD3CL]
[![Contributor Covenant][BDG_CONDUC]][URL_CONDUC]
[![Code of Collab][BDG_COLLAB]][URL_COLLAB]
[![SLIM][BDG___SLIM]][URL___SLIM]

The Routing Application for Programmed Integration of Discharge (RAPID) is a
river network routing model. Given external inflow to rivers, this model can
compute the flow of water everywhere in river networks made out of many
thousands of reaches.

> **Note:** While the underlying RAPID routing methodology is highly mature and
> battle-tested in operational environments, this specific Python 3 codebase
> (RAPID2) is currently in Beta (v2.0.0b1) and under active development.

Notable links:

- [RAPID website][URL_RAPHUB]
- [Discussion Board][URL_DISCUS]
- [Issue Tracker][URL_ISSUES]

## Features

Notable features of the RAPID model:

- Open Source
- Described in peer-reviewed papers
- Has been used in 100+ studies published in international peer-reviewed
  journals
- Operationally implemented at world-class research centers

## Contents

- [Quick Start](#quick-start)
- [Changelog](#changelog)
- [FAQ](#frequently-asked-questions-faq)
- [Contributing Guide](#contributing)
- [License](#license)
- [Support](#support)

## Quick Start

This guide provides a quick way to get started with our project. Please see the
[RAPID website][URL_RAPHUB] for a more comprehensive information.

### Requirements

- `git`
- `python3.11`
- `pip3`

### Setup Instructions

```bash
git clone https://github.com/c-h-david/rapid2
cd rapid2
pip install .
```

### Run Instructions

```bash
rapid2 --namelist namelist_Sandbox.yml
```

### Usage Examples

Below is an example of what `namelist_Sandbox.yml` should include:

```yaml
---
Qex_ncf: './input/Sandbox/Qext_Sandbox_19700101_19700110.nc4'
Q00_ncf: './input/Sandbox/Qinit_Sandbox_19700101_19700110.nc4'

con_csv: './input/Sandbox/rapid_connect_Sandbox.csv'
kpr_csv: './input/Sandbox/k_Sandbox.csv'
xpr_csv: './input/Sandbox/x_Sandbox.csv'

bas_csv: './input/Sandbox/riv_bas_id_Sandbox.csv'

IS_dtR: 900

Qou_ncf: './output/Sandbox/Qout_Sandbox_19700101_19700110_tst.nc4'
Qfi_ncf: './output/Sandbox/Qfinal_Sandbox_19700101_19700110_tst.nc4'
```

### Build Instructions

If you would like to build an Operating System to run RAPID2 from scratch,
we recommend Debian-based distributions and software packages for the
Advanced Packaging Tool (APT) are summarized in
[`requirements.apt`][URL_REQAPT]
to be installed with `apt-get`. All packages can be installed at once
using:

```bash
sudo apt-get install -y --no-install-recommends \
     $(grep -v -E '(^#|^$)' requirements.apt)
```

> Alternatively, one may install the APT packages listed in
> [`requirements.apt`][URL_REQAPT]
> one by one, for example:
>
> ```bash
> sudo apt-get install -y --no-install-recommends python3.11
> ```

Also make sure that `python3` points to `python3.11`:

```bash
sudo rm -f /usr/bin/python3
sudo ln -s /usr/bin/python3.11 /usr/bin/python3
```

If you would like to run in a virtual environment:

```bash
python3 -m venv $HOME/venv
export PATH=$HOME/venv/bin:$PATH
```

### Test Instructions

See our [`TESTING.md`][URL_TSTING] for a description of our tests.

## Changelog

See our [`CHANGELOG.md`][URL_CHGLOG] for a history of our changes.

See our [releases page][URL_RELEAS] for our key versioned releases.

## Frequently Asked Questions (FAQ)

Questions about our project? Please see our [Discussion Board][URL_DISCUS].

## Contributing

Interested in contributing to our project? Please see:

- [`CONTRIBUTING.md`][URL_CONTRI]
- [`CODE_OF_CONDUCT.md`][URL_CONDUC]
- [`CODE_OF_COLLAB.md`][URL_COLLAB]
- [`GOVERNANCE.md`][URL_GOVERN]

## License

We use a Berkeley Software Distribution 3-Clause license:
[`LICENSE`][URL_LICENS]

## Support

The prefered way to interact with RAPID2 and its community is to do so through
our public online resources:

- [RAPID website][URL_RAPHUB]
- [Discussion Board][URL_DISCUS]
- [Issue Tracker][URL_ISSUES]

For sensitive matters that cannot be shared publicly, contact
[Cédric H. David][URL_GITCHD]

<!-- pyml disable-num-lines 30 line-length -->
[BDG_ZENODO]: https://zenodo.org/badge/DOI/10.5281/zenodo.19393023.svg

[BDG_PY_VSN]: https://img.shields.io/pypi/pyversions/rapid2
[BDG_PYPI_V]: https://img.shields.io/pypi/v/rapid2
[BDG_PYPI_D]: https://img.shields.io/pypi/dm/rapid2?style=flat

[BDG_DKRRUN]: https://img.shields.io/badge/run-docker-blue?logo=docker
[BDG_DKRPUL]: https://img.shields.io/docker/pulls/chdavid/rapid2

[BDG_GHA_CI]: https://github.com/c-h-david/rapid2/actions/workflows/CI.yml/badge.svg
[BDG_GH_LST]: https://img.shields.io/github/last-commit/c-h-david/rapid2

[BDG___RUFF]: https://img.shields.io/badge/lint-ruff-blue
[BDG___MYPY]: https://img.shields.io/badge/type-mypy-blue
[BDG_DOCTST]: https://img.shields.io/badge/test-doctest-blue

[BDG_BSD3CL]: https://img.shields.io/badge/license-BSD%203--Clause-yellow.svg
[BDG_CONDUC]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
[BDG_COLLAB]: https://img.shields.io/badge/Code%20of%20Collab-DRAFT-violet.svg
[BDG___SLIM]: https://img.shields.io/badge/Best%20Practices%20from-SLIM-blue

[URL_ZENODO]: https://doi.org/10.5281/zenodo.19393023

[URL___PYPI]: https://pypi.org/project/rapid2/

[URL_DKRIMG]: https://hub.docker.com/r/chdavid/rapid2

[URL_GHA_CI]: https://github.com/c-h-david/rapid2/actions/workflows/CI.yml
[URL_GHREPO]: https://github.com/c-h-david/rapid2

[URL___RUFF]: https://docs.astral.sh/ruff/
[URL___MYPY]: https://mypy-lang.org/
[URL_DOCT]: https://docs.python.org/3/library/doctest.html

[URL_BSD3CL]: https://github.com/c-h-david/rapid2/blob/main/LICENSE
[URL_CONDUC]: https://github.com/c-h-david/rapid2/blob/main/CODE_OF_CONDUCT.md
[URL_COLLAB]: https://github.com/c-h-david/rapid2/blob/main/CODE_OF_COLLAB.md
[URL___SLIM]: https://nasa-ammos.github.io/slim/

[URL_RAPHUB]: http://rapid-hub.org/
[URL_DISCUS]: https://github.com/c-h-david/rapid2/discussions
[URL_ISSUES]: https://github.com/c-h-david/rapid2/issues
[URL_REQAPT]: https://github.com/c-h-david/rapid2/blob/main/requirements.apt
[URL_TSTING]: https://github.com/c-h-david/rapid2/blob/main/TESTING.md
[URL_CHGLOG]: https://github.com/c-h-david/rapid2/blob/main/CHANGELOG.md
[URL_RELEAS]: https://github.com/c-h-david/rapid2/releases
[URL_CONTRI]: https://github.com/c-h-david/rapid2/blob/main/CONTRIBUTING.md
[URL_GOVERN]: https://github.com/c-h-david/rapid2/blob/main/GOVERNANCE.md
[URL_GITCHD]: https://github.com/c-h-david
