import math

# Take coordinates of the first point
x1 = float(input("Enter x1: "))
y1 = float(input("Enter y1: "))

# Take coordinates of the second point
x2 = float(input("Enter x2: "))
y2 = float(input("Enter y2: "))

# Calculate the distance
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Display the result
print("Distance between the two points:", distance)