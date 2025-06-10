#
.SILENT:
#
#==========================================================================================

.PHONY: yaml-lint
yaml-lint:
	printf "\n🚀    Performing yaml linting on ${PLAYBOOK}...\n"
	yamllint ${PLAYBOOK}; \
	if [ $$? -eq 0 ]; \
	then \
		printf "      yaml linting successful!\n"; \
	fi

#==========================================================================================

.PHONY: syntax-check
syntax-check:
	printf "\n🚀    Performing syntax check on ${PLAYBOOK}...\n"
	ansible-playbook --syntax-check ${PLAYBOOK} --extra-vars "HOSTS=${HOSTS}" 
	if [ $$? -eq 0 ]; \
	then \
		printf "      syntax check successful!\n"; \
	fi

#==========================================================================================

.PHONY: ansible-lint
ansible-lint:
	printf "\n🚀    Performing ansible linting...\n"
	/opt/homebrew/bin/ansible-lint ${PLAYBOOK}
	if [ $$? -eq 0 ]; \
	then \
		printf "      ansible linting successful!\n"; \
	fi

#------------------------------------------------------------------------------------------

check: yaml-lint syntax-check ansible-lint

run-in-test:
	ansible-playbook -i inventory/hosts_test_swarm --ask-become-pass ${PLAYBOOK}

run-in-prod:
	ansible-playbook -i inventory/hosts_prod_swarm --ask-become-pass ${PLAYBOOK}


