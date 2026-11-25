
# University Student Skill Gap Analyzer

from career_management import career_roles


def analyze_skills(student_skills, selected_career):

    if selected_career not in career_roles:
        raise ValueError("Invalid career selected.")

    required_skills = career_roles[selected_career]

    matched_skills = []
    missing_skills = []

    # Compare skills without case sensitivity
    student_skill_set = {
        skill.strip().lower()
        for skill in student_skills
    }

    for skill in required_skills:

        if skill.strip().lower() in student_skill_set:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_skills = len(required_skills)

    if total_skills == 0:
        match_percentage = 0
    else:
        match_percentage = (
            len(matched_skills) / total_skills
        ) * 100

    # Return all analysis results
    return {
        "selected_career": selected_career,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(match_percentage, 2)
    }

