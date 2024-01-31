# Test the service
docker run -p 5000:5000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/book bchewy/book:1.0

# Airplay issue, if port 5000 in use
# https://stackoverflow.com/questions/69955686/why-cant-i-run-the-project-on-port-5000