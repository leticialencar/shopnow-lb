
.PHONY: help up down restart status logs test benchmark stop-server-2 start-server-2

ALGORITHM ?= round_robin
export ALGORITHM

help:
	@echo "ShopNow Load Balancer - Comandos disponíveis:"
	@echo "  make up                  Iniciar os serviços"
	@echo "  make down                Parar os serviços"
	@echo "  make restart             Reiniciar os serviços"
	@echo "  make status              Ver status dos containers"
	@echo "  make logs                Ver logs do balanceador"
	@echo "  make test                Executar testes unitários"
	@echo "  make benchmark           Executar teste de carga"
	@echo "  make stop-server-2       Simular falha do servidor 5002"
	@echo "  make start-server-2      Recuperar servidor 5002"

up:
	docker compose up --build -d

down:
	docker compose down

restart:
	docker compose down
	docker compose up --build -d

status:
	docker compose ps

logs:
	docker compose logs -f balanceador

test:
	python -m unittest discover -s tests -v

benchmark:
	docker compose --profile test run --rm ab

stop-server-2:
	docker compose stop servidor2

start-server-2:
	docker compose start servidor2