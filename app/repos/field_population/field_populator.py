from app.models.FormData import PopulationFunction


class DefaultDummyFieldPopulateRepo(PopulationFunction):
    def populate(self, field_data: dict=None) -> str:
        self.result = "DUMMY VALUE"
        return self.result

class FNameFieldPopulateRepo(PopulationFunction):
    def populate(self, field_data: dict=None) -> str:
        self.result = "John Doe"
        return self.result

class LNameFieldPopulateRepo(PopulationFunction):
    def populate(self, field_data: dict=None) -> str:
        self.result = "Smith"
        return self.result

class EmailFieldPopulateRepo(PopulationFunction):
    def populate(self, field_data: dict=None) -> str:
        self.result = "test_email"
        return self.result

class PhoneFieldPopulateRepo(PopulationFunction):
    def populate(self, field_data: dict=None) -> str:
        self.result = "123-456-7890"
        return self.result


