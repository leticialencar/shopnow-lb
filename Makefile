
ALGORITHM ?= round_robin
export ALGORITHM

.PHONY: help up down restart status logs test benchmark benchmark-nginx stop-server-2 start-server-2 nginx-test

help:
	@echo "ShopNow Load Balancer - Comandos disponíveis:"
	@echo "  make up                  Iniciar os serviços"
	@echo "  make down                Parar os serviços"
	@echo "  make restart             Reiniciar os serviços"
	@echo "  make status              Ver status dos containers"
	@echo "  make logs                Ver logs do balanceador"
	@echo "  make test                Executar testes unitários"
	@echo "  make benchmark           Executar benchmark do balanceador Python"
	@echo "  make benchmark-nginx     Executar benchmark do Nginx"
	@echo "  make stop-server-2       Simular falha do servidor 5002"
	@echo "  make start-server-2      Recuperar servidor 5002"
	@echo "  make nginx-test          Validar configuração do Nginx"

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
	docker compose logs -f load-balancer

test:
	python -m unittest discover -s tests -v

benchmark:
	docker run --rm alpine:3.20 sh -c "apk add --no-cache apache2-utils && ab -n 1000 -c 50 http://host.docker.internal:8000/"

benchmark-nginx:
	docker run --rm alpine:3.20 sh -c "apk add --no-cache apache2-utils && ab -n 1000 -c 50 http://host.docker.internal:8001/"

stop-server-2:
	docker compose stop server2

start-server-2:
	docker compose start server2

nginx-test:
	docker compose exec nginx nginx -t
