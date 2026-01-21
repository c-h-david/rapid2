# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0).

## [Unreleased]

### Added

| File                         | Note |
| ----                         | ---- |
| `./CHANGELOG.md`             | New file. |
| `./Dockerfile`               | New file. |
| `./LICENSE`                  | New file. |
| `./README.md`                | New file. |
| `./requirement.apt`          | New file. |
| `./requirement.pip`          | New file. |
| `./src/rapid2/bas_vec.py`    | New file. |
| `./src/rapid2/con_vec.py`    | New file. |
| `./src/rapid2/hsh_tbl.py`    | New file. |
| `./src/rapid2/net_mat.py`    | New file. |
| `./src/rapid2/k_x_vec.py`    | New file. |
| `./src/rapid2/ccc_mat.py`    | New file. |
| `./src/rapid2/rte_mat.py`    | New file. |
| `./src/rapid2/fak_m3r.py`    | New file. |
| `./.github/workflows/CD.yml` | New file. |
| `./src/rapid2/m3r_mdt.py`    | New file. |
| `./src/rapid2/stp_cor.py`    | New file. |
| `./src/rapid2/chk_ids.py`    | New file. |
| `./src/rapid2/chk_top.py`    | New file. |
| `./.github/workflows/CI.yml` | New file. |
| `./src/rapid2/Qou_mdt.py`    | New file. |
| `./src/rapid2/mus_rte.py`    | New file. |
| `./TESTING.md`               | New file. |
| `./CODE_OF_COLLAB.md`        | New file. |
| `./.yamllint.yml`            | New file. |
| `./.pymarkdown.yml`          | New file. |
| `./.gitignore`               | New file. |
| `./pyproject.toml`           | New file. |
| `./src/rapid2/__init__.py`   | New file. |
| `./clean.sh`                 | New file. |
| `./src/_rapid2.py`           | New file. |
| `./CODE_OF_CONDUCT.md`       | New file. |
| `./GOVERNANCE.md`            | New file. |
| `./CONTRIBUTING.md`          | New file. |
| `.github/bug_report.md`      | New file. |
| `.github/feature_request.md` | New file. |
| `.github/PR_TEMPLATE.md`     | New file. |
| `./src/rapid2/nml_cfg.py`    | New file. |
| `./src/rapid2/Qfi_mdt.py`    | New file. |
| `./SANDBOX.md`               | New file. |
| `./src/_dgldas2.py`          | New file. |
| `./CITATION.cff`             | New file. |
| `./src/_m3rivtoqext.py`      | New file. |
| `./src/_zeroqinit.py`        | New file. |
| `./img/font_rapid_network.s` | New file. |
| `./img/icon_rapid_network.s` | New file. |
| `./src/_sandboxqext.py`      | New file. |
| `./tst/tst_dwnl_Sandbox.sh`  | New file. |
| `./.github/workflows/CL.yml` | New file. |
| `./src/rapid2/crd_vec.py`    | New file. |
| `./src/rapid2/cpl_vec.py`    | New file. |
| `./src/rapid2/chk_cpl.py`    | New file. |
| `./src/_cpllsm.py`           | New file. |
| `./src/rapid2/inv_mat.py`    | New file. |
| `./src/rapid2/wdw_mat.py`    | New file. |
| `./src/_cmpncf.py`           | New file. |

### Changed

| File                         | Note |
| ----                         | ---- |
| `./src/rapid2/con_vec.py`    | Changed type hinting and updated docstring. |
| `./CHANGELOG.md`             | Changed to table format. |
| `./src/rapid2/bas_vec.py`    | Updated docstring. |
| `./src/rapid2/con_vec.py`    | Updated docstring. |
| `./src/rapid2/hsh_tbl.py`    | Updated docstring. |
| `./src/rapid2/k_x_vec.py`    | Used simpler test values. |
| `./src/rapid2/ccc_mat.py`    | Used simpler test values. |
| `./src/rapid2/rte_mat.py`    | Used simpler test values. |
| `./src/rapid2/net_mat.py`    | Changed network matrix to float64. |
| `./requirement.pip`          | Updated for yamllint. |
| `./.github/workflows/CD.yml` | Updated for yamllint. |
| `./src/rapid2/fak_m3r.py`    | Replaced compressed() by filled(). |
| `./src/rapid2/ccc_mat.py`    | Replaced type of routing time step. |
| `./.github/workflows/CD.yml` | Fixed typo. |
| `./.github/workflows/CD.yml` | Updated to Ubuntu 22.04. |
| `./.github/workflows/CI.yml` | Updated to Ubuntu 22.04. |
| `./.github/workflows/CI.yml` | Activated virtual environment. |
| `./src/rapid2/fak_m3r.py`    | Refined global attributes. |
| `./Dockerfile`               | Updated Debian. |
| `./.github/workflows/CI.yml` | Added pymarkdown. |
| `./requirement.pip`          | Added pymarkdown. |
| `./README.md`                | Added installation instructions. |
| `./src/rapid2/Qou_mdt.py`    | Changed mypy ignore comment. |
| `./src/rapid2/ccc_mat.py`    | Changed mypy ignore comment. |
| `./src/rapid2/fak_m3r.py`    | Changed mypy ignore comment. |
| `./src/rapid2/m3r_mdt.py`    | Changed mypy ignore comment. |
| `./src/rapid2/net_mat.py`    | Changed mypy ignore comment. |
| `./src/rapid2/rte_mat.py`    | Changed mypy ignore comment. |
| `./src/rapid2/bas_vec.py`    | Fixed typo. |
| `./src/rapid2/con_vec.py`    | Fixed typo. |
| `./src/rapid2/hsh_tbl.py`    | Fixed typo. |
| `./src/rapid2/rte_mat.py`    | Fixed typo. |
| `./src/rapid2/bas_vec.py`    | Used try and except for opening files. |
| `./src/rapid2/con_vec.py`    | Used try and except for opening files. |
| `./src/rapid2/k_x_vec.py`    | Used try and except for opening files. |
| `./README.md`                | Fixed text. |
| `./Dockerfile`               | Linted with hadolint. |
| `./.github/workflows/CI.yml` | Added hadolint. |
| `./requirement.pip`          | Added hadolint. |
| `./TESTING.md`               | Fixed typos. |
| `./.github/workflows/CI.yml` | Added hadolint exception. |
| `./Dockerfile`               | Fixed quotes and added apt-get clean. |
| `./.github/workflows/CI.yml` | Linted. |
| `./CODE_OF_COLLAB.md`        | Linted. |
| `./README.md`                | Linted. |
| `./TESTING.md`               | Linted. |
| `./README.md`                | Fixed Debian URL. |
| `./TESTING.md`               | Added URLs. |
| `./.github/workflows/CI.yml` | Enforced max line width for Dockerfile. |
| `./TESTING.md`               | Enforced max line width for Dockerfile. |
| `./src/rapid2/*.py`          | Moved files to sub-directory. |
| `./.github/workflows/CI.yml` | Moved files to sub-directory. |
| `./pyproject.toml`           | Added links for repository and license. |
| `TESTING.md`                 | Moved files to sub-directory. |
| `./src/rapid2/*.py`          | Changed mode to not executable. |
| `./Dockerfile`               | Added package installation. |
| `./.github/workflows/CI.yml` | Added new directory with Python files. |
| `TESTING.md`                 | Added new directory with Python files. |
| `./pyproject.toml`           | Added rapid2 executable. |
| `./src/_rapid2.py`           | Added whitespace. |
| `.github/PR_TEMPLATE.md`     | Linted. |
| `./GOVERNANCE.md`            | Fixed typos. |
| `./src/rapid2/*.py`          | Changed relative path in docstrings. |
| `TESTING.md`                 | Added testing for examples in docstrings. |
| `./src/_rapid2.py`           | Added basic RAPID routing process. |
| `./README.md`                | Added badges and notable features. |
| `./clean.sh`                 | Added more directories to clean up. |
| `TESTING.md`                 | Specified runtime testing activities. |
| `./README.md`                | Changed for SLIM guidelines. |
| `./src/rapid2/Qou_mdt.py`    | Added comments. |
| `./src/rapid2/Qou_mdt.py`    | Updated global attributes. |
| `./src/rapid2/fak_m3r.py`    | Updated global attributes. |
| `./src/rapid2/Qfi_mdt.py`    | Defaulted time to upper bound of final step. |
| `./src/_rapid2.py`           | Saved final discharge state. |
| `./src/rapid2/Qfi_mdt.py`    | Saved final discharge state. |
| `./src/rapid2/nml_cfg.py`    | Saved final discharge state. |
| `./src/_rapid2.py`           | Read initial discharge state. |
| `./src/rapid2/nml_cfg.py`    | Read initial discharge state. |
| `./src/_rapid2.py`           | Resorted final discharge state. |
| `./SANDBOX.md`               | Clarified description. |
| `./src/_rapid2.py`           | Used single quotes. |
| `./src/rapid2/nml_cfg.py`    | Fixed typo in docstring. |
| `./requirement.pip`          | Added earthaccess. |
| `./pyproject.toml`           | Added executable for GLDAS2 download. |
| `.github/bug_report.yml`     | Modified format. |
| `.github/enhancement.yml`    | Modified format. |
| `./CONTRIBUTING.md`          | Clarified expectations. |
| `.github/bug_report.yml`     | Linted. |
| `.github/enhancement.yml`    | Linted. |
| `./CONTRIBUTING.md`          | Linted. |
| `TESTING.md`                 | Expanded testing for .yml files. |
| `./.github/workflows/CI.yml` | Expanded testing for .yml files. |
| `.github/bug_report.yml`     | Removed markdown shortcuts. |
| `.github/enhancement.yml`    | Removed markdown shortcuts. |
| `TESTING.md`                 | Checked .yml for configuration files. |
| `./.github/workflows/CI.yml` | Checked .yml for configuration files. |
| `./README.md`                | Specified BSD-3-Clause. |
| `.github/bug_report.yml`     | Ignored yamllint rules. |
| `.github/enhancement.yml`    | Ignored yamllint rules. |
| `./README.md`                | Linted. |
| `./README.md`                | Added badge for Code of Collab. |
| `./CODE_OF_COLLAB.md`        | Added collaboration matrix. |
| `./CODE_OF_COLLAB.md`        | Fixed typo. |
| `./README.md`                | Changed summary. |
| `./CODE_OF_COLLAB.md`        | Added CITATION.cff. |
| `./CITATION.cff`             | Edited text. |
| `./README.md`                | Refactored m3riv into Qext. |
| `./src/_rapid2.py`           | Refactored m3riv into Qext. |
| `./src/rapid2/nml_cfg.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/rud_new.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/Qex_new.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/Qou_new.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/Qfi_new.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/Qex_mdt.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/snd_Qex.py`    | Refactored m3riv into Qext. |
| `./src/_rapid2.py`           | Enabled execution as script. |
| `./src/rapid2/Qex_mdt.py`    | Added debugging for time step values. |
| `./src/rapid2/stp_cor.py`    | Added debugging for time step values. |
| `./pyproject.toml`           | Added executables for old m3riv and Qinit. |
| `./README.md`                | Added variables to example namelist. |
| `./src/_m3rivtoqext.py`      | Replaced float32 by int32 for precision. |
| `./README.md`                | Added venv instructions. |
| `./SANDBOX.md`               | Added sub-sections. |
| `./README.md`                | Added icon and font. |
| `./README.md`                | Allowed inline html. |
| `./CODE_OF_CONDUCT.md`       | Added space in pymarkdown disable. |
| `./CONTRIBUTING.md`          | Added space in pymarkdown disable. |
| `./README.md`                | Added space in pymarkdown disable. |
| `./SANDBOX.md`               | Changed QeT equation. |
| `./pyproject.toml`           | Added sandboxqext. |
| `./README.md`                | Modified icon and font links. |
| `./SANDBOX.md`               | Changed rendering for sign function. |
| `./README.md`                | Changed icon size. |
| `./src/_sandboxqext.py`      | Hardcoded global attributes. |
| `./src/_zeroqinit.py`        | Copied global attributes. |
| `./SANDBOX.md`               | Added initial state. |
| `./TESTING.md`               | Clarified Dockerfile linter. |
| `./README.md`                | Fixed pyml disable. |
| `./src/rapid2/*.py`          | Renamed Test into Sandbox. |
| `./README.md`                | Renamed Test into Sandbox. |
| `./src/_rapid2.py`           | Copied global attributes. |
| `./SANDBOX.md`               | Added Zenodo badge. |
| `./.github/workflows/CI.yml` | Added shell linter. |
| `./TESTING.md`               | Added shell linter. |
| `./clean.sh`                 | Added shell linter. |
| `./requirement.apt`          | Added shell linter. |
| `./.github/workflows/CI.yml` | Refactored for Sandbox. |
| `./README.md`                | Added Continuous Linting. |
| `./tst/tst_dwnl_Sandbox.sh`  | Fixed line width. |
| `./.github/workflows/CI.yml` | Added doctest. |
| `./.github/workflows/CI.yml` | Installed RAPID. |
| `./clean.sh`                 | Removed MacOS metadata file. |
| `./src/_dgldas2.py`          | Updated time values. |
| `./src/_dgldas2.py`          | Removed print statement. |
| `./src/rapid2/cpl_vec.py`    | Renamed variables. |
| `./src/rapid2/cpl_vec.py`    | Updated doctest example. |
| `./tst/tst_dwnl_Sandbox.sh`  | Updated version and added new file. |
| `./src/_cpllsm.py`           | Rewrote line for mypy. |
| `./pyproject.toml`           | Added cpllsm. |
| `./tst/tst_dwnl_Sandbox.sh`  | Updated URL and added coords file. |
| `./src/rapid2/rte_mat.py`    | Updated type of identity matrix. |
| `./src/rapid2/inv_mat.py`    | Added comment on computation method. |
| `./src/rapid2/mus_rte.py`    | Added new doctest checks. |
| `./src/rapid2/inv_mat.py`    | Used at sign for linear algebra products. |
| `./src/rapid2/mus_rte.py`    | Used at sign for linear algebra products. |
| `./src/rapid2/rte_mat.py`    | Used at sign for linear algebra products. |
| `./requirement.pip`          | Updated for hadolint-bin. |
| `./pyproject.toml`           | Fixed acronym. |
| `./src/rapid2/wdw_mat.py`    | Split Ae and A0, folded Bet earlier. |
| `./src/_cpllsm.py`           | Changed nc4 to ncf for consitency. |
| `./src/rapid2/Qex_mdt.py`    | Moved time step computation for broader use. |
| `./src/_rapid2.py`           | Moved time step computation for broader use. |
| `./src/_cmpncf.py`           | Used refactored metadata function. |
| `./src/*.py`                 | Changed raise SystemExit(22) to sys.exit(1). |
| `./src/rapid2/*.py`          | Changed raise SystemExit(22) to sys.exit(1). |
| `./src/*.py`                 | Added import sys. |
| `./src/rapid2/*.py`          | Added import sys. |
| `./src/*.py`                 | Used f-strings in warnings and errors. |
| `./src/rapid2/*.py`          | Used f-strings in warnings and errors. |
| `./src/*.py`                 | Used f-strings in print statements. |
| `./src/rapid2/*.py`          | Used f-strings in print statements. |
| `./src/_sandboxqext.py`      | Fixed typo. |
| `./src/_cmpncf.py`           | Added comparison of metadata. |
| `./src/_cmpncf.py`           | Added comparison of main variable. |
| `./src/_rapid2.py`           | Fixed bug: populate time and time bounds. |
| `./src/_cmpncf.py`           | Fixed bug: check actual presence of mask. |
| `./pyproject.toml`           | Added cmpncf executable. |
| `./src/_cmpncf.py`           | Removed unnecessary runtime log. |
| `./README.md`                | Fixed URL for Docker images. |
| `./src/_cmpncf.py`           | Made time bounds optional where appropriate. |
| `./src/_rapid2.py`           | Made time bounds optional where appropriate. |
| `./src/rapid2/Qex_mdt.py`    | Made time bounds optional where appropriate. |

### Removed

| `./src/rapid2/m3r_mdt.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/Qou_mdt.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/Qfi_mdt.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/fak_m3r.py`    | Refactored m3riv into Qext. |
| `./src/rapid2/snd_Qex.py`    | Refactored into sandboxqext. |
