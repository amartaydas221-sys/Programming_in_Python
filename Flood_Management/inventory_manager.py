#Implementation-Borshon Debnath
from file_handler import load_inventory, save_inventory

# Inventory Menu
def inventoryMenu():
    while True:
        print("==============================")
        print("Inventory Management")
        print("=============================")
        print("1.Add Item")
        print("2.View Items")
        print("3.Search Item")
        print("4.Update Quantity")
        print("5.Delete Item")
        print("6.Low Stock Alert")
        print("7.Back")

        option=input("Enter your option :")

        if option == "1":
            addItem()
        elif option == "2":
            viewItems()   
        elif option == "3":
            searchItem()
        elif option == "4":
           updateQuantity()          
        elif option == "5":
            deleteItem()  
        elif option == "6":
            lowStockAlert()
        elif option == "7":
            print("Returning to main menu")
            break

        else:
            print("Invalid Option")                                             
# View All Inventory Items
def viewItems():
    try:
        items = load_inventory()

        print("-----INVENTORY----")

        for item in items:
            print(f"Item ID:{item['itemId']}")
            print(f"Name:{item['itemName']}")
            print(f"Quantity:{item['quantity']} {item['unit']}")
            print(f"Minimum:{item['minimumStock']}")
            print("----------------------------")

    except FileNotFoundError:
        print("File not found.")

# Search an Item by Item ID
def searchItem():

    itemId=input("Enter Item ID: ")

    items = load_inventory()

    for item in items:

        if item["itemId"]==itemId:

            print("\nItem Found")
            print("ID:",item["itemId"])
            print("Name:",item["itemName"])
            print("Quantity:",item["quantity"],item["unit"])
            print("Minimum Stock:",item["minimumStock"])
            return

    print("Item not found.")


# Add a New Inventory Item
def addItem():

    items = load_inventory()

    itemId=input("Enter Item ID: ")

    for item in items:
        if item["itemId"]==itemId:
            print("Item ID already exists.")
            return

    itemName=input("Enter Item Name: ")
    quantity=int(input("Enter Quantity: "))
    unit=input("Enter Unit: ")
    minimumStock=int(input("Enter Minimum Stock: "))

    # Create a new inventory item using a dictionary
    newItem={
    "itemId":itemId,
    "itemName":itemName,
    "quantity":quantity,
    "unit":unit,
    "minimumStock":minimumStock
    }
    items.append(newItem)
    # Save changes
    save_inventory(items)

    print("Item Added Successfully.")

# Update Quantity of an Existing Item
def updateQuantity():

    items = load_inventory()

    itemId=input("Enter Item ID: ")

    for item in items:

        if item["itemId"]==itemId:

            quantity=int(input("Enter New Quantity: "))
            item["quantity"] = quantity

            save_inventory(items)

            print("Quantity Updated Successfully.")
            return

    print("Item Not Found.")

# Delete an Item from Inventory
def deleteItem():

    items = load_inventory()

    itemId=input("Enter Item ID: ")

    for item in items:

        if item["itemId"]==itemId:

            items.remove(item)

            save_inventory(items)

            print("Item Deleted Successfully.")
            return

    print("Item Not Found.")  

# Display Low Stock Items
def lowStockAlert():

    items = load_inventory()

    print("Low Stock Items")
    print("------------")
    found=False


    for item in items:

        if item["quantity"]<=item["minimumStock"]:

            print("Item ID:",item["itemId"])
            print("Item Name:",item["itemName"])
            print("Quantity:",item["quantity"], item["unit"])
            print("Minimum Stock:",item["minimumStock"])
            print()
            found=True

    if not found:
            print("No Low Stock Items.")
      

if __name__ == "__main__":
    inventoryMenu()        