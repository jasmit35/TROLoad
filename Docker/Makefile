.PHONY: dr-build
dr-build: clean-build ## Build wheel file
	@echo "🚀 Building docker image"
	@docker image build -t example/troload:latest .
	docker scout quickview

.PHONY: dr-run 
dr-run: ##  Run the container
	@echo "🚀 Running container: Running Docker container"
	@docker container run --rm -it example/troload:latest
