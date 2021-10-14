VERSION := "v0.3.0"

########################################

ENV := ${ENVIRONMENT}

ifeq (${ENV}, devl)
        TROHOME := /Users/jeff/devl/troload
endif

ifeq (${ENV}, test)
        TROHOME := /Users/jeff/test/troload
endif

ifeq (${ENV}, prod)
        TROHOME := /home/jeff/prod/troload
endif

########################################

# echo-env:
# 	@echo "Environment = ${ENVIRONMENT}"
# 	@echo "TROHOME = ${TROHOME}"

# ########################################

# build:
# 	docker-compose --file=${DCYAML} build

# build-full:
# 	docker-compose --file=${DCYAML} build --pull --no-cache

# run:
# 	docker-compose --file=${DCYAML} run \
# 	--detach \
# 	--name troload \
# 	--volume ${HOME}/${ENVIRONMENT}/troload/local/log:/home/container/troload/local/log \
# 	--volume ${HOME}/${ENVIRONMENT}/troload/local/rpt:/home/container/troload/local/rpt \
# 	--volume ${HOME}/${ENVIRONMENT}/troload/local/stage:/home/container/troload/local/stage \
# 	troload \
# 	--environment=${ENV}

# ps:
# 	docker-compose --file=${DCYAML} ps -a 

# logs:
# 	docker logs troload 

# exec:
# 	docker-compose --file=${DCYAML} exec troload /bin/bash

# stop:
# 	docker-compose --file=${DCYAML} stop troload

# rm:
# 	docker-compose --file=${DCYAML} rm -fv troload


# ########################################

# connect-db:
# 	psql -h localhost -p 5432 -d ${ENV} -U postgres

# cluster-status:
# 	@echo "\nNetworks\n"
# 	@docker network ls -f name=tro*
# 	@echo "\nVolumes\n"
# 	@docker volume ls -f name=tro*
#
# run-load:
# 	local/bin/runmypy.sh ${TRO_LOCAL}/python/troload.py -e devl >${TRO_LOCAL}/log/troload.log 2>&1
#

# run-old:
# 	docker run \
# 	--detach \
# 	--name troload \
# 	troload_troload \
# 	--environment ${ENV} 
# 	docker ps -a
