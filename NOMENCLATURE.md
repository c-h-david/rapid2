# Nomenclature

This document defines the canonical naming system used in RAPID2 for data
structures, files, and functions. The goal is to ensure consistency, clarity,
and quick recognition across the codebase.

RAPID2 uses groups of one, three, or four semantic characters to unify names
across structures, files, and functions. This document serves as a quick
reference for these naming conventions.

## Enforcement

These guidelines are strictly enforced for the core routing model
(`_rapid2.py`), the `rapid2` library, and all internal data utilities (e.g.,
`_cmpncf.py`, `_cpllsm.py`).

The download utility (`_dgldas2.py`) is formally exempt from strict checking
to accommodate external API terminology.

## Semantic singleton

> These are used exclusively as prefixes in data structure names.

### `<type>`

| Code | Meaning            | Notes                                           |
| ---- | ------------------ | ----------------------------------------------- |
| `I`  | Integer            | Used for IDs, counters, and totals.             |
| `J`  | Integer (iterated) | Used exclusively for loop indices.              |
| `Z`  | Float              | Used for discharge, coordinates, parameters.    |
| `Y`  | String/character   | Used for variable names and text labels.        |
| `B`  | Boolean            | Used for logical masks and status flags.        |
| `A`  | Any                | Heterogeneous types.                            |

### `<structure1>`

| Code | Meaning            | Notes                                           |
| ---- | ------------------ | ----------------------------------------------- |
| `S`  | Scalar (0-D)       | A single value.                                 |
| `V`  | Vector (1-D)       | A 1-dimensional sequence or array of values.    |
| `M`  | Matrix (2-D)       | A 2-dimensional sequence or grid of values.     |
| `T`  | Table/Dictionary   | A mapping of keys to values (hash tables).      |

## Semantic Triplets

> These triplets appear consistently in the naming of data structures, files,
> and functions to define the subject or target.

### `<quantity>`

| Code | Meaning            | Notes                                           |
| ---- | ------------------ | ----------------------------------------------- |
| `riv`| River ID           | Unique identifier for each river reach (-).     |
| `dwn`| Downstream ID      | Downstream identifier (-).                      |
| `obs`| Observation ID     | Reach identifier where observations exist (-).  |
| `kpr`| k parameter        | Muskingum parameter k (s).                      |
| `xpr`| x parameter        | Muskingum parameter x (-).                      |
| `C1p`| C1 parameter       | Muskingum parameter C1 (-).                     |
| `C2p`| C2 parameter       | Muskingum parameter C2 (-).                     |
| `C3p`| C3 parameter       | Muskingum parameter C3 (-).                     |
| `tim`| Time               | Time stamps for simulation steps (s).           |
| `dtR`| Delta-T Routing    | Duration of Muskingum routing time step (s).    |
| `dtE`| Delta-T External   | Duration of external forcing time step (s).     |
| `dtO`| Delta-T Observation| Duration of observational time step (s).        |
| `rat`| Ratio              | Integer ratio between two time steps (-).       |
| `Qex`| External inflow    | Flow of water entering from exterior (m^3/s).   |
| `Qou`| Outflow discharge  | Flow of water exiting each reach (m^3/s).       |
| `Qob`| Observed discharge | Flow of water from observations (m^3/s).        |
| `Vol`| Volume             | Volume of water stored in the reach (m^3).      |
| `lon`| Longitude          | Representative longitude of the reach (°).      |
| `lat`| Latitude           | Representative latitude of the reach (°).       |
| `skm`| Contributing area  | Area of the contributing catchment (km^2).      |
| `scl`| Scaling factor     | Multiplier for scaling or unit conversion (-).  |
| `rsf`| Surface runoff     | Flow of water over the land surface (kg/m^2/s). |
| `rsb`| Subsurface runoff  | Flow of water within the subsurface (kg/m^2/s). |
| `run`| Total runoff       | Total surface and subsurface runoff (kg/m^2/s). |
| `0bi`| Zero-based i index | First dimension index (Python-native) (-).      |
| `0bj`| Zero-based j index | Second dimension index (Python-native) (-).     |
| `1bi`| One-based i index  | First dimension index (Fortran-native) (-).     |
| `1bj`| One-based j index  | Second dimension index (Fortran-native) (-).    |
| `fll`| Fill value         | Missing data or masked data (-).                |
| `val`| Generic value      | Generic value being compared (varies).          |
| `adf`| Absolute difference| Absolute difference (>=0) in `val` (varies).    |
| `rdf`| Relative difference| Relative difference (>=0) in `val` (-).         |
| `atl`| Absolute tolerance | Acceptable absolute difference (varies).        |
| `rtl`| Relative tolerance | Acceptable relative difference (-).             |

### `<dataset>`

> Datasets represent file origins. A dataset can share its name with its
> primary quantity (e.g., `Qou`), or use a unique triplet for its context.

| Code | Meaning            | Notes (netCDF Dataset pointer)                  |
| ---- | ------------------ | ----------------------------------------------- |
| `nml`| Namelist           | Configuration and input file paths.             |
| `bas`| Basin              | Subset of the full routing network.             |
| `con`| Connectivity       | River network connectivity.                     |
| `cpl`| Coupling           | Land surface model to river network mapping.    |
| `crd`| Coordinates        | Geospatial longitude and latitude data.         |
| `lsm`| Land surface model | External boundary condition forcing data. (`c`) |
| `m3r`| External volume    | Legacy file format for external volume. (`d`)   |
| `Q00`| Initial outflow    | Initial outflow state of the network. (`e`)     |
| `Qex`| External inflow    | NetCDF file containing forcing data. (`f`)      |
| `Qou`| Outflow discharge  | NetCDF file containing routing results. (`g`)   |
| `Qfi`| Final outflow      | Final outflow state of the network. (`h`)       |
| `skl`| Skeleton           | Empty netCDF file structure for init. (`s`)     |
| `std`| Standard           | Core metadata like time and coordinates. (`s`)  |
| `prv`| Previous           | File from a prior run. (`p`)                    |
| `now`| Current            | File from another run. (`n`)                    |

### `<qualifier>`

| Code | Meaning            | Notes                                           |
| ---- | ------------------ | ----------------------------------------------- |
| `tot`| Total network      | Array length equals `IS_riv_tot`.               |
| `bas`| Basin              | Array length equals `IS_riv_bas`.               |
| `lsm`| Land surface model | Associated with the external LSM grid/domain.   |
| `prv`| Previous value     | Previous state of a dynamic variable.           |
| `now`| Current value      | Current state of a dynamic variable.            |
| `avg`| Average value      | Time-averaged dynamic variable.                 |
| `all`| Complete sequence  | Used for arrays spanning the entire time domain.|
| `tmp`| Temporary value    | Non-persistent, for computation or validation.  |
| `Qex`| External inflow    | Associated with the external forcing timescale. |
| `Qob`| Observed discharge | Associated with the observation timescale.      |

### `<concept>`

> Algorithmic abstractions related to linear algebra and routing physics.

| Code | Meaning            | Notes                                           |
| ---- | ------------------ | ----------------------------------------------- |
| `Idt`| Identity matrix    | A must-have matrix for linear algebra.          |
| `Net`| Network matrix     | Represents topological connectivity.            |
| `CCC`| Muskingum CCC      | C1, C2, and C3 Muskingum parameter matrices.    |
| `ICN`| Identity minus C1N | Linear system matrix for Muskingum routing.
| `ImN`| Identity minus N   | Linear system matrix for Lumped routing.
| `Mus`| Muskingum          | The Muskingum routing physics and matrices.     |
| `Aex`| Ae operator        | Window mapping operator for external forcing.   |
| `A00`| A0 operator        | Window mapping operator for initial state.      |
| `Wdw`| Time window        | Temporal window for data assimilation.          |
| `Lmp`| Lumped             | The Lumped routing physics and matrices.        |

### `<structure2>` (Memory Destinations)

| Code | Meaning            | Notes                                           |
| ---- | ------------------ | ----------------------------------------------- |
| `vec`| Vector             | Assembled 1-dimensional array in memory.        |
| `mat`| Matrix             | Assembled 2-dimensional sparse matrix.          |
| `tbl`| Table              | Assembled dictionary or hash table.             |

### `<format>` (Disk Destinations)

| Code | Meaning            | Notes                                           |
| ---- | ------------------ | ----------------------------------------------- |
| `csv`| Comma Separated    | Used for tabular text data and parameters.      |
| `ncf`| NetCDF             | Used for scientific multi-dimensional data.     |
| `yml`| YAML               | Used for model configuration inputs.            |

## Semantic Quadruplets

### `<verb>`

> Exactly four characters dictating the function's action and destination.

| Code | Meaning            | Notes                                           |
| ---- | ------------------ | ----------------------------------------------- |
|`read`| Disk --> Memory    | Loads static data from files into RAM.          |
|`make`| Memory --> Memory  | Assembles arrays into complex structures.       |
|`prep`| Memory --> Disk    | Initializes a file with static data.            |
|`chck`| Memory --> Void    | Check arrays from file; raises error or logs.   |
|`calc`| Memory --> Scalar  | Computes one-time mathematical constants.       |
|`updt`| State --> State    | Advances physics through the time loop.         |
|`assm`| State --> State    | Assimilates observations to correct states.     |

## Data Structure Names

**Pattern:** `<type><structure1>_<quantity>_[<qualifier>]`
**or:** `<type><structure1>_<concept>`

**Examples:**

| Code             | Meaning            | Notes                               |
| ---------------- | ------------------ | ----------------------------------- |
| `IV_riv_tot`     | Total river IDs    | Integer vector of all river IDs.    |
| `IV_tim_all`     | All time stamps    | Integer vector of all time stamps.  |
| `ZV_lat_tot`     | Total latitudes    | Float vector of all latitudes.      |
| `ZM_Net`         | Network matrix     | Float matrix of network connect.    |

**Exemptions:**

The following are exempt from strict triplet checking, though they must
still obey the `<type><structure1>_` prefix:

- **Algebraic Idioms:** Data structures representing pure mathematical
  abstractions confined within a single function (e.g., right-hand side vectors
  `rhs` or `rh1`, equation denominators `den`, or Greek letter placeholders
   like `Alp` or `Bet`).
- **Sparse Matrix Idioms:** Standard coordinate arrays used for sparse matrix
  assembly (`row`, `col`, `val`).

The following are exempt from strict triplet checking and `<type><structure1>_`
prefix:

- **Interface Idioms:** Conventional variables representing standard parsing
  interfaces (e.g., `args`, `parser`) when used strictly for command-line or
  configuration parsing (e.g., `argparse`, YAML loaders).
- **NetCDF Toolbox Idioms:** Handles for `netCDF4` objects to maintain direct
  mapping with disk-level structures:
  - **Datasets:** Must use the single character assigned in the `<dataset>`
    table "Notes" column, if available (e.g., `f`, `g`).
  - **Variables/Dimensions:** Must match the exact string name of the target
    item (e.g., `Qout = g.createVariable("Qout", ...)`).
  - **Dynamic Iteration:** The generic labels `name`, `var`, and `dim` are
    permitted during loops.

## File Names

**Pattern:** `<dataset>_<format>`

**Examples:**

| Code             | Meaning            | Notes                               |
| ---------------- | ------------------ | ----------------------------------- |
| `bas_csv`        | Basin info         | CSV file with subset of river IDs.  |
| `Qex_ncf`        | External inflow    | NetCDF file containing forcing data.|
| `nml_yml`        | Namelist           | YAML file for model configuration.  |

## Function Names

**Functional Scope:** To maintain mathematical clarity, functions are reserved
for heavy I/O, complex assembly, or physics routines. Simple operations—such
as unit conversions or array equality checks—should remain inline to reduce
cognitive load and preserve the visibility of the naming grammar.

### Readers (Disk -> Memory)

**Pattern:** `read_<dataset>_<structure2>()`

**Examples:**

| Code             | Meaning            | Notes                               |
| ---------------- | ------------------ | ----------------------------------- |
| `read_bas_vec()` | Read basin vector  | Loads basin IDs into a 1D array.    |
| `read_con_vec()` | Read connectivity  | Loads connectivity into 1D arrays.  |
| `read_cpl_vec()` | Read coupling      | Loads mapping indices into arrays.  |
| `read_nml_tbl()` | Read namelist      | Loads configuration into a dict.    |

### Makers (Memory -> Memory)

**Pattern:** `make_<quantity>_<structure2>()`
**or:** `make_<concept>_<structure2>()`

**Examples:**

| Code             | Meaning            | Notes                               |
| ---------------- | ------------------ | ----------------------------------- |
| `make_0bi_tbl()` | Make 0-base index  | Builds dictionary mapping to 0bi.   |
| `make_net_mat()` | Make network mat   | Assembles connectivity matrix.      |
| `make_ccc_mat()` | Make CCC matrix    | Assembles C1, C2, C3 matrices.      |
| `make_lin_mat()` | Make linear mat    | Assembles linear routing system.    |

### Preparers (Memory -> Disk)

**Pattern:** `prep_<dataset>_<format>()`

**Examples:**

| Code             | Meaning            | Notes                               |
| ---------------- | ------------------ | ----------------------------------- |
| `prep_skl_ncf()` | Prepare skeleton   | Initializes `skl_ncf` file.         |
| `prep_Qou_ncf()` | Prepare Qou file   | Initializes `Qou_ncf` file.         |

### Checkers (Memory -> Void)

**Pattern:** `chck_<dataset>()`

**Examples:**

| Code             | Meaning            | Notes                               |
| ---------------- | ------------------ | ----------------------------------- |
| `chck_bas()`     | Check basin.       | Validates upstream/downstream sort. |
| `chck_cpl()`     | Check coupling     | Validates null indices and areas.   |

### Updaters (State -> State)

**Pattern:** `updt_<concept>_<quantity>()`

**Examples:**

| Code             | Meaning            | Notes                               |
| ---------------- | ------------------ | ----------------------------------- |
| `updt_mus_Qou()` | Update Muskingum   | Routes `Qou` flow forward.          |

### Assimilators (State -> State)

**Pattern:** `assm_<concept>_<quantity>()`

**Examples:**

| Code             | Meaning            | Notes                               |
| ---------------- | ------------------ | ----------------------------------- |
| `assm_mus_Qex()` | Assimilate Kalman  | Corrects `Qex` using observations.  |
