# Campus Resource Tracker

# Sample resource data
# Each record contains: ID, Name, Category, Quantity

resources = [
    [101, "Laptop", "Electronics", 8],
    [102, "Projector", "Electronics", 0],
    [103, "Whiteboard", "Classroom", 5],
    [104, "Microphone", "Audio", 3],
    [105, "Camera", "Electronics", 2]
]


# Function 1: Display all resources
def display_resources(resources):

    if not resources:
        print("No resources available.")
        return

    print("\n--- All Campus Resources ---")

    for resource in resources:
        print("Resource ID:", resource[0])
        print("Name:", resource[1])
        print("Category:", resource[2])
        print("Available Quantity:", resource[3])
        print("------------------------")


# Function 2: Search resources by category
def search_by_category(resources, category):

    found = False

    print("\n--- Search Results ---")

    for resource in resources:

        if resource[2].lower() == category.lower():
            print(
                "ID:", resource[0],
                "| Name:", resource[1],
                "| Category:", resource[2],
                "| Quantity:", resource[3]
            )

            found = True

    if not found:
        print("No resources found in this category.")


# Function 3: Find unavailable resources
def find_unavailable(resources):

    found = False

    print("\n--- Unavailable Resources ---")

    for resource in resources:

        if resource[3] == 0:
            print(
                "ID:", resource[0],
                "| Name:", resource[1],
                "| Category:", resource[2]
            )

            found = True

    if not found:
        print("All resources are currently available.")


# Function 4: Search for a resource by ID
def search_by_id(resources, resource_id):

    for resource in resources:

        if resource[0] == resource_id:
            return resource

    return None


# Function 5: Add a new resource
def add_resource(resources, resource_id, name, category, quantity):

    # Check whether the ID already exists
    if search_by_id(resources, resource_id) is not None:
        print("Error: Resource ID already exists.")
        return

    # Check for a negative quantity
    if quantity < 0:
        print("Error: Quantity cannot be negative.")
        return

    # Add the new resource
    resources.append([resource_id, name, category, quantity])

    print("Resource added successfully.")


# Main program
display_resources(resources)

search_by_category(resources, "Electronics")

find_unavailable(resources)

# Test an unknown resource ID
result = search_by_id(resources, 999)

if result is None:
    print("\nResource ID 999 was not found.")

# Test adding a resource with a negative quantity
add_resource(resources, 106, "Tablet", "Electronics", -2)

# Test adding a resource with a valid quantity
add_resource(resources, 106, "Tablet", "Electronics", 4)

# Test the empty resource list
empty_resources = []

print("\nTesting empty resource list:")
display_resources(empty_resources)
search_by_category(empty_resources, "Electronics")
find_unavailable(empty_resources)