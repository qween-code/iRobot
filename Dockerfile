# LastWarAutoBot Pro - Docker Image
# Multi-stage build for optimized image size

# ==========================================
# Stage 1: Builder
# ==========================================
FROM python:3.12-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ==========================================
# Stage 2: Runtime
# ==========================================
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # ADB and Android tools
    android-tools-adb \
    # OpenCV dependencies
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    # Tesseract OCR
    tesseract-ocr \
    tesseract-ocr-eng \
    # Utilities
    curl \
    wget \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create app user (non-root for security)
RUN useradd -m -u 1000 botuser && \
    mkdir -p /app /data /logs /models && \
    chown -R botuser:botuser /app /data /logs /models

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=botuser:botuser . .

# Switch to non-root user
USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Expose ports
EXPOSE 5000 5001

# Volume mounts
VOLUME ["/data", "/logs", "/models"]

# Entry point
ENTRYPOINT ["python", "src/main.py"]

# Default command
CMD ["--config", "configs/default.yaml"]
