from fastapi import APIRouter

from app.models.FormData import TaxFormData
from app.repos.form_manager.dummy_form_instance_test import generate_dummy_form_instance
from app.repos.form_manager.annotated_form_example import generate_dummy_annotated_form

ir = APIRouter()

@ir.get("/getFormJson", summary="Instead Demo", description="Returns a dummy form instance for testing purposes.")
async def instead_demo()-> TaxFormData:
    return generate_dummy_form_instance()

@ir.get("/getFormAnnotatedJson", summary="Instead Demo ", description="Returns a dummy annotated form instance for testing purposes.")
async def instead_demo_annotated()-> TaxFormData:
    return generate_dummy_annotated_form()