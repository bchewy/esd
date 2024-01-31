# Build images, and run the corresponding containers with the images; run in the background -- change to docker run -it to run in the foreground
docker build -t activity:latest activity/. && docker run -d --name activity activity:latest
docker build -t book:latest book/. && docker run -d --name book book:latest
docker build -t order:latest order/. && docker run -d --name order order:latest
docker build -t shipping:latest shipping/. && docker run -d --name shipping shipping:latest
docker build -t error:latest error/. && docker run -d --name error error:latest
docker build -t orchestrator:latest orchestrator/. && docker run -d --name orchestrator orchestrator:latest
