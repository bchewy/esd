# Running the RabbitMQ container
docker run -d --hostname esd-rabbit --name rabbitmq-mgmt -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Start/Stop
docker stop rabbitmq-mgmt
docker start rabbitmq-mgmt