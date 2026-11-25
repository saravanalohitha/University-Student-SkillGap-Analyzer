students = []

def add_student():
    print("\n===== STUDENT PROFILE =====")

    name = input("Enter student name: ")
    student_id = input("Enter student ID: ")
    course = input("Enter course: ")

    skills = input("Enter skills separated by commas: ")

    student = {
        "Name": name,
        "Student ID": student_id,
        "Course": course,
        "Skills": [s.strip() for s in skills.split(",")]
    }

    students.append(student)
    print("\nStudent profile created successfully!")


def view_students():
    print("\n===== STUDENT DETAILS =====")

    if not students:
        print("No student profiles found.")
        return

    for student in students:
        print(student)
if __name__ == "__main__":
    add_student()
    view_students()