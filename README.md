# Mars Probe API

API REST para controle de sondas exploradoras em um planalto retangular em Marte.

## Contexto

Uma sonda é lançada em um planalto 2D compartilhado. O ponto de pouso é sempre a origem `(0, 0)`. Os limites do planalto são definidos no momento do primeiro lançamento pelas coordenadas superiores direitas `(x, y)`. A sonda recebe comandos de movimento e rotação e nunca pode ultrapassar os limites da malha.

## Stack

- **Python 3.12**
- **FastAPI** — framework HTTP
- **Pydantic v2** — validação e schemas
- **Jinja2** — template do mapa visual
- **Pytest** — testes unitários e de integração
- **Docker / Docker Compose**

## Estrutura do projeto

```
app/
├── controllers/     # Camada HTTP — rotas FastAPI
├── services/        # Regras de negócio
├── repositories/    # Persistência em memória
├── models/          # Entidades de domínio e enums
├── schemas/         # DTOs Pydantic (request / response)
├── exceptions/      # Exceções de domínio
├── templates/       # Template HTML do mapa visual
└── core/            # Config, DI e seeder
tests/
├── unit/            # Testes de service e repository
└── integration/     # Testes dos endpoints via TestClient
```

## Executando localmente

**Pré-requisitos:** Python 3.12+ e `pip`.

```bash
# 1. Crie e ative um ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Suba o servidor
uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000`.

## Executando com Docker

```bash
# Build + start
docker compose up --build

# Apenas start (após o primeiro build)
docker compose up
```

## Documentação interativa

| Interface | URL |
|-----------|-----|
| Mapa visual | `http://localhost:8000/` |
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |

## Rodando os testes

```bash
pytest
```

Para relatório de cobertura:

```bash
pytest --cov=app --cov-report=html
```

## Endpoints

### `POST /probes`

Lança uma sonda e configura o planalto compartilhado. A sonda sempre inicia em `(0, 0)`.

> `x` e `y` definem as coordenadas superiores direitas do planalto (ex: `5, 5` cria uma malha de 6×6).

```json
// Request
{ "x": 5, "y": 5, "direction": "NORTH" }

// Response 201
{ "id": "uuid", "x": 0, "y": 0, "direction": "NORTH" }
```

### `POST /probes/{id}/commands`

Envia uma sequência de comandos para a sonda. Sequências com caracteres inválidos são rejeitadas integralmente antes de qualquer execução.

| Comando | Ação |
|---------|------|
| `M` | Avança uma posição na direção atual |
| `L` | Gira 90° à esquerda |
| `R` | Gira 90° à direita |

```json
// Request
{ "commands": "MMRMM" }

// Response 200
{ "id": "uuid", "x": 2, "y": 2, "direction": "EAST" }
```

### `GET /probes`

Retorna todas as sondas e suas posições atuais.

### `GET /probes/{id}`

Retorna a posição atual de uma sonda específica.

### `DELETE /probes/{id}`

Remove uma sonda. Retorna `204 No Content`.

### `GET /health`

Health check da aplicação.

## Regras de negócio

- Sondas iniciam sempre em `(0, 0)`
- O planalto é compartilhado entre todas as sondas e configurado no lançamento
- Comandos inválidos (`X`, `Z`, etc.) são rejeitados **antes** de qualquer execução — `422`
- Movimentos fora dos limites do planalto retornam `422`
- Sondas não encontradas retornam `404`
