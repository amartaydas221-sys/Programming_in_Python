#Implemented By Sazid Ahmed Ekram
from file_handler import load_data, save_data
from database import distribute_relief
from datetime import date

# Declare the global variables
family_collection = "families"
inventory_collection = "inventory"
distribution_collection = "distribution"

def menu():
    while True:
        print("=============================")
        print("Relief-Distribution")
        print("===========================")
        print("You need to search a Family to distribute the relief")
        print("1. Search Family By ID")
        print("2. Search Family By Name")
        print("3. Search Family By Phone Number")
        print("4. Go Back")

        choice = input("Enter your choice: ")
        families = load_data(family_collection)
        found = False
        match choice:
            case "1":
                family_id = input("Enter Family ID: ")
                for family in families:
                    if family_id.lower() == family["familyId"].lower():
                        found = True
                        display_family(family)
                        display_current_status(family)

                        if check_current_status(family):
                            relief_distribution(family)
                            break

            case "2":
                family_name = input("Enter Family's Head Name: ")
                for family in families:
                    if family_name.lower() == family["headName"].lower():
                        found = True
                        display_family(family)
                        display_current_status(family)

                        if check_current_status(family):
                            relief_distribution(family)
                            break

            case "3":
                phone_number = input("Enter Family's Phone Number: ")
                for family in families:
                    if phone_number == family["phone"]:
                        found = True
                        display_family(family)
                        display_current_status(family)

                        if check_current_status(family):
                            relief_distribution(family)
                            break

            case "4":
                return
            case _:
                print("Invalid choice")

        if not found:
            print("There is no family with that information")

def display_family(family):
    print("------------------------------------------------------------")
    print("Family ID: ", family["familyId"])
    print("Family Head's Name: ", family["headName"])
    print("Phone Number: ", family["phone"])
    print("District: ", family["district"])
    print("upazila", family["upazila"])
    print("village: ", family["village"])
    print("Family Members: ", family["members"])
    print("Children: ", family["children"])
    print("Elderly: ", family["elderly"])
    print("Disabled Members: ", family["disabledMembers"])
    print("Damage Level: ", family["damageLevel"])
    if family["shelterNeeded"]:
        print("Shelter Needed: Yes")
    else:
        print("Shelter Needed: No")

    if family["receivedRelief"]:
        print("Received Relief: Yes")
    else:
        print("Received Relief: No")
    print("------------------------------------------------------------")


def check_current_status(family):
    return not family["receivedRelief"]

def display_current_status(family):
    if check_current_status(family):
        print("This family is eligible for the relief.")
    else:
        print("This family has already received the relief.")
    print("------------------------------------------------------------")

def relief_distribution(family):
    if family["receivedRelief"]:
        print("This family has already received the relief.")
        return

    package_status = {
        "Low": "Small",
        "Medium": "Medium",
        "High": "Large",
        "Extreme": "Extreme",
    }.get(family["damageLevel"])
    if package_status is None:
        print("Invalid damage level.")
        return

    print(f"This family will receive the {package_status} Relief Package")
    if not check_inventory(package_status):
        print("Distribution failed.")
        return

    confirm = input("Distribute this package? (Y/N): ")
    if confirm.lower() != "y":
        print("Cancelled.")
        return

    try:
        _, package_status = distribute_relief(
            family["familyId"],
            relief_package(),
        )
    except ValueError as error:
        print(f"Distribution failed: {error}")
        return

    print(f"This family will receive the {package_status} Relief Package")
    print("--------------------------------")
    print("Relief Distributed Successfully")
    print("--------------------------------")


# Inventory Check
def check_inventory(package_name):
    # Load inventory from SQLite.
    inventory = load_data(inventory_collection)
    #  For Particular Package
    package = relief_package()[package_name]

    for item_name, required_qty in package.items():
        found = False
        for item in inventory:
            if item["itemName"].lower() == item_name.lower():
                found = True

                if item["quantity"] < required_qty:
                    print(f"Not enough {item_name}")
                    return False

        if not found:
            print(f"{item_name} not found in inventory")
            return False

    return True

def update_inventory(package_name):
    # Load
    inventory = load_data(inventory_collection)
    # each package
    package = relief_package()[package_name]

    for item in inventory:
        if item["itemName"] in package.keys():
            item["quantity"] -= package[item["itemName"]]

    save_data(inventory, inventory_collection)


def update_family_status(family):
    # Load the family JSON file to the python
    families = load_data(family_collection)

    for f in families:
        if f["familyId"] == family["familyId"]:
            f["receivedRelief"] = True
            break
    save_data(families, family_collection)

def save_distribution(package_name, family):
    history = load_data(distribution_collection)
    package = relief_package()[package_name]

    record = {
        "distributionId": f"D{len(history)+1:03}",
        "date": str(date.today()),
        "familyId": family["familyId"],
        "headName": family["headName"],
        "package": package_name,
        "items": []
    }
    inventory = load_data(inventory_collection)

    for item_name, qty in package.items():
        unit = ""
        for i in inventory:
            if i["itemName"] == item_name:
                unit = i["unit"]
                break

        record["items"].append({
            "itemName": item_name,
            "quantity": qty,
            "unit": unit
        })
    history.append(record)
    save_data(history, distribution_collection)

# Later I have to link this function to view the distribution history in the view features
def view_distribution_history():
    history = load_data(distribution_collection)
    if len(history) == 0:
        print("No history found.")
        return

    for record in history:
        print("="*40)
        print("Distribution ID :", record["distributionId"])
        print("Date :", record["date"])
        print("Family ID :", record["familyId"])
        print("Head Name :", record["headName"])
        print("Package :", record["package"])
        print("Items")
        for item in record["items"]:
            print(f"  {item['itemName']} : {item['quantity']} {item['unit']}")
        print("="*40)


def relief_package():
    return {
        "Small": {
            "Rice": 5,
            "Water": 6,
            "Blanket": 1
        },
        "Medium": {
            "Rice": 10,
            "Water": 12,
            "Blanket": 2,
            "Medicine": 1
        },
        "Large": {
            "Rice": 20,
            "Water": 24,
            "Blanket": 5,
            "Medicine": 2,
            "Baby Food": 3,
            "Hygiene Kit": 2
        },
        "Extreme": {
            "Rice": 25,
            "Water": 24,
            "Blanket": 5,
            "Medicine": 2,
            "Baby Food": 3,
            "Hygiene Kit": 2,
            "Clothes": 1,
            "Mosquito Net": 1,
            "Cooking Oil": 1,
            "Dry Food": 5,
            "Tent": 1,
            "Torch Light": 1
        }
    }