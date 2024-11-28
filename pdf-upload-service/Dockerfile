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

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "pdf_upload_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
