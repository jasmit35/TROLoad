########################################

ENV := ${ENVIRONMENT}

ifeq (${ENV}, devl)
        TROHOME := /Users/jeff/devl/TROLoad
endif

ifeq (${ENV}, test)
        TROHOME := /Users/jeff/test/TROLoad
endif

ifeq (${ENV}, prod)
        TROHOME := /home/jeff/prod/TROLoad
endif

########################################

categories_table_unit_tests:
	-rm logs/tests.categories_table_unit_tests.log
	python -m unittest tests.categories_table_unit_tests

csv_processor_unit_tests:
	-rm logs/tests.csv_processor_unit_tests.log
	-rm stage/categories.csv.bkp
	python -m unittest tests.csv_processor_unit_tests

unit-tests: categories_table_unit_tests csv_processor_unit_tests


functional-tests:
	-rm stage/*.bkp
	-rm stage/*.csv
	-rm logs/*
	-rm reports/*
	python -m unittest tests.functional_tests

