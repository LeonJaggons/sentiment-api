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
	
bash-ci:
	docker exec $(CONTAINER_NAME) /bin/bash

ps:
	docker ps -a

start-venv:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Run the following command to activate the virtual environment:"
	@echo "source venv/bin/activate"

test: start-venv
	. venv/bin/activate && PYTHONPATH=. pytest


run-local: start-venv
	. venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 0
    