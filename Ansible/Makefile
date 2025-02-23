#
.SILENT:
#

#==========================================================================================

.PHONY: yaml-lint
yaml-lint:
	printf "\n\n   Performing yaml linting on ${PLAYBOOK} ...\n"
	yamllint ${PLAYBOOK}; \
	if [ $$? -eq 0 ]; \
	then \
		printf "   yaml linting successful!\n"; \
	fi

#==========================================================================================

.PHONY: syntax-check
syntax-check:
	printf "\n\n   Performing syntax check...\n"
	ansible-playbook --syntax-check ${PLAYBOOK} --extra-vars "HOSTS=${HOSTS}"
	if [ $$? -eq 0 ]; \
	then \
		printf "   syntax check successful!\n"; \
	fi

#==========================================================================================

.PHONY: ansible-lint
ansible-lint:
	printf "\n\n   Performing ansible linting...\n"
	/opt/homebrew/bin/ansible-lint ${PLAYBOOK}
	if [ $$? -eq 0 ]; \
	then \
		printf "   ansible linting successful!\n"; \
	fi

#==========================================================================================

#  PLAYBOOK = './playbooks/TROLoadTrans.yaml'

verify-troloadtrans: yaml-lint syntax-check ansible-lint

run-troloadtrans: 
	ansible-playbook --ask-become-pass ${PLAYBOOK}

#==========================================================================================

verify: yaml-lint syntax-check ansible-lint

run: 
	ansible-playbook --ask-become-pass ${PLAYBOOK}


