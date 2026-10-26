number = int(input("Enter a number for countdown: "))

if number < 0:
    print("Please enter a non-negative number.")
else:
    while number >= 0:
        print(number)
        number -= 1

    print("Countdown finished!")