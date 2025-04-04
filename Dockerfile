# Use a lightweight Nginx base image
FROM nginx:alpine

# Set the working directory (Nginx serves files from /usr/share/nginx/html)
WORKDIR /usr/share/nginx/html

# Copy all your static files (HTML, CSS, JS) to the Nginx web directory
COPY . .

# Expose port 80 (default HTTP port for Nginx)
EXPOSE 80

# Nginx starts automatically when the container runs
