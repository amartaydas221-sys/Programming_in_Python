from file_handler import load_families, save_families
from models import Family


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


# Add Family
def add_family():

    families = load_families()

    print("\n========== ADD FAMILY ==========\n")

    familyId = input("Enter Family ID: ")

    if not validate_duplicate_id(families, familyId):
        print("Family ID already exists.")
        return

    headName = input("Enter Head Name: ")

    if not validate_name(headName):
        print("Head Name cannot be empty.")
        return

    phone = input("Enter Phone Number: ")

    if not validate_phone(phone):
        print("Invalid phone number.")
        return

    district = input("Enter District: ")
    upazila = input("Enter Upazila: ")
    village = input("Enter Village: ")

    try:
        members = int(input("Enter Number of Members: "))

        if not validate_members(members):
            print("Members must be greater than zero.")
            return

        children = int(input("Enter Number of Children: "))
        elderly = int(input("Enter Number of Elderly: "))
        disabledMembers = int(input("Enter Number of Disabled Members: "))

    except ValueError:
        print("Please enter valid numeric values.")
        return

    damageLevel = input("Enter Damage Level (Low/Medium/High): ")

    if not validate_damage_level(damageLevel):
        print("Invalid Damage Level.")
        return

    shelter = input("Shelter Needed (Yes/No): ")

    if not validate_yes_no(shelter):
        print("Please enter Yes or No.")
        return

    shelterNeeded = shelter.lower() == "yes"

    family = Family(
        familyId,
        headName,
        phone,
        district,
        upazila,
        village,
        members,
        children,
        elderly,
        disabledMembers,
        damageLevel.capitalize(),
        shelterNeeded
    )

    families.append(family.to_families_json())

    if save_families(families):
        print("\nFamily added successfully!")

# View Families
def view_families():

    families = load_families()

    if len(families) == 0:
        print("\nNo family records found.")
        return

    print("\n========== FAMILY LIST ==========\n")

    for family in families:

        print(f"Family ID          : {family['familyId']}")
        print(f"Head Name          : {family['headName']}")
        print(f"Phone              : {family['phone']}")
        print(f"District           : {family['district']}")
        print(f"Upazila            : {family['upazila']}")
        print(f"Village            : {family['village']}")
        print(f"Members            : {family['members']}")
        print(f"Children           : {family['children']}")
        print(f"Elderly            : {family['elderly']}")
        print(f"Disabled Members   : {family['disabledMembers']}")
        print(f"Damage Level       : {family['damageLevel']}")
        print(f"Shelter Needed     : {'Yes' if family['shelterNeeded'] else 'No'}")
        print(f"Received Relief    : {'Yes' if family['receivedRelief'] else 'No'}")

        print("-" * 50)


# Search Family
def search_family():

    families = load_families()

    if len(families) == 0:
        print("\nNo family records found.")
        return

    print("\nSearch By")
    print("1. Family ID")
    print("2. Head Name")
    print("3. Phone Number")

    choice = input("Enter your choice: ")

    found = False

    if choice == "1":
        search = input("Enter Family ID: ")

        for family in families:
            if family["familyId"] == search:
                print("\n========== FAMILY FOUND ==========")
                for key, value in family.items():
                    print(f"{key}: {value}")
                found = True
                break

    elif choice == "2":
        search = input("Enter Head Name: ").lower()

        for family in families:
            if family["headName"].lower() == search:
                print("\n========== FAMILY FOUND ==========")
                for key, value in family.items():
                    print(f"{key}: {value}")
                found = True

    elif choice == "3":
        search = input("Enter Phone Number: ")

        for family in families:
            if family["phone"] == search:
                print("\n========== FAMILY FOUND ==========")
                for key, value in family.items():
                    print(f"{key}: {value}")
                found = True
                break

    else:
        print("Invalid choice.")
        return

    if not found:
        print("Family not found.")

# Update Family
def update_family():

    families = load_families()

    if len(families) == 0:
        print("\nNo family records found.")
        return

    familyId = input("Enter Family ID to update: ")

    for family in families:

        if family["familyId"] == familyId:

            print("\nLeave blank if you don't want to change a field.\n")

            phone = input(f"Phone ({family['phone']}): ")

            if phone != "":
                if validate_phone(phone):
                    family["phone"] = phone
                else:
                    print("Invalid phone number.")

            district = input(f"District ({family['district']}): ")
            if district != "":
                family["district"] = district

            upazila = input(f"Upazila ({family['upazila']}): ")
            if upazila != "":
                family["upazila"] = upazila

            village = input(f"Village ({family['village']}): ")
            if village != "":
                family["village"] = village

            member = input(f"Members ({family['members']}): ")

            if member != "":
                try:
                    member = int(member)

                    if validate_members(member):
                        family["members"] = member
                    else:
                        print("Members must be greater than zero.")

                except ValueError:
                    print("Invalid input.")

            damage = input(f"Damage Level ({family['damageLevel']}): ")

            if damage != "":
                if validate_damage_level(damage):
                    family["damageLevel"] = damage.capitalize()
                else:
                    print("Invalid damage level.")

            save_families(families)

            print("\nFamily updated successfully.")

            return

    print("Family ID not found.")

# Delete Family
def delete_family():

    families = load_families()

    if len(families) == 0:
        print("\nNo family records found.")
        return

    familyId = input("Enter Family ID to delete: ")

    for family in families:

        if family["familyId"] == familyId:

            confirm = input("Are you sure? (Yes/No): ").lower()

            if confirm == "yes":

                families.remove(family)

                save_families(families)

                print("Family deleted successfully.")

            else:
                print("Deletion cancelled.")

            return

    print("Family ID not found.")


# Family Management Menu
def family_menu():

    while True:

        print("\n==============================")
        print("    FAMILY MANAGEMENT")
        print("==============================")
        print("1. Add Family")
        print("2. View Families")
        print("3. Search Family")
        print("4. Update Family")
        print("5. Delete Family")
        print("6. Return to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_family()

        elif choice == "2":
            view_families()

        elif choice == "3":
            search_family()

        elif choice == "4":
            update_family()

        elif choice == "5":
            delete_family()

        elif choice == "6":
            print("Returning to Main Menu...")
            break

        else:
            print("Invalid choice. Please try again.")