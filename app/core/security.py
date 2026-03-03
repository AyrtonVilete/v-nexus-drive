"""Módulo de segurança da aplicação"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()


async def verify_token(credentials = Depends(security)):
    """Verifica o token de autenticação"""
    if credentials.credentials == "test-token":
        return credentials.credentials
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido"
    )
