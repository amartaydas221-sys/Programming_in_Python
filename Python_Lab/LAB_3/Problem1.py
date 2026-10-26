# Take two values from the user
a = input("Enter the first value: ")
b = input("Enter the second value: ")

print("Before swapping:")
print("a =", a)
print("b =", b)

# Swap the values using a temporary variable
temp = a
a = b
b = temp

print("After swapping:")
print("a =", a)
print("b =", b)