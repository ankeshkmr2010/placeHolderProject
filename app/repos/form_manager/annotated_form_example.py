from typing import List

from app.models.AnnotatedFormData import AnnotatedFormFieldData, AnnotatedTaxSectionData, AnnotatedTaxFormData, \
    AnnotatedData
from app.models.FormData import Timestamps, ComponentVisualRepr, ComponentPopulation, PopulationFunction


def generate_dummy_annotated_form() -> AnnotatedTaxFormData:
    timestamp = Timestamps(
        CreatedDate="2024-06-01",
        LastModifiedDate="2024-06-01",
        LastModifiedBy="user123"
    )

    # Helper to build grid at (row, col)
    def build_grid(row: int, col: int = 0) -> ComponentVisualRepr:
        return ComponentVisualRepr(
            GridId="G1",
            GridLabel="Grid 1",
            IsHighlighted=False,
            IsEditable=True,
            GridTopLeft=f"{row},{col}",
            GridBottomRight=f"{1+row},{1.8*col}",
            GridHDivisions=1,
            GridVDivisions=1,
            TimestampData=timestamp
        )

    # Fake repos that just return a string
    class DummyPopRepo(PopulationFunction):

        def __init__(self, data:str):
            super().__init__()
            self.result = data


        def populate(self, data:dict=None)-> str:
            return self.result

    # Prepare populate functions
    repos = {
        "First Name": DummyPopRepo({"key":"First Name"}),
        "Last Name":  DummyPopRepo({"key":"Last Name"}),
        "Email":      DummyPopRepo({"key":"Email"}),
        "Phone":      DummyPopRepo({"key":"Phone"}),
        "Dummy":      DummyPopRepo({"key":"Dummy"}),
    }

    # Field definitions (original five)
    field_defs = [
        ("FIELD_FNAME", "First Name", "text"),
        ("FIELD_LNAME", "Last Name",  "text"),
        ("FIELD_EMAIL", "Email",      "email"),
        ("FIELD_PHONE", "Phone",      "phone"),
        ("FIELD_DUMMY", "Dummy",      "text"),
    ]

    annotated_fields: List[AnnotatedFormFieldData] = []

    for idx, (fid, label, ftype) in enumerate(field_defs):
        # field at row = idx*2, annotation row= idx*2+1
        row_field = idx * 2
        row_ann   = row_field + 1

        # Base field
        field = AnnotatedFormFieldData(
            FieldId=fid,
            FieldLabel=label,
            FieldValue="",  # will be populated
            FieldType=ftype,
            PopulationValidation=ComponentPopulation(PopulationFunction=repos[label]),
            GridData=build_grid(row_field, 0),
            TimestampData=timestamp
        )

        # Annotation below the field
        ann = AnnotatedData(
            Value="",
            Label=f"{label} Annotation",
            IsEditable=False,
            IsHighlighted=True,
            IsVisible=True,
            PopulationValidation=ComponentPopulation(PopulationFunction=DummyPopRepo(f"ANNOTATED {label}")),
            GridData=build_grid(row_ann, 0),
            TimestampData=timestamp
        )

        field.Annotations = [ann]
        annotated_fields.append(field)

    # Build one annotated section
    annotated_section = AnnotatedTaxSectionData(
        SectionId="SEC_PERSONAL",
        SectionLabel="Personal Info",
        SectionType="info",
        FormFields=annotated_fields[:-1],  # first four fields
        Annotations=[],                   # no section-level annotations
        GridData=build_grid(0,0),
        TimestampData=timestamp
    )

    # Another section for the Dummy field
    other_section = AnnotatedTaxSectionData(
        SectionId="SEC_OTHER",
        SectionLabel="Other Info",
        SectionType="misc",
        FormFields=[annotated_fields[-1]],
        Annotations=[],
        GridData=build_grid(4,0),
        TimestampData=timestamp
    )

    # Finally, the annotated form
    annotated_form = AnnotatedTaxFormData(
        FormId="FORM001",
        FormLabel="Dummy Tax Form (Annotated)",
        FormVersion="1.0",
        FormType="TAX",
        Sections=[annotated_section, other_section],
        Annotations=[],
        GridData=build_grid(0,0),
        TimestampData=timestamp
    )

    # Populate all values (calls populate on fields and annotations)
    annotated_form.call_populate_depth_first({})

    # View as dict
    return annotated_form

if __name__ == "__main__":
    # Generate and print the dummy annotated form instance
    generate_dummy_annotated_form()
    print("Dummy Annotated Form Instance Created Successfully.")