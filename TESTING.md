# Testing

## Stating code analysis

We leverage a variety of static code analysis tools as a means of checking and
enforcing some consistency in our code base.

### Markdown linter

We use `pymarkdown` to lint our markdown files.

```bash
pymarkdown scan *.md
```

> We enforce a maximum line width of 79 characters using the `.pymarkdown.yml`
> configuration file.

### Yaml linter

We use `yamllint` to lint our yaml files.

```bash
yamllint .github/workflows/*.yml .*.yml
```

> We enforce a maximum line width of 79 characters using the `.yamllint.yml`
> configuration file.

### Dockerfile linter

We use `hadolint` to lint our Dockerfiles.

```bash
hadolint --ignore DL3008 --ignore SC2046 Dockerfile
```

> `hadolint` does not allow to enforce a maximum line width, but we try to keep
> it at 79 for consistency

### Python linter

We use `flake8` to lint our python files.

```bash
flake8 src/*.py
```

> The maximum line width is 79 characters by default.

### Python type checker

We use `mypy` to dynamic typing and static typing.

```bash
mypy --strict src/*.py
```
