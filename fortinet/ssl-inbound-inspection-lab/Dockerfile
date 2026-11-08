# Use the official Nginx image as a base
FROM nginx:alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom configuration file to Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Copy your SSL files to the container
COPY ca_keys/ca.pem /etc/ssl/certs/
COPY web.crt /etc/ssl/certs/
COPY web.key /etc/ssl/private/

# Copy your website files to the container
COPY index.html /usr/share/nginx/html
