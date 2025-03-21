# Use the official Python 3.12 image as the base image
FROM python:3.12

# Force Python to send output directly to the terminal (stdout/stderr) without buffering
ENV PYTHONUNBUFFERED=1

# Install tzdata for timezone configuration
RUN apt-get update && \
    apt-get install -y tzdata

# Set the timezone to EST (use a region like America/New_York that observes EST)
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Poetry, a dependency management tool for Python
RUN pip install poetry

# Configure Poetry to install dependencies globally
RUN poetry config virtualenvs.create false

# Copy the dependency files (pyproject.toml and poetry.lock) to the container
COPY ./pyproject.toml ./poetry.lock ./

# Synchronize the lock file with the pyproject.toml without updating dependencies
# --no-update: Ensures the poetry.lock matches pyproject.toml without upgrading versions

# Install dependencies from the lock file
# --no-ansi: Disables colored output
# --no-interaction: Skips any interactive prompts
# --no-root: Does not install the current project as a dependency
RUN poetry lock --no-update && \
    poetry install --no-ansi --no-interaction --no-root

# Update the package list
RUN apt-get update 
