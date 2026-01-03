# 🔬 Nano Research - Aplikasi Analisis Penelitian Kelompok 6

![Nano Research Banner](https://via.placeholder.com/800x200/FF8C42/FFFFFF?text=NANO+RESEARCH+-+Kelompok+6+AKA+Bogor+2026)

Aplikasi web modern untuk analisis penelitian yang dikembangkan oleh **Kelompok 6 Politeknik AKA Bogor Tahun 2026**.

## 👥 Anggota Kelompok 6
1. **Dias Subarna** 
2. **Grhizzello Auricko Benedict Lamo** 
3. **Liza Nurhalizah** 
4. **Naila Amanda Putri** 
5. **Yudho Pamungkas** 

## 🎨 Fitur Utama

### 🎯 Tema Warna: Jingga Muda (#FF8C42)
- Warna primer: #FF8C42
- Warna sekunder: #FFB347
- Warna aksen: #FF6B21
- Background: #FFE5D9

### 🌙☀️ Mode Dark/Light
- **Mode Terang**: Tema cerah dengan aksen jingga
- **Mode Gelap**: Tema gelap dengan aksen jingga
- Toggle switch di sidebar

### 📝 Resume Penelitian
- Form input terstruktur
- Preview real-time
- Export ke PDF
- Template profesional

### 📈 Kurva Kalibrasi
- Analisis regresi linear lengkap
- Input data manual atau upload file
- **Format file support**: Excel (.xlsx, .xls), CSV (.csv)
- Grafik interaktif dengan Plotly
- Download hasil dalam berbagai format

## 🚀 Cara Deploy

### Deploy di Streamlit Cloud
1. Fork repository ini ke GitHub
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
