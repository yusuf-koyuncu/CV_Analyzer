# CV Analyzer: Full-Stack Aday Takip Sistemi 🚀

Bu proje, PDF formatındaki CV'leri analiz eden, içindeki yetenekleri çıkaran ve bir iş ilanıyla uyumluluk puanını hesaplayan full-stack bir uygulamadır.

## 🛠 Kullanılan Teknolojiler

-   **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python), SQLite, Regex-based Parser.
-   **Frontend:** [React](https://reactjs.org/) (JavaScript/CSS), Fetch API.
-   **Kütüphaneler:** PyPDF2 (PDF okuma), sqlite3 (Veritabanı).

## 📂 Proje Yapısı

```text
CV_Analyzer_Project/
├── cv-frontend/          # React Dashboard
├── parser.py             # CV Analiz Motoru (Regex & PDF)
├── main.py               # FastAPI Backend API
├── .gitignore            # Git dışlama dosyası
└── README.md             # Dokümantasyon
```

## 🚀 Kurulum ve Çalıştırma

### 1. Backend Hazırlığı

Öncelikle gerekli kütüphaneleri yükleyin:
```bash
pip install fastapi uvicorn PyPDF2
```

Ardından, CV analizi yapmak ve veritabanını doldurmak için parser'ı çalıştırın:
```bash
python parser.py
```

Son olarak API'yi ayağa kaldırın:
```bash
python -m uvicorn main:app --reload
```
API şu adreste çalışacaktır: `http://127.0.0.1:8000`

### 2. Frontend Hazırlığı

`cv-frontend` klasörüne gidin ve bağımlılıkları yükleyin:
```bash
cd cv-frontend
npm install
```

Uygulamayı başlatın:
```bash
npm start
```
Arayüz şu adreste açılacaktır: `http://localhost:3000`

## 📊 Özellikler
- **Akıllı Yetenek Tespiti:** Regex kullanarak "C++", "C#", "Python" gibi teknik yetenekleri hatasız algılar.
- **Uyumluluk Puanlama:** Adayın yeteneklerini iş ilanı kriterleriyle kıyaslar.
- **Canlı Dashboard:** Backend'den gelen verileri modern bir tablo arayüzünde gösterir.

---
Geliştiren: **Yusuf Koyuncu**
