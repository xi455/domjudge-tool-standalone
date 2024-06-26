ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION} as base

RUN pip install poetry

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock

RUN poetry export --format=requirements.txt --output=requirements.txt --without-hashes \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# App
FROM python:${PYTHON_VERSION}-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      libpq-dev \
      cron \
      libxml2 \
      && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=base /usr/local/lib/ /usr/local/lib/
COPY --from=base /usr/local/bin/ /usr/local/bin/

EXPOSE 8000

COPY ./docker /docker
COPY /docker/standalone-logrotate /etc/cron.d/standalone-logrotate
Run crontab /etc/cron.d/standalone-logrotate

RUN \
  mv -v /docker/entrypoint.sh /usr/local/bin/entrypoint && \
  chmod +x /usr/local/bin/entrypoint && \
  \
  mv -v /docker/standalone.logrotate.conf /etc/logrotate.d/standalone && \
  chmod 644 /etc/logrotate.d/standalone && \
  \
  rm -rvf /docker

COPY ./ui .

CMD [ "entrypoint" ]
