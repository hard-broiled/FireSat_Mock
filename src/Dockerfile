# Very simple dockerfile to start: using poetry for dependency management, and pytest execution
# src/Dockerfile
FROM python:alpine as base

# Set environment vars
ENV POETRY_VERSION=1.7.1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

# Set workdir
WORKDIR /app

# Copy project files
COPY ../pyproject.toml ../poetry.lock* ./
RUN poetry install --no-root

# Copy code
COPY ../src/ .

CMD ["poetry", "run", "pytest"]
