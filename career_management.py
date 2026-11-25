
# Career Management Module

career_roles = {
    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Statistics",
        "Power BI"
    ],

    "Python Developer": [
        "Python",
        "OOP",
        "Data Structures",
        "SQL",
        "Git"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Python",
        "SQL"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Machine Learning",
        "Data Visualization"
    ]
}


def select_career():
    print("\n===== CAREER SELECTION =====")

    for career in career_roles:
        print("-", career)

    choice = input("\nEnter your desired career: ")

    if choice in career_roles:
        print("\nCareer selected successfully!")
        print("Required Skills:", career_roles[choice])
        return choice
    else:
        print("Invalid career selection.")
        return None
if __name__ == "__main__":
    select_career()