test_json = """
{
  "FormId": "FORM001",
  "FormLabel": "Employee Tax Declaration",
  "FormVersion": "2025.1",
  "FormType": "Annual",
  "ComponentStatus": "Draft",
  "GridData": {
    "GridId": "main-grid-001",
    "GridLabel": "Main Grid",
    "IsHighlighted": false,
    "IsEditable": true,
    "GridTopLeft": "A1",
    "GridBottomRight": "D20",
    "GridHDivisions": 4,
    "GridVDivisions": 20,
    "TimestampData": {
      "CreatedDate": "2025-08-01T09:00:00Z",
      "LastModifiedDate": "2025-08-01T10:00:00Z",
      "LastModifiedBy": "system"
    }
  },
  "TimestampData": {
    "CreatedDate": "2025-08-01T08:55:00Z",
    "LastModifiedDate": "2025-08-01T10:10:00Z",
    "LastModifiedBy": "admin"
  },
  "Sections": [
    {
      "SectionId": "SEC001",
      "SectionLabel": "Personal Information",
      "SectionType": "Header",
      "ComponentStatus": "Draft",
      "GridData": {
        "GridId": "section-grid-01",
        "GridLabel": "Personal Info Grid",
        "IsHighlighted": true,
        "IsEditable": true,
        "GridTopLeft": "A1",
        "GridBottomRight": "B10",
        "GridHDivisions": 2,
        "GridVDivisions": 10,
        "TimestampData": {
          "CreatedDate": "2025-08-01T09:10:00Z",
          "LastModifiedDate": "2025-08-01T09:30:00Z",
          "LastModifiedBy": "user123"
        }
      },
      "TimestampData": {
        "CreatedDate": "2025-08-01T09:00:00Z",
        "LastModifiedDate": "2025-08-01T09:30:00Z",
        "LastModifiedBy": "user123"
      },
      "FormFields": [
        {
          "FieldId": "FIELD001",
          "FieldLabel": "Full Name",
          "FieldValue": "Jane Doe",
          "FieldType": "Text",
          "ComponentStatus": "Draft",
          "GridData": {
            "GridId": "field-grid-01",
            "GridLabel": "Name Field",
            "IsHighlighted": false,
            "IsEditable": true,
            "GridTopLeft": "A1",
            "GridBottomRight": "A1",
            "GridHDivisions": 1,
            "GridVDivisions": 1,
            "TimestampData": {
              "CreatedDate": "2025-08-01T09:15:00Z",
              "LastModifiedDate": "2025-08-01T09:20:00Z",
              "LastModifiedBy": "user123"
            }
          },
          "TimestampData": {
            "CreatedDate": "2025-08-01T09:15:00Z",
            "LastModifiedDate": "2025-08-01T09:20:00Z",
            "LastModifiedBy": "user123"
          }
        }
      ]
    }
  ]
}

"""