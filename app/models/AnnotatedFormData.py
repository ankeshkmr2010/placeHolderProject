from typing import List

from pydantic import BaseModel
from starlette.datastructures import FormData

from app.models.FormData import ComponentVisualRepr, ComponentPopulation, Timestamps, TaxFormData, TaxFormSection, \
    TaxFormField


class AnnotatedData(BaseModel):
    Value : str = None
    Label : str = None
    IsEditable : bool = False
    IsHighlighted : bool = False
    IsVisible : bool = True
    PopulationValidation: ComponentPopulation = None
    GridData: ComponentVisualRepr
    TimestampData: Timestamps

    def call_populate_depth_first(self, data: dict = None):
        """
        Recursively calls the populate method on the annotated data.
        :param data: The data to populate.
        """
        if self.PopulationValidation and self.PopulationValidation.ShouldPopulate:
            self.Value = self.PopulationValidation.PopulationFunction.populate(data)


class AnnotatedFormFieldData(TaxFormField):
    Annotations: List[AnnotatedData] = []

    def call_populate_depth_first(self, data: dict = None):
        """
        Recursively calls the populate method on the field and its annotations.
        :param data: The data to populate.
        """
        print(f">> population  validation: {self.PopulationValidation}")
        if self.PopulationValidation and self.PopulationValidation.ShouldPopulate:
            self.FieldValue = self.PopulationValidation.PopulationFunction.populate(data)

        for annotation in self.Annotations:
            if annotation.PopulationValidation and annotation.PopulationValidation.ShouldPopulate:
                annotation.Value = annotation.PopulationValidation.PopulationFunction.populate(data)

class AnnotatedTaxSectionData(TaxFormSection):
    FormFields: List[AnnotatedFormFieldData] = []
    Annotations: List[AnnotatedData] = []

    def call_populate_depth_first(self, data: dict = None):
        """
        Recursively calls the populate method on all fields and annotations in the section.
        :param data: The data to populate.
        """
        for field in self.FormFields:
            field.call_populate_depth_first(data)

        for annotation in self.Annotations:
            annotation.call_populate_depth_first(data)

class AnnotatedTaxFormData(TaxFormData):
    Sections: List[AnnotatedTaxSectionData] = []
    Annotations: List[AnnotatedData] = []

    def call_populate_depth_first(self, data: dict = None):
        """
        Recursively calls the populate method on all sections and annotations in the form data.
        :param data: The data to populate.
        """
        for section in self.Sections:
            section.call_populate_depth_first(data)

        for annotation in self.Annotations:
            annotation.call_populate_depth_first(data)

