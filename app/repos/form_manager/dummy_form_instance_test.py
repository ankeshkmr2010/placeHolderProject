import json
from app.models.AnnotatedFormData import AnnotatedTaxFormData, AnnotatedTaxSectionData, AnnotatedFormFieldData
from app.models.FormData import ComponentVisualRepr, Timestamps, ComponentPopulation, TaxFormData, TaxFormField, \
    TaxFormSection
from app.repos.field_population.field_populator import FNameFieldPopulateRepo, LNameFieldPopulateRepo, EmailFieldPopulateRepo, PhoneFieldPopulateRepo, DefaultDummyFieldPopulateRepo



def generate_dummy_form_instance() -> TaxFormData:
    # Common timestamp and grid data for simplicity
    timestamp = Timestamps(CreatedDate="2024-06-01", LastModifiedDate="2024-06-01", LastModifiedBy="user123")

    # Helper to build grid with coordinates
    def build_grid(row: int) -> ComponentVisualRepr:
        return ComponentVisualRepr(
            GridId="G1",
            GridLabel="Grid 1",
            IsHighlighted=False,
            IsEditable=True,
            GridTopLeft=f"{row},0",
            GridBottomRight=f"{row},1",
            GridHDivisions=1,
            GridVDivisions=1,
            TimestampData=timestamp
        )

    # Populators
    fname_pop = FNameFieldPopulateRepo()
    lname_pop = LNameFieldPopulateRepo()
    email_pop = EmailFieldPopulateRepo()
    phone_pop = PhoneFieldPopulateRepo()
    dummy_pop = DefaultDummyFieldPopulateRepo()

    # Fields with unique grid positions
    fname_field = TaxFormField(
        FieldId="FIELD_FNAME",
        FieldLabel="First Name",
        FieldValue="",
        FieldType="text",
        PopulationValidation=ComponentPopulation(PopulationFunction=fname_pop),
        GridData=build_grid(0),
        TimestampData=timestamp
    )

    lname_field = TaxFormField(
        FieldId="FIELD_LNAME",
        FieldLabel="Last Name",
        FieldValue="",
        FieldType="text",
        PopulationValidation=ComponentPopulation(PopulationFunction=lname_pop),
        GridData=build_grid(1),
        TimestampData=timestamp
    )

    email_field = TaxFormField(
        FieldId="FIELD_EMAIL",
        FieldLabel="Email",
        FieldValue="",
        FieldType="email",
        PopulationValidation=ComponentPopulation(PopulationFunction=email_pop),
        GridData=build_grid(2),
        TimestampData=timestamp
    )

    phone_field = TaxFormField(
        FieldId="FIELD_PHONE",
        FieldLabel="Phone",
        FieldValue="",
        FieldType="phone",
        PopulationValidation=ComponentPopulation(PopulationFunction=phone_pop),
        GridData=build_grid(3),
        TimestampData=timestamp
    )

    dummy_field = TaxFormField(
        FieldId="FIELD_DUMMY",
        FieldLabel="Dummy",
        FieldValue="",
        FieldType="text",
        PopulationValidation=ComponentPopulation(PopulationFunction=dummy_pop),
        GridData=build_grid(4),
        TimestampData=timestamp
    )

    # Sections
    personal_section = TaxFormSection(
        SectionId="SEC_PERSONAL",
        SectionLabel="Personal Info",
        SectionType="info",
        FormFields=[fname_field, lname_field, email_field, phone_field],
        GridData=build_grid(0),  # doesn't matter for section-level layout in frontend
        TimestampData=timestamp
    )

    other_section = TaxFormSection(
        SectionId="SEC_OTHER",
        SectionLabel="Other Info",
        SectionType="misc",
        FormFields=[dummy_field],
        GridData=build_grid(5),
        TimestampData=timestamp
    )

    # Form
    dummy_form = TaxFormData(
        FormId="FORM001",
        FormLabel="Dummy Tax Form",
        FormVersion="1.0",
        FormType="TAX",
        Sections=[personal_section, other_section],
        GridData=build_grid(0),
        TimestampData=timestamp
    )

    print("Form populated successfully.")
    return dummy_form



if __name__ == "__main__":
    # Generate and print the dummy form instance
    dummy_form_instance = generate_dummy_form_instance()
    print("Dummy Form Instance Created:")
    print(json.dumps(dummy_form_instance.model_dump(), indent=2, ensure_ascii=False))