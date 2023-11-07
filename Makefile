build:
	docker-compose build

up:
	docker-compose -f docker-compose.yml --env-file .env up -d

destroy:
	docker stop oms
	docker rm oms

reup:
	docker stop oms
	docker rm oms
	docker-compose build
	docker-compose -f docker-compose.yml --env-file .env up -d

.PHONY: build up destroy reup
