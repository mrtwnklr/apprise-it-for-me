ARG ARCH
FROM ${ARCH}python:3.8.6-alpine as base

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
RUN pip install pipenv

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

HEALTHCHECK --interval=60s --timeout=3s --retries=6 CMD wget --no-verbose --tries=1 --spider http://localhost:${FLASK_RUN_PORT}/health || exit 1

ENV FLASK_RUN_PORT=8001
ENV FLASK_APP=manage.py
EXPOSE ${FLASK_RUN_PORT}/tcp

# Install application into container
COPY . /apprise-it-for-me

CMD ["flask", "run", "-h", "0.0.0.0"]
