# Base image: minimal Debian for compatibility and small footprint
FROM debian:bookworm-slim

# Install tcpreplay (packet replay tool) and clean up apt cache to reduce image size
RUN apt-get update \
    && apt-get install -y tcpreplay \
    && rm -rf /var/lib/apt/lists/*    

# Use tcpreplay as the default entrypoint so
# the container’s command args are passed directly to tcpreplay
ENTRYPOINT ["tcpreplay"]
