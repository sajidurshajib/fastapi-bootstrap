FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/src


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    make \
    libffi-dev \
    g++ \
    git \
    bash \
    zip \
    openssl \
    openssh-client \
    curl \
    libcurl4-openssl-dev \
    libpcre3-dev \
    libpq5 \
    libpq-dev \
    python3-dev \
    postgresql-client \
    libjpeg-dev \
    zlib1g-dev \
    wget \
    default-libmysqlclient-dev \
    mariadb-client && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip psycopg2 pandas requests


# Set the working directory
WORKDIR /src

# Install Project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code
COPY mount/ .

# scripts
COPY mount/scripts /scripts
RUN chmod u+x /scripts/*.sh

RUN sed -i 's/\r$//g' /scripts/start.sh
RUN sed -i 's/\r$//g' /scripts/migrate-db.sh
# Expose the FastAPI port
EXPOSE 80

# Command to run the FastAPI application
CMD ["/scripts/start.sh"]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
