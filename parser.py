import sqlite3
import pymupdf
import re

def extract_text_from_pdf(pdf_path):
    try:
        with pymupdf.open(pdf_path) as doc:
            return "".join(page.get_text() for page in doc)
    except Exception as e:
        return f"Hata oluştu: {e}"

# Canonical skill name -> regex alternatives (names and common aliases).
# (?<![\w.]) keeps "js" inside "Node.js" or "React.js" from counting as JavaScript.
SKILL_PATTERNS = {
    "Python": [r"\bPython\d*\b"],
    "SQL": [r"\bSQL\b"],
    "React": [r"\bReact\d*\b", r"\bReact\.?js\b"],
    "JavaScript": [r"\bJavaScript\b", r"(?<![\w.])JS\b"],
    "C#": [r"\bC#", r"\bC-?Sharp\b"],
    "C++": [r"\bC\s?\+\s?\+", r"\bCPP\b"],
    "Java": [r"\bJava\d*\b"],
    "Docker": [r"\bDocker\b"],
    "Git": [r"\bGit\b"],
    "HTML": [r"\bHTML\d*\b"],
    "CSS": [r"\bCSS\d*\b"],
    "Node.js": [r"\bNode\.?\s?js\b"],
    "Django": [r"\bDjango\b"],
    "PostgreSQL": [r"\bPostgreSQL\b", r"\bPostgres\b"],
    "AWS": [r"\bAWS\b", r"\bAmazon Web Services\b"],
}

def find_skills(text):
    found_skills = []
    for skill, patterns in SKILL_PATTERNS.items():
        if any(re.search(p, text, re.IGNORECASE) for p in patterns):
            found_skills.append(skill)
    return found_skills

def calculate_match_score(user_skills, required_skills):
    if not required_skills:
        return 0
    matches = set(user_skills).intersection(set(required_skills))
    score = (len(matches) / len(required_skills)) * 100
    return round(score, 2)

def save_to_db(pdf_name, skills, score):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            skills TEXT,
            match_score REAL
        )
    ''')
    skills_str = ", ".join(skills)
    cursor.execute('''
        INSERT INTO candidates (name, skills, match_score)
        VALUES (?, ?, ?)
    ''', (pdf_name, skills_str, score))
    conn.commit()
    conn.close()
    print(f"Veritabanı güncellendi: {pdf_name} kaydedildi.")

if __name__ == "__main__":
    pdf_ismi = "sample_cv.pdf"
    is_ilani_kriterleri = ["Python", "React", "SQL", "Docker", "AWS", "C++"]

    print(f"--- {pdf_ismi} Analizi Başlıyor ---")

    raw_text = extract_text_from_pdf(pdf_ismi)

    if "Hata oluştu" not in raw_text:
        yetenekler = find_skills(raw_text)
        puan = calculate_match_score(yetenekler, is_ilani_kriterleri)
        save_to_db(pdf_ismi, yetenekler, puan)

        print(f"Senin Yeteneklerin: {yetenekler}")
        print(f"İş İlanı Kriterleri: {is_ilani_kriterleri}")
        print(f"--- UYUMLULUK PUANI: %{puan} ---")
    else:
        print(raw_text)
