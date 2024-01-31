# Use the official MySQL image as the base image
FROM mysql:latest

# Set the root password for the MySQL server
ENV MYSQL_ROOT_PASSWORD=root

# Copy the order.sql file to the /docker-entrypoint-initdb.d directory
COPY order.sql /docker-entrypoint-initdb.d/
COPY book.sql /docker-entrypoint-initdb.d/

# Expose the default MySQL port
EXPOSE 3306
