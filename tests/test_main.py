"""Testes de exemplo"""
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    """Testa a rota raiz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Testa o health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_read_items():
    """Testa leitura de itens"""
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
