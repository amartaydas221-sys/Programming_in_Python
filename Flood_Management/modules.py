from file_handler import load_families as load_family_records
from file_handler import save_families as save_family_records
from models import Family

# Load Families from the database
def load_families():
    return load_family_records()


# Save Families to the database
def save_families(data):
    return save_family_records(data)


# Validation Functions

# Check Duplicate Family ID
def validate_duplicate_id(families, familyId):

    for family in families:
        if family["familyId"] == familyId:
            return False

    return True


# Check Empty Name
def validate_name(headName):

    return headName.strip() != ""


# Check Phone Number
def validate_phone(phone):

    return phone.isdigit() and len(phone) == 11


# Check Number of Members
def validate_members(members):

    return members > 0


# Check Damage Level
def validate_damage_level(damageLevel):

    damageLevel = damageLevel.capitalize()

    if damageLevel in ["Low", "Medium", "High"]:
        return True

    return False


# Check Yes/No Input
def validate_yes_no(choice):

    choice = choice.lower()

    if choice == "yes" or choice == "no":
        return True

    return False