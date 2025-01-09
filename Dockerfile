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

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]