[![release](https://img.shields.io/github/release/raffclar/llm_works.svg)](https://github.com/raffclar/llm_works/releases/latest)
[![tests](https://github.com/raffclar/llm_works/actions/workflows/check-format-and-lint.yaml/badge.svg)](https://github.com/raffclar/llm_works/actions/workflows/check-format-and-lint.yaml)
[![codecov](https://codecov.io/gh/raffclar/llm_works/branch/main/graph/badge.svg?token=2L7QM6R6RH)](https://codecov.io/gh/raffclar/llm_works)
# ZanV2 / LLM Works

## Requirements
1. Python >=3.9
2. Poetry

## Install the dependencies
```
poetry install --with dev --no-root
```

## Run the tests
```
poetry run python manage.py test
```

## Code coverage for tests
```
poetry run coverage run manage.py test
```
