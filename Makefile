run: build
	docker run -it -v $$(pwd):/app my_python_image /bin/bash

build:
	docker build -t my_python_image .


fclean:
	@printf "Complete clearning of all docker configuration ... \n"
	@docker stop $$(docker ps -qa);\
	docker system prune -a ;\
	docker system prune --all --force --volumes;\
	docker network prune --force;\
	docker volume rm  token-volume