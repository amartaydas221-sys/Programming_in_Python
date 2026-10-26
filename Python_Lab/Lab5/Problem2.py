students = [
    [201, "Amina", [78, 85, 90]],
    [202, "Rahim", [65, 70, 68]],
    [203, "Nadia", [92, 88, 95]],
    [204, "Hasan", [55, 60, 65]],
    [205, "Tania", [80, 80, 80]]
]


def validate_marks(marks):

    if not isinstance(marks, list) or len(marks) != 3:
        return False

    for mark in marks:

        if not isinstance(mark, (int, float)):
            return False

        if isinstance(mark, bool):
            return False

        if mark < 0 or mark > 100:
            return False

    return True


def calculate_average(marks):

    if not validate_marks(marks):
        return None

    average = sum(marks) / len(marks)

    return average


def classify_performance(average):

    if average is None:
        return "Invalid Data"

    if average >= 80:
        return "Excellent"

    elif average >= 70:
        return "Good"

    elif average >= 60:
        return "Satisfactory"

    else:
        return "Needs Improvement"


def display_report(students):

    if len(students) == 0:
        print("No student records available.")
        return

    print("\n--- Student Performance Report ---")

    for student in students:

        if not isinstance(student, list) or len(student) != 3:
            print("Invalid student record:", student)
            continue

        student_id = student[0]
        name = student[1]
        marks = student[2]

        average = calculate_average(marks)

        if average is None:
            print(
                "ID:", student_id,
                "| Name:", name,
                "| Average: Invalid",
                "| Performance: Invalid Data"
            )
            continue

        performance = classify_performance(average)

        print(
            "ID:", student_id,
            "| Name:", name,
            "| Average:", round(average, 2),
            "| Performance:", performance
        )


display_report(students)


print("\n--- Testing Equal Marks ---")

marks = [80, 80, 80]

print("Marks:", marks)
print("Average:", calculate_average(marks))
print("Performance:", classify_performance(calculate_average(marks)))


print("\n--- Testing Tied Averages ---")

student_a = [301, "Student A", [70, 80, 90]]
student_b = [302, "Student B", [80, 80, 80]]

average_a = calculate_average(student_a[2])
average_b = calculate_average(student_b[2])

print("Student A Average:", average_a)
print("Student B Average:", average_b)


print("\n--- Testing Invalid Mark ---")

invalid_marks = [80, 105, 90]

print("Average:", calculate_average(invalid_marks))


print("\n--- Testing Missing Marks ---")

missing_students = [
    [303, "Student C", []]
]

display_report(missing_students)


print("\n--- Testing Empty Student List ---")

display_report([])