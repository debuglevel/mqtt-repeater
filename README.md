# Python Microservice Template

Python microservice template, inspired by my Kotlin based microservice
template https://github.com/debuglevel/greeting-microservice, but with way less enthusiasm; and I'm not too sure that
too much works here, because I just copied a bunch of stuff from my various other projects to have them at one place at
least.

## Development environment

* Python environment
    * Python 3.8
    * venv
* Code quality
    * Formatting
        * black
    * Type annotations
        * mypy
    * Testing
        * pytest
        * tox
* REST
    * FastAPI
* Deployment
    * Docker
    * docker-compose
* IDE
    * PyCharm Community

### TODO

* Logging that does not completely suck
    * would nice to be configurable via ENV
* Testing?
    * tox (which seems to test against different Python versions. WTF compatibility? But it does not install those
      environments/python versions!)
* linting?
* Formatting?

## Development

### Environment

#### Initialize virtual environment (using venv)

```sh
python3 -m venv venv
```

#### Activate virtual environment

```sh
source ./venv/Scripts/activate
```

```powershell
.\venv\Scripts\Activate.ps1
```

### Dependencies

#### Install dependencies

```sh
pip install -r requirements-dev.txt
```

#### Dependency updates

`pip list --outdated` shows outdated (transitive) dependencies.

#### Formatting / Linting

##### black

`black` is used for formatting, because `black` does not ask about your opinion about how Python code should be formatted.

```bash
black .
```

##### mypy

mypy checks the type annotations:

```sh
mypy app tests
```

### Testing

#### Run tests

```sh
pytest
```

#### Run tests on every file change

```sh
pytest-watch -c # -c clears terminal before pytest runs
```

#### Run test against different environments

```sh
tox
```

### Documentation

#### OpenAPI documentation

* Open [Swagger UI](http://localhost:8000/docs) or [ReDoc](http://localhost:8000/redoc)
* OpenAPI specs are available (as JSON) at http://localhost:8080/openapi.json 
* Update `openapi.json` via `python update-openapi.py`

### All-in-one
`tox.ini` is also configured to run some additional commands (like a Makefile):
* `black .` for formatting
* `python update-openapi.py` to update `openapi.yaml`
* `pytest` for testing

### Deployment

#### Development (with auto reloading changed files)

```sh
uvicorn app.rest.main:fastapi --port=8080 --reload --log-config=app/logging-config.yaml
```

#### Production

This should be quite okay:

```sh
uvicorn app.rest.main:fastapi --port=8080 --log-config=app/logging-config.yaml
```

But some docs mention that `gunicorn` can be used as a manager.

#### Production (via docker compose)

```sh
docker compose up --build
```


