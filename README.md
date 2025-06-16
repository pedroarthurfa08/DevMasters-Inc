# DevMasters API

API REST desenvolvida com FastAPI para gerenciamento de projetos.

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd DevMasters-Inc
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando a API

Para iniciar a API em modo de desenvolvimento:

```bash
python run.py
```

A API estará disponível em:
- http://localhost:8000
- Documentação Swagger UI: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

## Endpoints

### Projetos

- `GET /projects` - Lista todos os projetos
  - Suporta filtros por status e prioridade
  - Suporta paginação (skip e limit)
  - Suporta ordenação (order_by e order_direction)

- `POST /projects` - Cria um novo projeto
  - Campos obrigatórios: título, prioridade, status
  - Campos opcionais: descrição

- `GET /projects/{project_id}` - Retorna detalhes de um projeto

- `PUT /projects/{project_id}` - Atualiza um projeto
  - Atualização parcial permitida
  - Não permite alterar id nem data_criacao

- `DELETE /projects/{project_id}` - Remove um projeto

## Validações

- Título: 3-100 caracteres, único
- Descrição: máximo 500 caracteres
- Prioridade: 1, 2 ou 3
- Status: "Planejado", "Em Andamento", "Concluído", "Cancelado"

## Desenvolvimento

Para contribuir com o projeto:

1. Crie uma branch para sua feature
2. Faça suas alterações
3. Envie um pull request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
