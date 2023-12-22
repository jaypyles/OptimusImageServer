export DOPPLER_TOKEN=$(shell doppler configs tokens create dev --plain --max-age=900s)

reup: destroy build up

destroy:
	doppler run -- docker stop oms
	doppler run -- docker rm oms

build:
	doppler run -- docker-compose build

up:
	doppler run -- docker-compose -f docker-compose.yml up -d



.PHONY: build up destroy reup
