# Use the official Python 3.12 image as the base image
FROM python:3.12

# Force Python to send output directly to the terminal without buffering
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y tzdata plantuml && \
    rm -rf /var/lib/apt/lists/*

# Set the timezone to EST (America/New_York)
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# Install uv for dependency management
RUN pip install uv

# Copy and install dev tools to system
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt
