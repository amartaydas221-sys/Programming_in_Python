def main():
    while True:
        print("=============================")
        print("RELIEFLINK MAIN MENU")
        print("=============================")
        print("1. Family Management") #Easha
        print("2. Relief Inventory") # Borshon
        print("3. Shelter Management") # Sazid
        print("4. Relief Distribution") # Sazid
        print("5. Reports")       # Anurag
        print("6. Statistics")    # Anurag
        print("7. Exit")

        choice = input("Enter your choice: ")

        match(choice):
            case "1":
                import family_manager
                family_manager.family_menu()
            case "2":
                import inventory_manager
                inventory_manager.inventoryMenu()
            case "3":
                # Implemented by Sazid
                import shelter_manager
                shelter_manager.menu()
            case "4":
                #Implemented by Sazid
                import relief_distribution
                relief_distribution.menu()
            case "5":
                import reports
                reports.reportMenu()

            case "6":
                import statistics
                statistics.menu()
            case "7":
                break
            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
