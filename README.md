# 🔬 Nano Research - Aplikasi Analisis Penelitian

![Nano Research Banner](https://via.placeholder.com/800x200/0066CC/FFFFFF?text=NANO+RESEARCH+-+Kelompok+6+AKA+Bogor+2026)

Aplikasi web modern untuk analisis penelitian yang dikembangkan oleh **Kelompok 6 D4 Politeknik AKA Bogor Tahun 2026**.

## 🎯 Fitur Utama

### 📝 Resume Penelitian
- Form input terstruktur untuk data penelitian
- Preview resume dalam format profesional
- Export ke PDF dengan watermark kelompok
- Template standar penelitian akademik

### 📈 Kurva Kalibrasi
- Analisis regresi linear lengkap
- Perhitungan slope, intercept, R², dan statistik lainnya
- Grafik interaktif dengan Plotly
- Export hasil dalam multiple format (PNG, CSV, PDF)

### ✨ UI Modern
- Desain clean dan professional
- Warna khas Kelompok 6 (Biru AKA)
- Responsive untuk semua device
- User-friendly interface

## 🚀 Cara Menjalankan

### Deploy di Streamlit Cloud (Rekomendasi)
1. Fork repository ini ke GitHub Anda
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Login dengan akun GitHub
4. Klik "New app"
5. Pilih repository dan branch
6. Set Main file path ke `app.py`
7. Klik "Deploy"

### Jalankan Lokal
```bash
# Clone repository
git clone https://github.com/kelompok6-aka/nano-research.git
cd nano-research

# Install dependencies
pip install -r requirements.txt

# Run aplikasi
streamlit run app.py
