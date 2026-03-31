DEV_COMPOSE_FILE := docker-compose.yml

# Construir la imagen
build:
	docker compose -f $(DEV_COMPOSE_FILE) build

# Levantar los contenedores
up:
	docker compose -f $(DEV_COMPOSE_FILE) up

# Levantar en segundo plano
up-d:
	docker compose -f $(DEV_COMPOSE_FILE) up -d

# Detener contenedores
down:
	docker compose -f $(DEV_COMPOSE_FILE) down

# Ver logs
logs:
	docker compose -f $(DEV_COMPOSE_FILE) logs -f

# Ejecutar comandos dentro del contenedor
shell:
	docker compose -f $(DEV_COMPOSE_FILE) exec web bash

# Reiniciar contenedores
restart:
	docker compose -f $(DEV_COMPOSE_FILE) restart

# Ver estado
ps:
	docker compose -f $(DEV_COMPOSE_FILE) ps

# Limpiar todo (volúmenes incluidos)
clean:
	docker compose -f $(DEV_COMPOSE_FILE) down -v
