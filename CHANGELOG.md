# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0b3] - 2026-07-07

### Added

- **Sandbox Downloader (`dsandbox`)**: Introduced a CLI utility using `pooch`
  to automate the downloading of Sandbox synthetic datasets directly from
  Zenodo.
- **Model Equivalents (`subsampleqout`)**: Added a CLI utility to spatially and
  temporally sub-sample discharge outputs (`Qou`) to match observation
  locations and cadences, generating model equivalents (`Qme`).
- **Hydrograph Plotting (`hydrographs`)**: Added a CLI utility leveraging
  `toyplot` to generate standalone SVG hydrographs comparing observations
  (`Qob`) against model equivalents (`Qme`).
- **Dependencies**: Added `toyplot` (`>=2.1.0`) and `pooch` (`>=1.9.0`) to the
  core requirements.

### Changed

- **Riv ID Vector Reader**: Generalized `read_bas_vec.py` to `read_riv_vec.py`
  to support reading arbitrary subsets of river IDs (e.g., basins, observation
  gages).
- **Sandbox Dataset**: Updated the synthetic Sandbox test suite to exaggerate
  land surface model biases (missing baseflow, exaggerated amplitudes) using a
  "multiples-of-5" mathematical design. Updated the dataset source to Zenodo
  record (`21248920`).
- **Nomenclature Rules**: Expanded `NOMENCLATURE.md` to support observational
  data concepts (`Qob`, `Qme`), new array size bounds (`avl`, `act`), and plot
  formatting prefixes/suffixes (`hyd`, `svg`).

## [2.0.0b2] - 2026-06-16

### Added

- **Legacy Conversion Tool (`rapid1to2`)**: Introduced a new CLI utility to
  easily convert legacy RAPID1 `.csv` static files into the new RAPID2
  `.parquet` format.
- **Explicit Routing Matrices (`make_Wdx_mat`)**: Added an explicit routing
  matrix builder for time-averaged discharge over a window, using a time-lagged
  semi-implicit Muskingum method to bypass computationally expensive matrix
  inversions (this is highly EXPERIMENTAL).
- **Docker Hub Automation**: Added a step in the GitHub Actions CD pipeline to
  automatically sync the `README.md` to Docker Hub upon release.
- **Citation Update**: Added a new Zenodo DOI (`10.5281/zenodo.19393023`) to
  `CITATION.cff` and `README.md`.

### Changed

- **Parquet I/O Migration**: Transitioned the core I/O for network
  connectivity, parameters, and coordinate files from standard CSVs to Apache
  Parquet via `pyarrow`. This drastically improves read speeds and provides
  strict type enforcement.
- **Dependency Updates**: Added `pyarrow` (`>=24.0.0`) as a core project
  requirement. Added `pyarrow-stubs` and `parq-cli` to the developer
  dependencies.
- **Sandbox Updates**: Migrated the synthetic Sandbox test suite to use
  `.parquet` inputs and updated the dataset source to a new Zenodo record
  (`20671995`).
- **Documentation Overhaul**: Moved the tutorial from the repository to the
  external RAPID Hub documentation site. Updated `README.md` with new project
  badges (PyPI, Docker pulls, Linters) and modernized configuration examples.
- **Nomenclature Rules**: Updated the internal terminology guidelines
  (`NOMENCLATURE.md`) to reflect the new `pqt` format and include specific rule
  exemptions for `pyarrow` and `argparse` idioms.

## [2.0.0b1] - 2026-04-02

### Changed

- **Transition to Python**: Complete architectural shift from legacy Fortran 90
  to a modern, object-oriented Python 3 framework (RAPID2).
- **Project Structure**: Adopted standard Python packaging and a
  `pyproject.toml` ecosystem, replacing legacy Makefile builds.
- **Core Methodology**: Prioritized readability and integration with the modern
  scientific stack (NumPy, SciPy, netCDF4) while maintaining consistency with
  original Muskingum routing physics.
- **Standard Open Source Practices**: Implemented SLIM guidelines, including
  formalized `CODE_OF_CONDUCT`, `CODE_OF_COLLAB`, and `CONTRIBUTING`
  documentation.
- **Project Nomenclature**: Enhanced and formalized the original RAPID
  naming conventions within a strict `NOMENCLATURE.md` framework.

### Added

- **Initial Beta Release** of the Python 3 implementation.
- **Standardized CLI Tools** for river routing and data preprocessing.
- **Automated CI/CD Pipelines**: Enforced strict linting, formatting, and
  testing via GitHub Actions with deployment to Docker Hub and PyPI.
- **Modernized Testing Suite**: Transitioned to `doctest` and synthetic Sandbox
  experiments for rapid verification, replacing the full reproduction of past
  paper results.
