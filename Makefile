build:
	docker build -t optimusmediaserver .

up:
	docker run -d --name oms optimusmediaserver

destroy:
	docker stop oms
	docker rm oms

.PHONY: build up destroy
