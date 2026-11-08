# Use the official Ubuntu base image
FROM ubuntu:latest

# Update the package repository and install OpenSSL
RUN apt-get update && \
    apt-get install -y openssl && \
    rm -rf /var/lib/apt/lists/*

# Define a volume to mount a directory from the host
VOLUME ["/home/parrot007/fortinet_labs/ssl_cert"]

# Set the working directory to the mounted volume
WORKDIR /data

# By default, run a shell. Users can override this command as needed
CMD ["/bin/bash"]
