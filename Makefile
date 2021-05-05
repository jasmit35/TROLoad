#
ENV := devl
# ENV := test
# ENV := prod

TRO_LOCAL := /Users/jeff/${ENV}/TROLoad/local

exec-db:
	docker exec -it tro_db_1 /bin/bash
#
connect-db:
	psql -h localhost -p 5432 -d tro -U postgres
#
cluster-build:
	docker-compose build 
#
cluster-up:
	docker-compose up -d
#
cluster-status:
	@echo "\nNetworks\n"
	@docker network ls -f name=tro*
	@echo "\nVolumes\n"
	@docker volume ls -f name=tro*
#
cluster-down:
	@cd /Users/jeff/devl/TRO
	docker-compose down 
#
run-load:
	local/bin/runmypy.sh ${TRO_LOCAL}/python/troload.py -e devl >${TRO_LOCAL}/log/troload.log 2>&1
#
doc-build:
	docker build . --tag jasmit/troload:latest 
#