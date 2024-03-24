export DOPPLER_TOKEN=$(shell doppler configs tokens create dev --plain --max-age=900s)
export COMPOSE_YMLS=$(shell doppler secrets get COMPOSE_YMLS --plain)

reup: destroy build up

destroy:
	doppler run -- docker stop oms
	doppler run -- docker rm oms

build:
	doppler run -- docker-compose ${COMPOSE_YMLS} build

up:
	doppler run -- docker-compose ${COMPOSE_YMLS} up -d



.PHONY: build up destroy reup
