base = int(input("Enter the base: "))
exponent = int(input("Enter a non-negative exponent: "))

if exponent < 0:
    print("Please enter a non-negative exponent.")
else:
    result = 1

    for i in range(exponent):
        result = result * base

    print("Result:", result)