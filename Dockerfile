ARG PYTHON_VERSION=3.9.6
ARG ALPINE_VERSION=3.14

## Final image
#FROM python:$PYTHON_VERSION-slim-buster
FROM python:$PYTHON_VERSION-alpine$ALPINE_VERSION as runtime

ENV PYTHONUNBUFFERED 1

# add a group and an user with specified IDs
RUN addgroup -S -g 1111 appgroup && adduser -S -G appgroup -u 1111 appuser
#RUN groupadd -r -g 1111 appgroup && useradd -r -g appgroup -u 1111 --no-log-init appuser # if based on Debian/Ubuntu

# add curl for health check
RUN apk add --no-cache curl
#RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* # if based on Debian/Ubuntu

# add /data directory with correct rights
RUN mkdir /data && chown 1111:1111 /data

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
# /app/app looks ugly, but preserves the "app" module folder
COPY app/ /app/app/

# switch to unprivileged user for following commands
USER appuser

## set the default port to 8080
#ENV MICRONAUT_SERVER_PORT 8080
EXPOSE 8080

## use a log appender with no timestamps as Docker logs the timestamp itself ("docker logs -t ID")
#ENV LOG_APPENDER classic-stdout

HEALTHCHECK --interval=5m --timeout=5s --retries=3 --start-period=1m CMD curl --fail http://localhost/health || exit 1

CMD ["uvicorn", "--host=0.0.0.0", "app.rest.main:fastapi", "--port=8080", "--log-config=app/logging-config.yaml"]

###############
# COPY venv /app/venv
# COPY requirements.txt .
# RUN venv/bin/activate && pip3 install -r requirements.txt
# CMD venv/bin/activate && cd base && flask run --host=0.0.0.0 --port=80

# # NOTE: We do not use the python:3.x-alpine image because it lacks the corresponding python-dev package.
# #       But python-dev cannot be installed via apk as it might not be available in the corresponding version (or things get installed in the wrong way anyway).
# #       Therefore we set up python ourselves.
#
# # TODO: actually it just might not be a good idea to use a alpine image for Python, because wheels cannot be used
#
# # Download and compile (where necessary) python dependencies in a venv in this stage
# FROM alpine:3.12 as builder
#
# WORKDIR /install
#
# ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# ENV PIP_NO_CACHE_DIR 1
# ENV PYTHONUNBUFFERED 1
#
# # CairoSVG (and maybe other python dependencies) need to compile stuff during their installation. pip cannot download wheels from PyPi as alpine uses musl instead of glibc
# RUN apk add --no-cache python3 python3-dev cmd:pip3 gcc make musl-dev cairo-dev pango-dev gdk-pixbuf libffi-dev zlib-dev jpeg-dev
#
# RUN python3 -m venv /venv
# # Activate venv
# ENV PATH="/venv/bin:$PATH"
#
# # `pip3 install -r requirements.txt` breaks otherwise.
# RUN pip3 install wheel
#
# COPY requirements.txt .
# RUN pip3 install -r requirements.txt
#
#
# # Copy the venv from the builder stage
# FROM alpine:3.12
#
# # Add python and some necessary runtime dependencies
# RUN apk add --no-cache python3 libjpeg cairo
# # Copy the pythen dependencies with compiled stuff
# COPY --from=builder /venv /venv
#
# WORKDIR /app
# COPY . /app
#
# # Activate venv
# ENV PATH="/venv/bin:$PATH"
###########
# USER python
#CMD ["gunicorn", "--workers", "8", "--log-level", "INFO", "--bind", "0.0.0.0:5000", "manage:app"]
###########
