# Use the official Python slim image
FROM python:3.12

# Install system dependencies
RUN apt update && apt install -y \
    wget \
    unzip \
    curl \
    chromium-driver \
    chromium \
    libnss3 \
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
RUN pip install uv
RUN uv sync

# Default command to run the bot
CMD ["uv", "run", "random_chess"]
