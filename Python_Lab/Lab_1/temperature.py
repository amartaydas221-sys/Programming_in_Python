
temperature = float(input("Enter the temperature in Celsius: "))

if temperature >= 35:
    print("It is very hot!")
elif temperature >= 25:
    print("The weather is warm.")
elif temperature >= 15:
    print("The weather is cool.")
else:
    print("It is cold!")