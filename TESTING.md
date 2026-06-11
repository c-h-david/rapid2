# Testing

> If wanting to rebuild from scratch:
>
> ```bash
> rm -r ~/venv/
> /usr/bin/python3 -m venv ~/venv
> pip install .[dev]
> ```

## Stating code analysis

We leverage a variety of static code analysis tools as a means of checking and
enforcing some consistency in our code base.

### Markdown linter

We use `pymarkdown` to lint our markdown files.

```bash
pymarkdown scan *.md
```

> We enforce a maximum line width of 79 characters using the
> [`.pymarkdown.yml`][URL_CFG_MD]
> configuration file.

### Yaml linter

We use `yamllint` to lint our yaml files.

```bash
yamllint .*.yml .github/*/*.yml
```

> We enforce a maximum line width of 79 characters using the
> [`.yamllint.yml`][URL_CFG_YM]
> configuration file.

### Dockerfile linter

We use `hadolint` to lint our Dockerfiles.

```bash
hadolint --ignore DL3008 --ignore SC2046 Dockerfile
```

> We also enforce a maximum line width of 79 characters using `awk` because
> `hadolint` does not allow to enforce a maximum line width.

```bash
awk 'length>79 {print FILENAME ":"FNR">79"; exit 1}' Dockerfile
```

### Bash linter

We use `shellcheck` to lint our bash scripts.

```bash
shellcheck *.sh tst/*.sh
```

> We also enforce a maximum line width of 79 characters.

```bash
awk 'length>79 {print FILENAME ":"FNR">79"; exit 1}' *.sh tst/*.sh
```

### Python linter and formatter

We use `ruff` to lint our python files.

```bash
ruff check .
```

We also use `ruff` to check the formatting of our python files.

```bash
ruff format . --check
```

> We enforce a maximum line width of 79 characters, version 3.11 of python,
> as well as standard options for linting and formatting using the
> [`pyproj.toml`][URL_CFG_PY]
> configuration file.

### Python type checker

We use `mypy` to check dynamic and static typing.

```bash
mypy .
```

> We enforce strict typing and python version 3.11 using the
> [`pyproj.toml`][URL_CFG_PY]
> configuration file.

## Runtime testing

RAPID comes along with a set of test files based on a synthetic experiment
described in
[`SANDBOX.md`][URL_SNDBOX].
on which our runtime testing efforts rely.

### Python docstrings check

We use the `doctest` module to check examples in docstrings.

```bash
python3 -m doctest src/rapid2/core/*.py
```

### Replication of past results

```bash
rapid2 -nml input/Sandbox/nml_Sandbox.yml
```

```bash
cmpncf \
  -prv output/Sandbox/Qou_Sandbox_19700101_19700110.nc4 \
  -now output/Sandbox/Qou_Sandbox_19700101_19700110_tst.nc4
```

```bash
cmpncf \
  -prv output/Sandbox/Qfi_Sandbox_19700101_19700110.nc4 \
  -now output/Sandbox/Qfi_Sandbox_19700101_19700110_tst.nc4
```

[URL_SNDBOX]: https://github.com/c-h-david/rapid2/blob/main/SANDBOX.md
[URL_CFG_MD]: https://github.com/c-h-david/rapid2/blob/main/.pymarkdown.yml
[URL_CFG_YM]: https://github.com/c-h-david/rapid2/blob/main/.yamllint.yml
[URL_CFG_PY]: https://github.com/c-h-david/rapid2/blob/main/pyproj.toml
