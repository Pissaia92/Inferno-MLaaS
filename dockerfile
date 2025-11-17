# Stage 1: The "Builder"

FROM python:3.11-slim as builder

WORKDIR /app

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.in-project true

# Copy only the dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --only main

# Stage 2: The "Production" Image

FROM python:3.11-slim

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv ./.venv

# Copy the application code and the model
COPY api/ ./api/
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]