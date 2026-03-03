# Estrutura de Pastas - Documentação

## 📁 Estrutura do Projeto

```
API_Drive/
├── main.py                      # Ponto de entrada da aplicação
├── requirements.txt             # Dependências Python
├── .env.example                 # Variáveis de ambiente (exemplo)
├── .gitignore                   # Arquivos ignorados pelo Git
├── README.md                    # Documentação principal
│
├── app/                         # Pacote principal da aplicação
│   ├── __init__.py             # Inicializador do pacote
│   │
│   ├── api/                    # Rotas e endpoints da API
│   │   ├── __init__.py
│   │   └── v1/                 # Versão 1 da API
│   │       ├── __init__.py
│   │       └── endpoints/      # Endpoints específicos
│   │           ├── __init__.py
│   │           ├── items.py    # Endpoints de exemplo (CRUD)
│   │           └── drive.py    # Endpoints do Google Drive
│   │
│   ├── core/                   # Configurações centrais
│   │   ├── __init__.py
│   │   ├── config.py           # Configurações da aplicação (Settings)
│   │   └── security.py         # Autenticação e segurança
│   │
│   ├── models/                 # Modelos de banco de dados
│   │   └── __init__.py         # Modelos SQLAlchemy aqui
│   │
│   ├── schemas/                # Schemas Pydantic (DTOs)
│   │   └── __init__.py         # Schemas de validação aqui
│   │
│   ├── services/               # Lógica de negócio
│   │   └── __init__.py         # Serviços e regras de negócio aqui
│   │
│   └── database/               # Configuração do banco de dados
│       ├── __init__.py
│       └── database.py         # Conexão e sessão com SQLAlchemy
│
└── tests/                      # Testes automatizados
    ├── __init__.py
    └── test_main.py            # Testes da API
```

## 📝 Descrição dos Diretórios

### `app/`
Contém toda a lógica da aplicação FastAPI, organizada em camadas:

### `app/api/`
- Agrupa todos os endpoints da API
- `v1/` permite versionamento futuro (v2, v3, etc.)
- `endpoints/` contém os controladores (routes)

### `app/core/`
- Configurações globais da aplicação
- `config.py` - Variáveis de ambiente e settings
- `security.py` - Autenticação, JWT, verificação de tokens

### `app/models/`
- Define os modelos de banco de dados
- Usa SQLAlchemy ORM
- Exemplo: User, Item, Project, etc.

### `app/schemas/`
- Define esquemas Pydantic para validação
- Request/Response models
- Separado dos models para manter a arquitetura limpa

### `app/services/`
- Contém a lógica de negócio
- Operações complexas, validações, cálculos
- Mantém endpoints simples e limpos

### `app/database/`
- Configuração do banco de dados
- Factory de sessões
- Conexão e migrações

### `tests/`
- Testes unitários e de integração
- Pytest para automação
- TestClient para testes de API

## 🚀 Como Usar

### 1. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Editar .env com suas configurações
```

### 2. Ativar ambiente virtual
```bash
.venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação
```bash
python main.py
```
A API estará em: `http://localhost:8000`

### 5. Acessar documentação interativa
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 6. Rodar testes
```bash
pytest
```

## 📦 Dependências

| Pacote | Uso |
|--------|-----|
| **fastapi** | Framework web moderno |
| **uvicorn** | Servidor ASGI |
| **pydantic** | Validação de dados |
| **pydantic-settings** | Configurações com variáveis de ambiente |
| **sqlalchemy** | ORM para banco de dados |
| **python-multipart** | Suporte para upload de arquivos |
| **google-api-python-client** | Cliente da Google API |
| **google-auth** | Autenticação Google |
| **pytest** | Framework de testes |
| **httpx** | Client HTTP para testes |

## 🔄 Fluxo de Desenvolvimento

1. **Criar um novo endpoint**
   - Adicionar route em `app/api/v1/endpoints/`
   - Criar schema em `app/schemas/`
   - Criar serviço em `app/services/`

2. **Adicionar modelo de banco**
   - Definir modelo em `app/models/`
   - Importar em `app/database/database.py`

3. **Implementar lógica**
   - Endpoint chama serviço
   - Serviço usa modelo e banco de dados
   - Retorna schema validado

4. **Testar**
   - Escrever testes em `tests/`
   - Executar com pytest

## 🔐 Segurança

- Variáveis sensíveis em `.env` (não commitare no Git)
- CORS configurado em `main.py`
- Autenticação centralizada em `app/core/security.py`

## 📚 Referências

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Google Drive API](https://developers.google.com/drive/api)
