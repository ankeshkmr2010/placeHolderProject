from fastapi import APIRouter, Body

from app.repos.sensitive_data_checker.deps import get_sensitive_data_checker

ub_demo = APIRouter()


@ub_demo.get("/unbound")
async def unbound_demo():
    """
    Unbound demo endpoint.
    This is a placeholder for an unbound demo functionality.
    """
    return {"message": "This is an unbound demo endpoint."}


@ub_demo.post("/unbound/process_data")
async def process_data(data: str = Body(...)):
    dc = get_sensitive_data_checker()
    fd = await dc.check(data)
    return {"processed_data": fd}