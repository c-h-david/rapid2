# Testing

## Stating code analysis

We leverage a variety of static code analysis tools as a means of checking and
enforcing some consistency in our code base.

### Markdown linter

We use `pymarkdown` to lint our markdown files.

```bash
pymarkdown scan *.md
```

> The maximum line width is 80 characters by default.

### Yaml linter

We use `yamllint` to lint our yaml files.

```bash
yamllint .github/workflows/*.yml
```

> The maximum line width is 80 characters by default.

### Dockerfile linter

We use `hadolint` to lint our Dockerfiles.

```bash
hadolint --ignore DL3008 Dockerfile
```

> `hadolint` does not enforce a maximum line width.

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
