from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mesaj": "CV Analiz API'si Çalışıyor!"}

@app.get("/adaylar")
def get_candidates():
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    data = cursor.fetchall()
    conn.close()
    
    result = []
    for item in data:
        result.append({
            "id": item[0],
            "name": item[1],
            "skills": item[2],
            "score": item[3]
        })
    return result