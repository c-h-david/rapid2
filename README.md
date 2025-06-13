# RAPID2

[![License (3-Clause BSD)][BDG_BSD3CL]][URL_LICENS]

[![Contributor Covenant][BDG_CONDUC]][URL_CONDUC]

[![Code of Collab][BDG_COLLAB]][URL_COLLAB]

[![SLIM][BDG___SLIM]][URL___SLIM]

[![GitHub CI Status][BDG_GHA_CI]][URL_GHA_CI]

[![GitHub CI Status][BDG_GHA_CD]][URL_GHA_CD]

[![Docker Images][BDG_DKRIMG]][URL_DKRIMG]

The Routing Application for Programmed Integration of Discharge (RAPID) is a
river network routing model. Given external inflow to rivers, this model can
compute the flow of water everywhere in river networks made out of many
thousands of reaches.

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
pip3 install .
```

### Run Instructions

```bash
rapid2 -nl namelist.yml
```

OR

```bash
rapid2 --namelist namelist.yml
```

### Usage Examples

Below is an example of what `namelist.yml` should include:

```yaml
---
Qex_ncf: './input/Test/Qext_Test_20000101_20000102.nc4'
Q00_ncf: './input/Test/Qinit_Test_20000101_20000102.nc4'

con_csv: './input/Test/rapid_connect_Test.csv'
kpr_csv: './input/Test/k_Test.csv'
xpr_csv: './input/Test/x_Test.csv'

bas_csv: './input/Test/riv_bas_id_Test.csv'

IS_dtR: 900

Qou_ncf: './output/Test/Qout_Test_20000101_20000102_tst.nc4'
Qfi_ncf: './output/Test/Qfinal_Test_20000101_20000102_tst.nc4'
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

<!-- pyml disable-num-lines 30 line-length-->
[BDG_BSD3CL]: https://img.shields.io/badge/license-BSD%203--Clause-yellow.svg
[BDG_CONDUC]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
[BDG_COLLAB]: https://img.shields.io/badge/Code%20of%20Collab-DRAFT-violet.svg
[BDG___SLIM]: https://img.shields.io/badge/Best%20Practices%20from-SLIM-blue
[BDG_GHA_CI]: https://github.com/c-h-david/rapid2/actions/workflows/CI.yml/badge.svg
[BDG_GHA_CD]: https://github.com/c-h-david/rapid2/actions/workflows/CD.yml/badge.svg
[BDG_DKRIMG]: https://img.shields.io/badge/docker-images-blue?logo=docker

[URL_LICENS]: https://github.com/c-h-david/rapid2/blob/main/LICENSE
[URL_CONDUC]: https://github.com/c-h-david/rapid2/blob/main/CODE_OF_CONDUCT.md
[URL_COLLAB]: https://github.com/c-h-david/rapid2/blob/main/CODE_OF_COLLAB.md
[URL___SLIM]: https://nasa-ammos.github.io/slim/
[URL_GHA_CI]: https://github.com/c-h-david/rapid2/actions/workflows/CI.yml
[URL_GHA_CD]: https://github.com/c-h-david/rapid2/actions/workflows/CD.yml
[URL_DKRIMG]: https://hub.docker.com/r/chdavid/rapid/tags

[URL_RAPHUB]: http://rapid-hub.org/
[URL_DISCUS]: https://github.com/c-h-david/rapid2/discussions
[URL_ISSUES]: https://github.com/c-h-david/rapid2/issues
[URL_REQAPT]: https://github.com/c-h-david/rapid2/blob/main/requirements.apt
[URL_TSTING]: https://github.com/c-h-david/rapid2/blob/main/TESTING.md
[URL_CHGLOG]: https://github.com/c-h-david/rapid2/blob/main/CHANGELOG.md
[URL_RELEAS]: https://github.com/c-h-david/rapid2/releases
[URL_CONTRI]: https://github.com/c-h-david/rapid2/blob/main/CONTRIBUTING.md
[URL_CONDUC]: https://github.com/c-h-david/rapid2/blob/main/CODE_OF_CONDUCT.md
[URL_COLLAB]: https://github.com/c-h-david/rapid2/blob/main/CODE_OF_COLLAB.md
[URL_GOVERN]: https://github.com/c-h-david/rapid2/blob/main/GOVERNANCE.md
[URL_GITCHD]: https://github.com/c-h-david
