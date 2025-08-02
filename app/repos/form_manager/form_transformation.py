import json

from app.models.AnnotatedFormData import AnnotatedTaxFormData
from app.models.FormData import ComponentPopulation
from app.repos.field_population.field_populator import DefaultDummyFieldPopulateRepo
from app.repos.form_manager import test_json


class TransformationRepo:
    @staticmethod
    def transform_form_data(incoming_json:str|dict) -> AnnotatedTaxFormData:
        """
        Transforms incoming JSON data into an AnnotatedTaxFormData object.

        Args:
            incoming_json (dict): The incoming JSON data to be transformed.

        Returns:
            AnnotatedTaxFormData: The transformed data as an AnnotatedTaxFormData object.
        """
        if isinstance(incoming_json, str):
            data = json.loads(incoming_json)
        else:
            data = incoming_json

        return AnnotatedTaxFormData(**data)

    @staticmethod
    def add_population_function(
        form_data: AnnotatedTaxFormData
    ) -> AnnotatedTaxFormData:
        """
        Adds a population function to the form data.

        Args:
            form_data (AnnotatedTaxFormData): The form data to which the population function will be added.
            population_function (str): The name of the population function to add.

        Returns:
            AnnotatedTaxFormData: The updated form data with the population function added.
        """
        if not form_data.PopulationValidation:
            form_data.PopulationValidation = ComponentPopulation(
                ShouldPopulate=True,
                PopulationFunction=DefaultDummyFieldPopulateRepo()
            )
            for annotation in form_data.Annotations:
                if not annotation.PopulationValidation:
                    annotation.PopulationValidation = ComponentPopulation(
                        ShouldPopulate=True,
                        PopulationFunction=DefaultDummyFieldPopulateRepo()
                    )


        for section in form_data.Sections:
            if not section.PopulationValidation:
                section.PopulationValidation = ComponentPopulation(
                    ShouldPopulate=True,
                    PopulationFunction=DefaultDummyFieldPopulateRepo()
                )
            for annotation in section.Annotations:
                if not annotation.PopulationValidation:
                    annotation.PopulationValidation = ComponentPopulation(
                        ShouldPopulate=True,
                        PopulationFunction=DefaultDummyFieldPopulateRepo()
                    )

            for field in section.FormFields:
                if not field.PopulationValidation:
                    field.PopulationValidation = ComponentPopulation(
                        ShouldPopulate=True,
                        PopulationFunction=DefaultDummyFieldPopulateRepo()
                    )
                for annotation in field.Annotations:
                    if not annotation.PopulationValidation:
                        annotation.PopulationValidation = ComponentPopulation(
                            ShouldPopulate=True,
                            PopulationFunction=DefaultDummyFieldPopulateRepo()
                        )
        return form_data



if __name__ == "__main__":
    # Example usage
    transformed_data = TransformationRepo.transform_form_data(test_json)
    transformed_data = TransformationRepo.add_population_function(transformed_data)
    # Call populate method to fill in the data
    transformed_data.call_populate_depth_first()

    print(transformed_data)
    print(json.dumps(transformed_data.model_dump(), indent=2, ensure_ascii=False))