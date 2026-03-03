"""Endpoints de exemplo"""
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
async def read_items():
    """Lista todos os itens"""
    return [{"name": "Item 1"}, {"name": "Item 2"}]


@router.get("/{item_id}")
async def read_item(item_id: int):
    """Obtém um item específico"""
    return {"item_id": item_id, "name": f"Item {item_id}"}
