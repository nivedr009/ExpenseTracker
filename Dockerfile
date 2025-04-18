# Use official Python image
FROM python:3.13-slim

# Install system dependencies for selenium and Chrome WebDriver
RUN apt-get update \
    && apt-get install -y \
    wget \
    curl \
    unzip \
    libpq-dev gcc \
    libgtk-3-0 libdbus-1-3 libxtst6 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libnss3 libxss1 libgdk-pixbuf2.0-0 \
    && pip install --upgrade pip

# Create a directory for Chrome installation and change permissions
RUN mkdir -p /tmp/chrome-install \
    && cd /tmp/chrome-install

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    || apt-get install -f -y \
    && rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Copy chromedriver from your local machine to Docker container
COPY drivers/chromedriver.exe /usr/local/bin/chromedriver

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files into the Docker container
COPY . .

# Expose default Django port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
