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

Download GLDAS version `2.1`, model `VIC`, for `2010-01`:

``` bash
dgldas2 \
    --vsn 2.1 \
    --mod VIC \
    --tim 2010-01 \
    --dir input/Tutorial \
    --fil GLDAS_2.1_VIC_2010-01.nc4
```

The new file is placed in `input/Tutorial`. Other files are also automatically
downloaded in that directory and removed after use.

> Note: GLDAS `2.0` is also supported, as are the `CLSM` and `NOAH` models.

## 3. Transform Runoff to RAPID External Inflow with `cpllsm`

Convert the GLDAS runoff file into RAPID external inflow format:

``` bash
cpllsm \
    --lsm input/Tutorial/GLDAS_2.1_VIC_2010-01.nc4 \
    --con input/Tutorial/rapid_connect_pfaf_74.csv \
    --pos input/Tutorial/coords_pfaf_74.csv \
    --bnd input/Tutorial/rapid_coupling_pfaf_74_GLDAS.csv \
    --dir input/Tutorial \
    --fil Qext_GLDAS_2.1_VIC_2010-01.nc4
```

## 4. Create Cold Start File with `zeroqinit`

``` bash
zeroqinit \
    --input input/Tutorial/Qext_GLDAS_2.1_VIC_2010-01.nc4 \
    --output input/Tutorial/Qinit_GLDAS_2.1_VIC_2010-01.nc4
```

## 5. Run the Routing Model with `rapid2`

``` bash
rapid2 --namelist namelist_Sandbox.yml
```

## 6. Compare Output to Baseline with `cmpncf`

``` bash
cmpncf \
    --old input/Tutorial/Qinit_GLDAS_2.1_VIC_2010-01_GOLD.nc4 \
    --new input/Tutorial/Qinit_GLDAS_2.1_VIC_2010-01.nc4 \
    --rel 1e-6 \
    --abs 1e-3
```

## Current Known Challenges to Command Line Interface

The current command-line interface includes many options, some of which overlap
or duplicate functionality. A future goal is to reduce the number of options to
the minimal set necessary for clarity and ease of use.

At this stage, the tools remain separate commands rather than subcommands
(e.g., like `git commit` or `git clone`). Unifying these under `rapid2` may be
considered in the future.

The near-term focus is on:

- Clear, consistent runtime options
- Short, intuitive 3-letter flags
- Minimalistic and readable design

## Opportunities for Growth

This tutorial is intended to expand over time to include:

- Inspecting input datasets
- Examining model outputs
- Basic interpretation and analysis

<!-- pyml disable-num-lines 30 line-length -->
[SVG_ZENODO]: https://zenodo.org/badge/doi/10.5281/zenodo.8248069.svg

[URL_ZENODO]: https://doi.org/10.5281/zenodo.8248069
