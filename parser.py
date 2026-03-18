import sqlite3
import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        return text
    except Exception as e:
        return f"Hata oluştu: {e}"

def find_skills(text):
    skills_database = [
        "Python", "SQL", "React", "JavaScript", "C#", r"C\+\+", "Java", 
        "Docker", "Git", "HTML", "CSS", "Node.js", "Django", "PostgreSQL", "AWS"
    ]
    
    found_skills = []
    for skill in skills_database:
        pattern = rf"\b{skill}\b" if skill[-1].isalnum() else rf"\b{skill}"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill.replace("\\", ""))
            
    return list(set(found_skills))

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
    pdf_ismi = "Yusuf_Koyuncu_CV.pdf" 
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
