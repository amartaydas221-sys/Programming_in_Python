# Implemented by Sazid Ahmed Ekram
class ShelterManagement:
    # Initialize by the parameterized constructors
    def __init__(self, shelterId, shelterName, district, capacity):
        self.shelterId = shelterId
        self.shelterName = shelterName
        self.district = district
        self.capacity = capacity
        self.currentOccupancy = 0
        self.families = []

    # Load the data to the JSON files
    def to_shelter_json(self):
        return {
            "shelterId": self.shelterId,
            "shelterName": self.shelterName,
            "district": self.district,
            "capacity": self.capacity,
            "currentOccupancy": self.currentOccupancy,
            "families": self.families
        }

