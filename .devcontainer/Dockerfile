# Use Ubuntu 24.04 as the base image.
FROM ubuntu:24.04

# Disable interactive prompts during package installation.
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install required packages.
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    clang \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the default command to bash.
CMD [ "bash" ]
