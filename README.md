# API Drive - FastAPI

Estrutura de projeto para uma API usando FastAPI.

## Estrutura do Projeto

```
API_Drive/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── .env.example           # Variáveis de ambiente (exemplo)
├── .gitignore             # Arquivos ignorados pelo git
│
├── app/                    # Aplicação FastAPI
│   ├── __init__.py
│   ├── api/               # Rotas da API
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── items.py
│   ├── core/              # Configurações principais
│   │   ├── __init__.py
│   │   ├── config.py      # Settings da app
│   │   └── security.py    # Segurança e autenticação
│   ├── models/            # Modelos do banco de dados
│   │   └── __init__.py
│   ├── schemas/           # Schemas Pydantic
│   │   └── __init__.py
│   ├── services/          # Lógica de negócio
│   │   └── __init__.py
│   └── database/          # Configuração do banco
│       ├── __init__.py
│       └── database.py
│
└── tests/                 # Testes
    ├── __init__.py
    └── test_main.py
```

## Como Usar

### 1. Ativar o ambiente virtual
```bash
.venv\\Scripts\\activate
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar a aplicação
```bash
python main.py
```

A API estará disponível em: `http://localhost:8000`

### 4. Acessar a documentação interativa
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependências

- **fastapi**: Framework web moderno
- **uvicorn**: Servidor ASGI
- **python-multipart**: Suporte para multipart/form-data
- **google-api-python-client**: Cliente da Google API
- **google-auth**: Autenticação Google

## Próximos Passos

1. Criar arquivos `.env` baseado em `.env.example`
2. Adicionar modelos no diretório `models/`
3. Implementar schemas Pydantic em `schemas/`
4. Desenvolver serviços em `services/`
5. Criar endpoints adicionais em `endpoints/`
6. Escrever testes em `tests/`
