N = int(input("Enter the upper limit N: "))

if N <= 0:
    print("Please enter a positive number.")
else:
    first = 0
    second = 1

    print("Fibonacci numbers below", N, ":")

    while first < N:
        print(first, end=" ")

        next_number = first + second
        first = second
        second = next_number

    print()