
VERSION := "v0.2.1"

########################################

ENV := "${ENVIRONMENT}"

ifeq (${ENV}, "devl")
        TROHOME := "/Users/jeff/devl/troload"
endif

ifeq (${ENV}, "test")
        TROHOME := "/Users/jeff/test/troload"
endif

ifeq (${ENV}, "prod")
        TROHOME := "/home/jeff/prod/troload"
endif

DCYAML := "${TROHOME}/docker-compose.yaml"

########################################

echo-env:
	@echo "Environment = ${ENVIRONMENT}"
	@echo "TROHOME = ${TROHOME}"

########################################

build:
	docker-compose --file=${DCYAML} build

build-full:
	docker-compose --file=${DCYAML} build --pull --no-cache

run:
	docker-compose --file=${DCYAML} up -d
	docker-compose --file=${DCYAML} ps

ps:
	docker-compose --file=${DCYAML} ps

logs:
	docker-compose --file=${DCYAML} logs load 

exec_db:
	docker exec -it troload_database_1 /bin/bash

exec_app:
	docker exec -it troload_application_1 /bin/bash

stop:
	docker-compose --file=${DCYAML} stop application 
	docker-compose --file=${DCYAML} stop database 

rm:
	docker-compose --file=${DCYAML} rm -fsv load 


########################################

connect-db:
	psql -h localhost -p 5432 -d tro -U postgres

cluster-status:
	@echo "\nNetworks\n"
	@docker network ls -f name=tro*
	@echo "\nVolumes\n"
	@docker volume ls -f name=tro*
#
# run-load:
# 	local/bin/runmypy.sh ${TRO_LOCAL}/python/troload.py -e devl >${TRO_LOCAL}/log/troload.log 2>&1
#
