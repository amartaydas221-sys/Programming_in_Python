total = 0

for number in range(2, 1000):
    is_prime = True

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            is_prime = False
            break

    if is_prime:
        total += number

print("Sum of prime numbers below 1000:", total)