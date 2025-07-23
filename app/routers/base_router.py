from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_items():
    return [{"id": 1, "name": "Foo"}, {"id": 2, "name": "Bar"}]