# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /WTFScript
COPY requirements-flask.txt /WTFScript


RUN apk add --no-cache \
    bash \
    curl \
    docker-cli \
    docker-compose \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements-flask.txt
    
COPY . /WTFScript

ENTRYPOINT ["python3", "-u", "previewer.py"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

