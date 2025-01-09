FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
ARG ENV={ENV}
COPY requirements.txt dev_requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN if [ "$ENV" = "development" ] ; then pip install --no-cache-dir -r dev_requirements.txt ; fi

# Copy application code
COPY . .

# Fix line endings and permissions for entrypoint
RUN sed -i 's/\r$//g' entrypoint.sh && \
    chmod +x entrypoint.sh

# Run with uvicorn
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]