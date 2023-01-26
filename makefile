build:
	docker compose -f local.yml up --build -d --remove-orphans

single_build:
	docker build -t fin-24 .

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down