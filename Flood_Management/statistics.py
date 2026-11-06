# Anurag will work on

import numpy as np
from file_handler import load_families
from file_handler import load_inventory
from file_handler import load_shelters

def menu():

    while True:

        print("\n==============================")
        print("STATISTICS")
        print("==============================")
        print("1. Average Family Size")
        print("2. Maximum Family Members")
        print("3. Minimum Family Members")
        print("4. Total Affected People")
        print("5. Percentage of Families Served")
        print("6. High Priority Families")
        print("7. Shelter Occupancy Percentage")
        print("8. Average Inventory Remaining")
        print("9. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            averageFamilySize()

        elif choice == "2":
            maximumFamilyMembers()

        elif choice == "3":
            minimumFamilyMembers()

        elif choice == "4":
            totalAffectedPeople()

        elif choice == "5":
            percentageFamiliesServed()

        elif choice == "6":
            highPriorityFamilies()

        elif choice == "7":
            shelterOccupancyPercentage()

        elif choice == "8":
            averageInventoryRemaining()

        elif choice == "9":
            break

        else:
            print("Invalid Choice")



def averageFamilySize():

    families = load_families()

    if len(families) == 0:
        print("No Family Data Found")
        return

    members = []

    for family in families:
        members.append(family["members"])

    average = np.mean(members)

    print("\nAverage Family Size :", round(average, 2))


def maximumFamilyMembers():

    families = load_families()

    if len(families) == 0:
        print("No Family Data Found")
        return

    members = []

    for family in families:
        members.append(family["members"])

    maximum = np.max(members)

    print("\nMaximum Family Members :", maximum)


def minimumFamilyMembers():

    families = load_families()

    if len(families) == 0:
        print("No Family Data Found")
        return

    members = []

    for family in families:
        members.append(family["members"])

    minimum = np.min(members)

    print("\nMinimum Family Members :", minimum)

def totalAffectedPeople():

    families = load_families()

    if len(families) == 0:
        print("No Family Data Found")
        return

    members = []

    for family in families:
        members.append(family["members"])

    total = np.sum(members)

    print("\nTotal Affected People :", total)


def percentageFamiliesServed():

    families = load_families()

    if len(families) == 0:
        print("No Family Data Found")
        return

    served = 0

    for family in families:

        if family["receivedRelief"] == True:
            served = served + 1

    percentage = (served / len(families)) * 100

    print("\nFamilies Served :", served)
    print("Percentage of Families Served :", round(percentage, 2), "%")


def highPriorityFamilies():

    families = load_families()

    if len(families) == 0:
        print("No Family Data Found")
        return

    high = 0

    for family in families:

        if family["damageLevel"] == "High":
            high = high + 1

    print("\nHigh Priority Families :", high)


def shelterOccupancyPercentage():

    shelters = load_shelters()

    if len(shelters) == 0:
        print("No Shelter Found")
        return

    print("\nShelter Occupancy Percentage")
    print("-----------------------------")

    for shelter in shelters:

        if shelter["capacity"] == 0:
            percentage = 0
        else:
            percentage = (shelter["currentOccupancy"] / shelter["capacity"]) * 100

        print("Shelter :", shelter["shelterName"])
        print("Occupancy :", round(percentage, 2), "%")
        print("-----------------------------")


def averageInventoryRemaining():

    inventory = load_inventory()

    if len(inventory) == 0:
        print("Inventory Empty")
        return

    quantities = []

    for item in inventory:
        quantities.append(item["quantity"])

    average = np.mean(quantities)

    print("\nAverage Inventory Remaining :", round(average, 2))