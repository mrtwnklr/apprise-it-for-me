ARG ARCH
FROM ${ARCH}python:3.11.2-alpine as base

LABEL org.opencontainers.image.authors="Marty Winkler"

# Setup env
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

# --------------------------------------------------

FROM base AS python-deps

# Install pipenv
RUN pip install pipenv==2023.2.18

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# --------------------------------------------------

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN addgroup -S apprise-it-for-me && adduser -S apprise-it-for-me -G apprise-it-for-me
WORKDIR /apprise-it-for-me
USER apprise-it-for-me

HEALTHCHECK --interval=60s --timeout=3s --retries=6 CMD wget --no-verbose --tries=1 --spider http://localhost:${GUNICORN_PORT}/health || exit 1

ENV GUNICORN_PORT=8001
ENV WSGI_APP=manage:app
EXPOSE ${GUNICORN_PORT}/tcp

# Install application into container
COPY . /apprise-it-for-me

CMD ["sh", "-c", "gunicorn -c application/gunicorn.conf.py -b :${GUNICORN_PORT} --worker-tmp-dir /dev/shm \"${WSGI_APP}\""]
