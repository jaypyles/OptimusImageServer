build:
	docker build -t optimusmediaserver .

up:
	docker run -d -p 8000:8000 --name oms optimusmediaserver

destroy:
	docker stop oms
	docker rm oms

.PHONY: build up destroy
