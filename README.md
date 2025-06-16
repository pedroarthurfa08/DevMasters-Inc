# DevMasters API

API REST desenvolvida com FastAPI para gerenciamento de projetos.

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

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

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
