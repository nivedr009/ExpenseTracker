# Use official Python image
FROM python:3.13-slim

# Install system dependencies for selenium and Edge WebDriver
RUN apt-get update \
    && apt-get install -y \
    wget \
    curl \
    unzip \
    libpq-dev gcc \
    libgtk-3-0 libdbus-1-3 libxtst6 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    && pip install --upgrade pip

# Download and install Microsoft Edge WebDriver
RUN wget https://msedgedriver.azureedge.net/113.0.1774.50/edgedriver_linux64.zip \
    && unzip edgedriver_linux64.zip -d /usr/local/bin/ \
    && rm edgedriver_linux64.zip

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
