# Implemented by Anurag Sarkar

from file_handler import load_families
from file_handler import load_inventory
from file_handler import load_shelters
from file_handler import load_distribution


def reportMenu():

    while True:

        print("\n==============================")
        print("        REPORT MENU")
        print("==============================")
        print("1. Total Families")
        print("2. Families Served")
        print("3. Families Waiting")
        print("4. Families by District")
        print("5. Families by Damage Level")
        print("6. Inventory Remaining")
        print("7. Shelter Occupancy")
        print("8. Distribution History")
        print("9. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            totalFamilies()

        elif choice == "2":
            familiesServed()

        elif choice == "3":
            familiesWaiting()

        elif choice == "4":
            familiesByDistrict()

        elif choice == "5":
            familiesByDamageLevel()

        elif choice == "6":
            inventoryRemaining()

        elif choice == "7":
            shelterOccupancy()

        elif choice == "8":
            distributionHistory()

        elif choice == "9":
            break

        else:
            print("Invalid Choice")


# Total Families

def totalFamilies():

    families = load_families()

    count = 0

    for family in families:
        count = count + 1

    print("\nTotal Registered Families :", count)



# Families Served

def familiesServed():

    families = load_families()

    served = 0

    for family in families:

        if family["receivedRelief"] == True:
            served = served + 1

    print("\nFamilies Served :", served)


# Families Waiting

def familiesWaiting():

    families = load_families()

    waiting = 0

    for family in families:

        if family["receivedRelief"] == False:
            waiting = waiting + 1

    print("\nFamilies Waiting :", waiting)


# Families By District

def familiesByDistrict():

    families = load_families()

    count = 0

    for family in families:
        count = count + 1

    if count == 0:
        print("No Family Data Found")
        return

    districtCount = {}  #empty_dict

    for family in families:

        district = family["district"]

        if district in districtCount:
            districtCount[district] = districtCount[district] + 1
        else:
            districtCount[district] = 1

    print("\nFamilies By District")
    print("--------------------------")

    for district in districtCount:

        print(district, ":", districtCount[district])


# Families By Damage Level

def familiesByDamageLevel():

    families = load_families()

    count = 0

    for family in families:
        count = count + 1

    if count == 0:
        print("No Family Data Found")
        return

    damageCount = {}

    for family in families:

        damage = family["damageLevel"]

        if damage in damageCount:
            damageCount[damage] = damageCount[damage] + 1
        else:
            damageCount[damage] = 1

    print("\nFamilies By Damage Level")
    print("--------------------------")

    for damage in damageCount:

        print(damage, ":", damageCount[damage])


# Inventory Remaining

def inventoryRemaining():

    inventory = load_inventory()

    count = 0

    for item in inventory:
        count = count + 1

    if count == 0:
        print("Inventory Empty")
        return

    print("\nInventory Remaining")
    print("--------------------------")

    for item in inventory:

        print("Item ID :", item["itemId"])
        print("Item Name :", item["itemName"])
        print("Quantity :", item["quantity"], item["unit"])
        print("Minimum Stock :", item["minimumStock"])
        print("--------------------------")


# Shelter Occupancy

def shelterOccupancy():

    shelters = load_shelters()

    count = 0

    for shelter in shelters:
        count = count + 1

    if count == 0:
        print("No Shelter Found")
        return

    print("\nShelter Occupancy")
    print("--------------------------")

    for shelter in shelters:

        print("Shelter ID :", shelter["shelterId"])
        print("Shelter Name :", shelter["shelterName"])
        print("District :", shelter["district"])
        print("Capacity :", shelter["capacity"])
        print("Current Occupancy :", shelter["currentOccupancy"])
        print("--------------------------")


# Distribution History

def distributionHistory():

    history = load_distribution()

    count = 0

    for record in history:
        count = count + 1

    if count == 0:
        print("No Distribution History Found")
        return

    print("\nDistribution History")
    print("--------------------------")

    for record in history:

        print("Distribution ID :", record["distributionId"])
        print("Date :", record["date"])
        print("Family ID :", record["familyId"])
        print("Head Name :", record["headName"])
        print("Package :", record["package"])

        print("Items :")

        for item in record["items"]:

            print(item["itemName"], "-", item["quantity"], item["unit"])

        print("--------------------------")