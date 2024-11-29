# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install Poetry
RUN pip install poetry

# Install the dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Create a non-root user
RUN useradd --create-home --shell /bin/bash working_task

# Switch to the non-root user
USER working_task

# Run the worker
CMD ["celery", "-A", "metadata_extraction_worker.tasks", "worker", "--loglevel=info"]
