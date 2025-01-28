IMAGE_NAME = sentiment-analysis-api
CONTAINER_NAME = sentiment-analysis-container
PORT = 80

build:
	docker build -t $(IMAGE_NAME) .

rebuild:
	docker build --no-cache -t $(IMAGE_NAME) .

start:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):80 $(IMAGE_NAME)

remove:
	docker rm $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)

clean:
	docker rmi $(IMAGE_NAME)

bash:
	docker exec -it $(CONTAINER_NAME) /bin/bash

ps:
	docker ps -a


test-local:
	PYTHONPATH=. pytest tests/