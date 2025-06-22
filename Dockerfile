# Use Python image
FROM python:3.10-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set path
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY . /tests
WORKDIR /tests

# Run tests
CMD ["python", "selenium_tests.py"]
