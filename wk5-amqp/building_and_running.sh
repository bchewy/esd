# Run and build all our different microservices
docker build -t activity:wk5 activity_log/. && docker run -d --name activity activity:wk5
docker build -t error:wk5 error/. && docker run -d --name error error:wk5
docker build -t shipping:wk5 shipping/. && docker run -d --name shipping shipping:wk5
docker build -t placeorder:wk5 place_order/. && docker run -p 5100:5100 -d --name placeorder placeorder:wk5

# Run the rabbitMQ service
docker run -d --hostname esd-rabbit --name rabbitmq-mgmt -p 5672:5672 -p 15672:15672 rabbitmq:3-management
