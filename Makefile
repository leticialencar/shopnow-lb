ALGORITHM ?= round_robin
export ALGORITHM

.PHONY: help up down restart status logs test benchmark benchmark-nginx servers request request-nginx algorithm round-robin least-connections random stop-server-1 start-server-1 stop-server-2 start-server-2 stop-server-3 start-server-3 nginx-test

help:
	@echo "ShopNow Load Balancer - Comandos disponíveis:"
	@echo "  make up                  Iniciar todos os serviços"
	@echo "  make down                Parar todos os serviços"
	@echo "  make restart             Reiniciar todos os serviços"
	@echo "  make status              Ver status dos containers"
	@echo "  make servers             Iniciar os 3 servidores"
	@echo "  make logs                Ver logs do balanceador"
	@echo "  make request             Enviar requisição ao balanceador Python"
	@echo "  make request-nginx       Enviar requisição ao Nginx"
	@echo "  make algorithm            Mostrar algoritmo configurado"
	@echo "  make round-robin         Usar Round Robin"
	@echo "  make least-connections   Usar Least Connections"
	@echo "  make random              Usar Random"
	@echo "  make test                Executar testes unitários"
	@echo "  make benchmark           Benchmark do balanceador Python"
	@echo "  make benchmark-nginx     Benchmark do Nginx"
	@echo "  make stop-server-1       Parar servidor 1"
	@echo "  make start-server-1      Iniciar servidor 1"
	@echo "  make stop-server-2       Parar servidor 2"
	@echo "  make start-server-2      Iniciar servidor 2"
	@echo "  make stop-server-3       Parar servidor 3"
	@echo "  make start-server-3      Iniciar servidor 3"
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

servers:
	docker compose up -d server1 server2 server3

logs:
	docker compose logs -f load-balancer

request:
	powershell -Command "Invoke-RestMethod http://localhost:8000/"

request-nginx:
	powershell -Command "Invoke-RestMethod http://localhost:8001/"

algorithm:
	@echo "Algoritmo configurado: $(ALGORITHM)"

round-robin:
	docker compose stop load-balancer
	$(MAKE) up ALGORITHM=round_robin

least-connections:
	docker compose stop load-balancer
	$(MAKE) up ALGORITHM=least_connections

random:
	docker compose stop load-balancer
	$(MAKE) up ALGORITHM=random

test:
	python -m unittest discover -s tests -v

benchmark:
	docker run --rm alpine:3.20 sh -c "apk add --no-cache apache2-utils && ab -n 1000 -c 50 http://host.docker.internal:8000/"

benchmark-nginx:
	docker run --rm alpine:3.20 sh -c "apk add --no-cache apache2-utils && ab -n 1000 -c 50 http://host.docker.internal:8001/"

stop-server-1:
	docker compose stop server1

start-server-1:
	docker compose start server1

stop-server-2:
	docker compose stop server2

start-server-2:
	docker compose start server2

stop-server-3:
	docker compose stop server3

start-server-3:
	docker compose start server3

nginx-test:
	docker compose exec nginx nginx -t
