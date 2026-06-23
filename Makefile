# ==============================================================================
#                             Opsie Automation Interface
# ==============================================================================

init:
	@echo "🎯 Initializing local python development environments..."
	pip install -r requirements-dev.txt
	pre-commit install

up:
	@echo "🚀 Provisioning service mesh topology and compiling modified layers..."
	docker compose up -d --build

down:
	@echo "🛑 Demolishing active container infrastructure and pruning volumes..."
	docker compose down -v --remove-orphans

restart:
	@echo "🔄 Executing sequential sequence teardown and immediate deployment..."
	@$(MAKE) down
	@$(MAKE) up

logs:
	@echo "📋 Attaching to unified standard output log streams..."
	docker compose logs -f
