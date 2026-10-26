character = input("Enter a character: ")

if len(character) == 1 and character.isalpha():
    if character.lower() in "aeiou":
        print(character, "is a vowel")
    else:
        print(character, "is not a vowel")
else:
    print("Please enter exactly one alphabetic character")