
print("=" * 45)
print("UNIVERSITY STUDENT SKILL GAP ANALYZER")
print("=" * 45)

from student_data import add_student, view_students, students
from career_management import select_career
from skill_analyzer import analyze_skills

# Step 1: Register student
add_student()

# Step 2: Display student details
view_students()

# Step 3: Select career
selected_career = select_career()

# Step 4: Analyze skills
if selected_career and students:
    student_skills = students[-1]["Skills"]
    analyze_skills(student_skills, selected_career)

print("\nProject execution completed!")
