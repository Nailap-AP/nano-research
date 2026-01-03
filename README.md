# Aplikasi Resume Penelitian & Kurva Kalibrasi

Aplikasi web untuk membantu peneliti dalam:
1. Membuat resume laporan penelitian yang dapat diunduh dalam format PDF
2. Menganalisis data kurva kalibrasi dengan perhitungan statistik lengkap

## Fitur Utama

### 1. Generator Resume Penelitian
- Form input untuk data penelitian
- Generate PDF dengan format profesional
- Download langsung hasil resume

### 2. Analisis Kurva Kalibrasi
- Input data manual atau upload file CSV
- Perhitungan regresi linear lengkap:
  - Slope (kemiringan)
  - Intercept (perpotongan)
  - Koefisien determinasi (R²)
  - Standard error
- Visualisasi grafik kurva kalibrasi
- Prediksi nilai Y dari X
- Download grafik hasil analisis

## Cara Menjalankan Aplikasi

### Lokal
1. Clone repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
