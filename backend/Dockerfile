FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# Need to add Chrome and Chrom Driver for selenium to work
RUN apt-get update && apt-get install -y \
    postgresql-client \
    git \
    wget \
    gnupg2 \
    unzip \ 
    curl \
    chromium \
    chromium-driver \
    python3-lxml \
    libxml2-dev \
    libxslt-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set permissions for ChromeDriver
RUN chmod +x /usr/bin/chromedriver

# Expose the port the app runs on
EXPOSE 8000

# Use the startup script as the entry point
CMD ["./start.sh"]
