# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
