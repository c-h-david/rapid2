# RAPID2 Tutorial

> ⚠️ DRAFT. Work in progress.

This tutorial demonstrates a real scientific workflow using RAPID2. It focuses
on obtaining input data, running the model, and verifying that results match
expectations.

All commands below are written in `bash`. This example is intended to serve as
a primary reference for new users.

## 1. Get Started

Create working directories:

``` bash
mkdir -p input/Tutorial
mkdir -p output/Tutorial
```

We'll be using files from a Zenodo repository:

[![DOI:10.5281/zenodo.8248069][SVG_ZENODO]][URL_ZENODO]

Specifically, the following files are needed:

- `rapid_connect_pfaf_ii.zip`
- `coords_pfaf_ii.zip`
- `rapid_coupling_pfaf_ii_GLDAS.zip`

For this tutorial, we use the `pfaf_74` files, corresponding to the Mississippi
River Basin.

## 2. Download Raw Runoff Data with `dgldas2`

Download GLDAS phase `2.1`, model `VIC`, for `2010-01`:

``` bash
dgldas2 \
    --phase 2.1 \
    --model VIC \
    --time 2010-01 \
    --land_surface_model \
    input/Tutorial/GLDAS_2.1_VIC_2010-01.nc4
```

The new file is placed in `input/Tutorial`. Other files are also automatically
downloaded in that directory and removed after use.

> Note: GLDAS `2.0` is also supported, as are the `CLSM` and `NOAH` models.

## 3. Transform Runoff to RAPID External Inflow with `cpllsm`

Convert the GLDAS runoff file into RAPID external inflow format:

``` bash
cpllsm \
    --land_surface_model \
    input/Tutorial/GLDAS_2.1_VIC_2010-01.nc4 \
    --connectivity \
    input/Tutorial/rapid_connect_pfaf_74.csv \
    --coordinates \
    input/Tutorial/coords_pfaf_74.csv \
    --coupling \
    input/Tutorial/rapid_coupling_pfaf_74_GLDAS.csv \
    --external_inflow \
    input/Tutorial/Qext_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4
```

## 4. Create Cold Start File with `zeroqinit`

``` bash
zeroqinit \
    --external_inflow \
    input/Tutorial/Qext_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4 \
    --initial_outflow \
    input/Tutorial/Qinit_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4
```

## 5. Run the Routing Model with `rapid2`

Using the following content in a file called `namelist_Tutorial.md`

```yaml
# -----------------------------------------------------------------------------
# Mandatory input files
# -----------------------------------------------------------------------------
Qex_ncf: './input/Tutorial/Qext_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4'
Q00_ncf: './input/Tutorial/Qinit_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4'

con_csv: './input/Tutorial/rapid_connect_pfaf_74.csv'
kpr_csv: './input/Tutorial/k_pfaf_74_nrm.csv'
xpr_csv: './input/Tutorial/x_pfaf_74_nrm.csv'

bas_csv: './input/Tutorial/riv_bas_id_pfaf_74_topo.csv'

# -----------------------------------------------------------------------------
# Mandatory values
# -----------------------------------------------------------------------------
IS_dtR: 900

# -----------------------------------------------------------------------------
# Mandatory output files
# -----------------------------------------------------------------------------
Qou_ncf: './output/Tutorial/Qout_pfaf_74_GLDAS_2.1_VIC_2010-01_tst.nc4'
Qfi_ncf: './output/Tutorial/Qfinal_pfaf_74_GLDAS_2.1_VIC_2010-01_tst.nc4'
```

``` bash
rapid2 --namelist input/Tutorial/namelist_Tutorial.yml
```

## 6. Compare Files to Baseline with `cmpncf`

``` bash
cmpncf \
    --previous \
    input/Tutorial/Qinit_pfaf_74_GLDAS_2.1_VIC_2010-01_GOLD.nc4 \
    --current \
    input/Tutorial/Qinit_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4 \
    --relative_tolerance 1e-6 \
    --absolute_tolerance 1e-3
```

```bash
cmpncf \
    --previous \
    input/Tutorial/Qext_pfaf_74_GLDAS_2.1_VIC_2010-01_GOLD.nc4 \
    --current \
    input/Tutorial/Qext_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4 \
    --relative_tolerance 1e-6 \
    --absolute_tolerance 1e-3
```

``` bash
cmpncf \
    --previous \
    output/Tutorial/Qout_pfaf_74_GLDAS_2.1_VIC_2010-01_GOLD.nc4 \
    --current \
    output/Tutorial/Qout_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4 \
    --relative_tolerance 1e-6 \
    --absolute_tolerance 1e-3
```

```bash
cmpncf \
    --previous \
    output/Tutorial/Qfinal_pfaf_74_GLDAS_2.1_VIC_2010-01_GOLD.nc4 \
    --current \
    output/Tutorial/Qfinal_pfaf_74_GLDAS_2.1_VIC_2010-01.nc4 \
    --relative_tolerance 1e-6 \
    --absolute_tolerance 1e-3
```

## Current Known Challenges to Command Line Interface

The near-term focus is on:

- Clear, consistent runtime options
- Short, intuitive 3-letter flags
- Minimalistic and readable design

At this stage, the tools remain separate commands rather than subcommands
(e.g., like `git commit` or `git clone`). Unifying these under `rapid2` may be
considered in the future.

## Opportunities for Growth

This tutorial is intended to expand over time to include:

- Inspecting input datasets
- Examining model outputs
- Basic interpretation and analysis

<!-- pyml disable-num-lines 30 line-length -->
[SVG_ZENODO]: https://zenodo.org/badge/doi/10.5281/zenodo.8248069.svg

[URL_ZENODO]: https://doi.org/10.5281/zenodo.8248069
