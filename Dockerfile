# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/weather.py .
COPY src/discord_bot.py .
COPY src/main.py .
COPY src/scheduler.py .

# Create a non-root user for security
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Run the scheduler by default
CMD ["python", "scheduler.py", "--no-test"]

