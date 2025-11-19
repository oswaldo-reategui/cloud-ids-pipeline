
# Base image: Python 3.10 slim for minimal footprint
FROM python:3.10-slim

# All subsequent commands run from /app
WORKDIR /app

# Copy requirements and install Redis client library
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the log-shipping Python script into the image
COPY zeek_to_redis.py ./

# Default command: run the Python shipper
ENTRYPOINT ["python", "zeek_to_redis.py"]
