FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry export --format=requirements.txt --output=requirements.txt --without-hashes \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/{apt,dpkg,cache,log}
    
COPY ui .
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["python", "-m", "streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]