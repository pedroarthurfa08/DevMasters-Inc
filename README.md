# DevMasters API

API RESTful desenvolvida com Python, FastAPI e Pydantic.

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
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando a API

Para iniciar o servidor de desenvolvimento:

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Documentação

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estrutura do Projeto

```
DevMasters-Inc/
├── app/
│   ├── config/
│   │   └── settings.py
│   ├── models/
│   │   └── base.py
│   └── routes/
├── main.py
└── requirements.txt
```
