# Use the official Python slim image
FROM python:3.11-slim

# Install system dependencies
RUN apt update && apt install -y \
    wget \
    unzip \
    curl \
    chromium-driver \
    chromium \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/usr/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port if necessary (e.g., Flask UI)
EXPOSE 8000

# Default command to run the bot
CMD ["python", "src/random_chess_2.0/main.py"]
