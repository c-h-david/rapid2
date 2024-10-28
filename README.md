# RAPID2

[![License (3-Clause BSD)](https://img.shields.io/badge/license-BSD%203--Clause-yellow.svg)](https://github.com/c-h-david/rapid2/blob/main/LICENSE)

## Installation with Docker

Installing RAPID2 is **by far the easiest with Docker**. This document was
written and tested using
[Docker Community Edition](https://www.docker.com/community-edition#/download)
which is available for free and can be installed on a wide variety of operating
systems. To install it, follow the instructions in the link provided above.

Note that the experienced users may find more up-to-date installation
instructions in
[Dockerfile](https://github.com/c-h-david/rapid2/blob/main/Dockerfile).

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
[Debian 12.7.0 ARM64](https://get.debian.org/images/release/current/arm64/iso-cd/debian-12.7.0-arm64-netinst.iso)
installed, *i.e.* **no update** was performed, and **no upgrade** either.
Similar steps **may** be applicable for Ubuntu.

Note that the experienced users may find more up-to-date installation
instructions in
[CI.yml](https://github.com/c-h-david/rapid2/blob/main/.github/workflows/CI.yml).

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
[requirements.apt](https://github.com/c-h-david/rapid2/blob/main/requirements.apt)
and can be installed with `apt-get`. All packages can be installed at once using:

```bash
sudo apt-get install -y --no-install-recommends $(grep -v -E '(^#|^$)' requirements.apt)
```

> Alternatively, one may install the APT packages listed in
> [requirements.apt](https://github.com/c-h-david/rapid2/blob/main/requirements.apt)
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
[requirements.pip](https://github.com/c-h-david/rapid2/blob/main/requirements.pip)
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
> [requirements.pip](https://github.com/c-h-david/rapid2/blob/main/requirements.pip)
> one by one, for example:
>
> ```bash
> pip3 install flake8==7.1.1
> ```
