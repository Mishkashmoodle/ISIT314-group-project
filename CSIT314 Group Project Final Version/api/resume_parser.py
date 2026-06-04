import pdfplumber
from docx import Document
import re


KNOWN_SKILLS = [
    "Python", "Java", "JavaScript", "HTML", "CSS", "SQL", "Excel",
    "Word", "PowerPoint", "Microsoft Office", "Data Analysis",
    "Data Analytics", "Communication", "Customer Service",
    "Leadership", "Problem Solving", "Critical Thinking",
    "Legal Research", "Analytical Skills", "Computer Literacy",
    "Databases", "Digital Systems", "Cyber Security",
    "Project Management", "Bartending", "Training"
]

EDUCATION_KEYWORDS = [
    "Doctorate",
    "Master's Degree",
    "Bachelor's Degree",
    "Graduate Diploma",
    "Graduate Certificate",
    "Advanced Diploma",
    "Associate Degree",
    "Diploma",
    "Certificate IV",
    "Certificate III",
    "Certificate II",
    "Certificate I",
    "High School",
    "HSC"
]

MAJOR_KEYWORDS = [

    # Technology
    "Computer Science",
    "Software Engineering",
    "Computer Engineering",
    "Information Systems",
    "Information Technology",
    "Cyber Security",
    "Data Science",
    "Data Analytics",
    "Big Data",
    "Artificial Intelligence",
    "AI",

    # Business
    "Business",
    "Business Administration",
    "Business Analytics",
    "Commerce",
    "Accounting",
    "Finance",
    "Economics",
    "Marketing",
    "Human Resources",
    "Human Resource Management",
    "Management",
    "Project Management",

    # Law
    "Law",
    "Legal Studies",
    "Criminology",

    # Engineering
    "Engineering",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Environmental Engineering",

    # Health
    "Nursing",
    "Medicine",
    "Medical Science",
    "Health Science",
    "Public Health",
    "Physiotherapy",
    "Occupational Therapy",
    "Pharmacy",

    # Science
    "Science",
    "Biology",
    "Chemistry",
    "Physics",
    "Mathematics",
    "Statistics",

    # Education
    "Education",
    "Teaching",
    "Early Childhood Education",

    # Arts / Humanities
    "Arts",
    "Psychology",
    "History",
    "Philosophy",
    "Sociology",
    "Political Science",
    "International Studies",

    # Media / Creative
    "Graphic Design",
    "Digital Media",
    "Communications",
    "Journalism",
    "Media Studies",

    # Construction
    "Construction Management",
    "Architecture",
    "Urban Planning",

    # General
    "Bachelor of",
    "Master of"
]


def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_text_from_docx(file):
    document = Document(file)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )


def extract_resume_text(file):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    if filename.endswith(".docx"):
        return extract_text_from_docx(file)

    raise ValueError("Unsupported file format")


def extract_email(text):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else ""


def extract_phone(text):
    cleaned_text = text.replace(" ", "")

    match = re.search(
        r"(\+61|0)[2-9]\d{8}",
        cleaned_text
    )

    return match.group(0) if match else ""


def extract_name(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored_words = {
        "professional summary",
        "skills",
        "work experience",
        "education",
        "accomplishments"
    }

    possible_name_parts = []

    for line in lines[:10]:
        clean_line = line.strip()

        if clean_line.lower() in ignored_words:
            continue

        if "@" in clean_line:
            continue

        if re.search(r"\d", clean_line):
            continue

        if len(clean_line.split()) > 3:
            continue

        if clean_line.replace(" ", "").isalpha():
            possible_name_parts.append(clean_line)

        if len(possible_name_parts) == 2:
            break

    if len(possible_name_parts) >= 2:
        return f"{possible_name_parts[0].title()} {possible_name_parts[1].title()}"

    if possible_name_parts:
        return possible_name_parts[0].title()

    return ""


def extract_education(text):
    lower_text = text.lower()

    if "bachelor of" in lower_text:
        return "Bachelor's Degree"

    if "master of" in lower_text:
        return "Master's Degree"

    if "diploma" in lower_text:
        return "Diploma"

    if "hsc" in lower_text:
        return "High School"

    for education in EDUCATION_KEYWORDS:
        if education.lower() in lower_text:
            return education

    return ""


def extract_major(text):
    lower_text = text.lower()
    matched_majors = []

    for major in MAJOR_KEYWORDS:
        if major.lower() in lower_text:
            matched_majors.append(major)

    if "big data" in lower_text and "ai" in lower_text:
        return "Big Data and AI"

    if matched_majors:

    
        unique_majors = []

        for major in matched_majors:
            if major not in unique_majors:
                unique_majors.append(major)

        return ", ".join(unique_majors[:3])

    return ""


def extract_skills(text):
    lower_text = text.lower()
    matched_skills = []

    for skill in KNOWN_SKILLS:
        if skill.lower() in lower_text:
            matched_skills.append(skill)

    return matched_skills


def estimate_experience_years(text):
    lower_text = text.lower()

    current_year_matches = re.findall(
        r"(\d{2}/\d{4}|\d{4})\s*[-–]\s*(current|present)",
        lower_text
    )

    if current_year_matches:
        return 2

    year_ranges = re.findall(
        r"(\d{4})\s*[-–]\s*(\d{4})",
        lower_text
    )

    total_years = 0

    for start, end in year_ranges:
        start_year = int(start)
        end_year = int(end)

        if end_year >= start_year:
            total_years += end_year - start_year

    if total_years > 0:
        return min(total_years, 10)

    return 0


def parse_resume(file):
    text = extract_resume_text(file)

    email = extract_email(text)
    phone = extract_phone(text)

    return {
        "name": extract_name(text),
        "email": email,
        "phone": phone,
        "contact": phone or email,
        "education": extract_education(text),
        "major": extract_major(text),
        "skills": extract_skills(text),
        "experience": estimate_experience_years(text),
        "raw_text": text[:5000]
    }