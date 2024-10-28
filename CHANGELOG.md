# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0).

## [Unreleased]

### Added

| File                         | Note |
| ----                         | ---- |
| `./CHANGELOG`                | New file. |
| `./Dockerfile`               | New file. |
| `./LICENSE`                  | New file. |
| `./README.md`                | New file. |
| `./requirement.apt`          | New file. |
| `./requirement.pip`          | New file. |
| `./src/bas_vec.py`           | New file. |
| `./src/con_vec.py`           | New file. |
| `./src/hsh_tbl.py`           | New file. |
| `./src/net_mat.py`           | New file. |
| `./src/k_x_vec.py`           | New file. |
| `./src/ccc_mat.py`           | New file. |
| `./src/rte_mat.py`           | New file. |
| `./src/fak_m3r.py`           | New file. |
| `./.github/workflows/CD.yml` | New file. |
| `./src/m3r_mdt.py`           | New file. |
| `./src/stp_cor.py`           | New file. |
| `./src/chk_ids.py`           | New file. |
| `./src/chk_top.py`           | New file. |
| `./.github/workflows/CI.yml` | New file. |
| `./src/Qou_mdt.py`           | New file. |
| `./src/mus_rte.py`           | New file. |

### Changed

| File                         | Note |
| ----                         | ---- |
| `./src/con_vec.py`           | Changed type hinting and updated docstring. |
| `./CHANGELOG`                | Changed to table format. |
| `./src/bas_vec.py`           | Updated docstring. |
| `./src/con_vec.py`           | Updated docstring. |
| `./src/hsh_tbl.py`           | Updated docstring. |
| `./src/k_x_vec.py`           | Used simpler test values. |
| `./src/ccc_mat.py`           | Used simpler test values. |
| `./src/rte_mat.py`           | Used simpler test values. |
| `./src/net_mat.py`           | Changed network matrix to float64. |
| `./requirement.pip`          | Updated for yamllint. |
| `./.github/workflows/CD.yml` | Updated for yamllint. |
| `./src/fak_m3r.py`           | Replaced compressed() by filled(). |
| `./src/ccc_mat.py`           | Replaced type of routing time step. |
| `./.github/workflows/CD.yml` | Fixed typo. |
| `./.github/workflows/CD.yml` | Updated to Ubuntu 22.04. |
| `./.github/workflows/CI.yml` | Updated to Ubuntu 22.04. |
| `./.github/workflows/CI.yml` | Activated virtual environment. |
| `./src/fak_m3r.py`           | Refined global attributes. |
| `./Dockerfile`               | Updated Debian. |
| `./.github/workflows/CI.yml` | Added pymarkdown. |
| `./requirement.pip`          | Added pymarkdown. |
| `./README.md`                | Added installation instructions. |
| `./src/Qou_mdt.py`           | Changed mypy ignore comment. |
| `./src/ccc_mat.py`           | Changed mypy ignore comment. |
| `./src/fak_m3r.py`           | Changed mypy ignore comment. |
| `./src/m3r_mdt.py`           | Changed mypy ignore comment. |
| `./src/net_mat.py`           | Changed mypy ignore comment. |
| `./src/rte_mat.py`           | Changed mypy ignore comment. |
| `./src/bas_vec.py`           | Fixed typo. |
| `./src/con_vec.py`           | Fixed typo. |
| `./src/hsh_tbl.py`           | Fixed typo. |
| `./src/rte_mat.py`           | Fixed typo. |
| `./src/bas_vec.py`           | Used try and except for opening files. |
| `./src/con_vec.py`           | Used try and except for opening files. |
| `./src/k_x_vec.py`           | Used try and except for opening files. |
