from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel
from abc import ABC, abstractmethod


class ValidationFunction(BaseModel,ABC):
    inputData: dict
    validationParameters: dict
    isValid: bool = False

    @abstractmethod
    def validate(self, data) -> bool:
        """
        Validate the provided data.
        :param data: The data to validate.
        :return: True if valid, False otherwise.
        """
        pass

class PopulationFunction(BaseModel,ABC):
    inputData: Optional[dict] = {}
    populationParameters: Optional[dict] = {}
    result: str = None

    @abstractmethod
    def populate(self, data=None) -> str:
        """
        Populate the provided data.
        :param data: The data to populate.
        :return: The populated data.
        """
        pass

class ComponentStatusEnum(str, Enum):
    Draft = "Draft"
    Submitted = "Submitted"
    Approved = "Approved"
    Rejected = "Rejected"

class Timestamps(BaseModel):
    CreatedDate: str
    LastModifiedDate: str
    LastModifiedBy: str

class ComponentPopulation(BaseModel):
    DataType: str = "input"
    ShouldValidate: bool = False
    ShouldPopulate: bool = True
    ValidationFunction: Optional[ValidationFunction] = None  # noqa: pydantic-field-serializer
    PopulationFunction: Optional[PopulationFunction]  # noqa: pydantic-field-serializer

class ComponentVisualRepr(BaseModel):
    GridId: str
    GridLabel: str
    IsHighlighted: bool
    IsEditable: bool
    GridTopLeft: str
    GridBottomRight: str
    GridHDivisions: int
    GridVDivisions: int
    TimestampData: Timestamps

class TaxFormCoreComponent(BaseModel):
    PopulationValidation: Optional[ComponentPopulation] = None
    GridData: ComponentVisualRepr
    TimestampData: Timestamps
    ComponentStatus: ComponentStatusEnum = ComponentStatusEnum.Draft


class TaxFormField( TaxFormCoreComponent):
    FieldId: str
    FieldLabel: str
    FieldValue: str
    FieldType: str

    def call_populate_depth_first(self, data: dict = None):
        """
        Recursively calls the populate method on the field.
        :param data: The data to populate.
        """
        if self.PopulationValidation and self.PopulationValidation.ShouldPopulate:
            self.FieldValue = self.PopulationValidation.PopulationFunction.populate(data)


class TaxFormSection( TaxFormCoreComponent):
    SectionId: str
    SectionLabel: str
    SectionType: str
    FormFields: list[TaxFormField] = []

    def call_populate_depth_first(self, data: dict = None):
        """
        Recursively calls the populate method on all fields in the section.
        :param data: The data to populate.
        """
        for field in self.FormFields:
            field.call_populate_depth_first(data)

class TaxFormData( TaxFormCoreComponent):
    FormId: str
    FormLabel: str
    FormVersion: str
    FormType: str
    Sections: list[TaxFormSection] = []

    def call_populate_depth_first(self, data: dict = None):
        """
        Recursively calls the populate method on all components in the form data.
        :param data: The data to populate.
        """

        for section in self.Sections:
            section.call_populate_depth_first(data)



