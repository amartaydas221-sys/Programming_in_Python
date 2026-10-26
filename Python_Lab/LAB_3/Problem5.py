marks = float(input("Enter student's marks (0-100): "))

if marks < 0 or marks > 100:
    print("Invalid marks. Enter marks between 0 and 100.")

elif marks >= 90:
    print("Grade: A+")

elif marks >= 85:
    print("Grade: A")

elif marks >= 80:
    print("Grade: B+")

elif marks >= 75:
    print("Grade: B")

elif marks >= 70:
    print("Grade: C+")

elif marks >= 65:
    print("Grade: C")

elif marks >= 60:
    print("Grade: D+")

elif marks >= 50:
    print("Grade: D")

else:
    print("Grade: F")