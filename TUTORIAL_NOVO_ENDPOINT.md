"""
GUIA: Como Criar um Novo Endpoint

Este arquivo demonstra como adicionar um novo recurso (por exemplo, Users)
à sua API seguindo a arquitetura do projeto.
"""

# ============================================================================
# PASSO 1: Criar o Schema (Validação de Dados)
# Arquivo: app/schemas/user.py
# ============================================================================

"""
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Para converter modelo ORM
"""


# ============================================================================
# PASSO 2: Criar o Modelo (Banco de Dados)
# Arquivo: app/models/user.py
# ============================================================================

"""
from sqlalchemy import Column, Integer, String
from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
"""


# ============================================================================
# PASSO 3: Criar o Serviço (Lógica de Negócio)
# Arquivo: app/services/user_service.py
# ============================================================================

"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        # Aqui vai a lógica de criação, hash de senha, etc.
        db_user = User(name=user.name, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
"""


# ============================================================================
# PASSO 4: Criar o Endpoint (Rota)
# Arquivo: app/api/v1/endpoints/users.py
# ============================================================================

"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.database.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    '''Cria um novo usuário'''
    return UserService.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    '''Obtém um usuário específico'''
    db_user = UserService.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user


@router.get("/", response_model=list[User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''Lista todos os usuários'''
    return UserService.get_all_users(db=db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    '''Atualiza um usuário'''
    db_user = UserService.update_user(db=db, user_id=user_id, user_update=user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    '''Deleta um usuário'''
    success = UserService.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}
"""


# ============================================================================
# PASSO 5: Registrar o Endpoint no main.py
# ============================================================================

"""
# Em main.py, adicione:
from app.api.v1.endpoints import users

# E depois inclua a rota:
app.include_router(users.router, prefix="/api/v1")
"""


# ============================================================================
# PASSO 6: Criar Testes
# Arquivo: tests/test_users.py
# ============================================================================

"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={"name": "John Doe", "email": "john@example.com", "password": "secret"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "john@example.com"


def test_read_user():
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200


def test_list_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
"""


# ============================================================================
# RESUMO: Passos para Adicionar um Novo Recurso
# ============================================================================

"""
1. ✅ Criar Schema (Validação)
   - app/schemas/[recurso].py
   - Define Create, Read, Update models com Pydantic

2. ✅ Criar Modelo (Banco de Dados)
   - app/models/[recurso].py
   - Define a tabela com SQLAlchemy

3. ✅ Criar Serviço (Lógica)
   - app/services/[recurso]_service.py
   - Implementa CRUD e lógica de negócio

4. ✅ Criar Endpoint (Rota)
   - app/api/v1/endpoints/[recurso].py
   - Define GET, POST, PUT, DELETE

5. ✅ Registrar Rota
   - Adicionar import e include_router em main.py

6. ✅ Escrever Testes
   - tests/test_[recurso].py
   - Testar cada endpoint

7. ✅ Executar
   - python main.py
   - Acessar http://localhost:8000/docs
"""
