# RAPID2

[![License (3-Clause BSD)][BDG_BSD3CL]][URL_LICENS]

[![Contributor Covenant][BDG_CONDUC]][URL_CONDUC]

[![SLIM][BDG___SLIM]][URL___SLIM]

[![GitHub CI Status][BDG_GHA_CI]][URL_GHA_CI]

[![GitHub CI Status][BDG_GHA_CD]][URL_GHA_CD]

The Routing Application for Python Integration of Discharge (RAPID) is a river
network routing model. Given surface and groundwater inflow to rivers, this
model can compute flow and volume of water everywhere in river networks made
out of many thousands of reaches.

[RAPID website][URL_RAPHUB]

[Discussion Board][URL_DISCUS]

[Issue Tracker][URL_ISSUES]

## Features

Notable features of the RAPID model:

- Open Source
- Described in peer-reviewed papers
- Has been used in 100+ studies published in international peer-reviewed
  journals
- Operationally implemented at world-class research centers

## Installation with Docker

Installing RAPID2 is **by far the easiest with Docker**. This document was
written and tested using
[Docker Community Edition][URL_DOCSFT]
which is available for free and can be installed on a wide variety of operating
systems. To install it, follow the instructions in the link provided above.

Note that the experienced users may find more up-to-date installation
instructions in
[Dockerfile][URL_DOCFIL].

### Download RAPID2 Docker image from Docker Hub

Downloading RAPID2 with Docker can be done using:

```bash
docker pull chdavid/rapid2
```

### Install packages

The beauty of Docker is that there is **no need to install anymore packages**.
RAPID2 is ready to go! To run it, just use:

```bash
docker run --rm -it chdavid/rapid2
```

## Installation on Debian

This document was written and tested on a machine with a **clean** image of
[Debian 12.7.0 ARM64][URL_DEBIAN]
installed, *i.e.* **no update** was performed, and **no upgrade** either.
Similar steps **may** be applicable for Ubuntu.

Note that the experienced users may find more up-to-date installation
instructions in
[CI.yml][URL_CI_YML].

### Download RAPID2 source code from GitHub

First, make sure that `git` is installed:

```bash
sudo apt-get install -y --no-install-recommends git
```

Then download RAPID2:

```bash
git clone https://github.com/c-h-david/rapid2
```

Finally, enter the RAPID2 directory:

```bash
cd rapid2/
```

### Install APT packages

Software packages for the Advanced Packaging Tool (APT) are summarized in
[requirements.apt][URL_REQAPT]
and can be installed with `apt-get`. All packages can be installed at once
using:

```bash
sudo apt-get install -y --no-install-recommends \
     $(grep -v -E '(^#|^$)' requirements.apt)
```

> Alternatively, one may install the APT packages listed in
> [requirements.apt][URL_REQAPT]
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

### Install Python packages

Python packages from the Python Package Index (PyPI) are summarized in
[requirements.pip][URL_REQPIP]
and can be installed with `pip`. But first, let's make sure to create a
virtual environment

```bash
python3 -m venv $HOME/venv
export PATH=$HOME/venv/bin:$PATH
```

> Consider including this last `export` statement in your run command file,
> like `~/.bash_aliases` on Debian.

All packages can be installed at once using:

```bash
pip3 install --no-cache-dir -r requirements.pip
```

> Alternatively, one may install the PyPI packages listed in
> [requirements.pip][URL_REQPIP]
> one by one, for example:
>
> ```bash
> pip3 install flake8==7.1.1
> ```

<!-- pyml disable-num-lines 30 line-length-->
[BDG_BSD3CL]: https://img.shields.io/badge/license-BSD%203--Clause-yellow.svg
[BDG_CONDUC]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
[BDG___SLIM]: https://img.shields.io/badge/Best%20Practices%20from-SLIM-blue
[BDG_GHA_CI]: https://github.com/c-h-david/rapid2/actions/workflows/CI.yml/badge.svg
[BDG_GHA_CD]: https://github.com/c-h-david/rapid2/actions/workflows/CD.yml/badge.svg

[URL_LICENS]: https://github.com/c-h-david/rapid2/blob/main/LICENSE
[URL_CONDUC]: https://github.com/c-h-david/rapid2/blob/main/CODE_OF_CONDUCT.md
[URL___SLIM]: https://nasa-ammos.github.io/slim/
[URL_GHA_CI]: https://github.com/c-h-david/rapid2/actions/workflows/CI.yml
[URL_GHA_CD]: https://github.com/c-h-david/rapid2/actions/workflows/CD.yml
[URL_RAPHUB]: http://rapid-hub.org/
[URL_DISCUS]: https://github.com/c-h-david/rapid2/discussions
[URL_ISSUES]: https://github.com/c-h-david/rapid2/issues
[URL_DOCFIL]: https://github.com/c-h-david/rapid2/blob/main/Dockerfile
[URL_CI_YML]: https://github.com/c-h-david/rapid2/blob/main/.github/workflows/CI.yml
[URL_REQAPT]: https://github.com/c-h-david/rapid2/blob/main/requirements.apt
[URL_REQPIP]: https://github.com/c-h-david/rapid2/blob/main/requirements.pip
[URL_REPOSI]: https://github.com/c-h-david/rapid2/blob/main/

[URL_DOCSFT]: https://www.docker.com/community-edition#/download
[URL_DEBIAN]: https://cloud.debian.org/images/archive/12.7.0/arm64/iso-cd/debian-12.7.0-arm64-netinst.iso
