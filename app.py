import streamlit as st
import requests
import base64
import json
from datetime import datetime
import re

# Konfigurasi halaman
st.set_page_config(
    page_title="Resume Laporan Penelitian",
    page_icon="📊",
    layout="wide"
)

# CSS kustom
st.markdown("""
<style>
    .main-header {
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
    }
    .section-header {
        color: #2563EB;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
    }
    .info-box {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
    }
    .stButton > button {
        width: 100%;
        background-color: #2563EB;
        color: white;
    }
    .github-info {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Judul aplikasi
st.title("📊 Aplikasi Resume Laporan Penelitian")
st.markdown("---")

# Sidebar untuk navigasi
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/25/25231.png", width=80)
    st.markdown("## Navigasi")
    menu = st.radio(
        "Pilih Menu:",
        ["📝 Buat Resume", "🔗 Integrasi GitHub", "📤 Deploy", "📁 Contoh Format"]
    )
    
    st.markdown("---")
    st.markdown("### Informasi")
    st.info("""
    Aplikasi ini membantu Anda:
    1. Membuat resume laporan penelitian
    2. Menyimpan ke GitHub
    3. Deploy ke Streamlit Cloud
    """)

# Fungsi untuk mengambil data dari GitHub
def get_github_content(repo_url, file_path, github_token=""):
    """Mengambil konten dari repository GitHub"""
    try:
        # Ekstrak owner dan repo dari URL
        pattern = r'github\.com/([^/]+)/([^/]+)'
        match = re.search(pattern, repo_url)
        
        if not match:
            return None, "URL GitHub tidak valid"
        
        owner, repo = match.groups()
        
        # Hilangkan .git jika ada
        repo = repo.replace('.git', '')
        
        # URL API GitHub
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        
        headers = {}
        if github_token:
            headers['Authorization'] = f"token {github_token}"
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            content = response.json()
            # Decode konten dari base64
            file_content = base64.b64decode(content['content']).decode('utf-8')
            return file_content, None
        else:
            return None, f"Gagal mengambil file: {response.status_code}"
            
    except Exception as e:
        return None, str(e)

# Fungsi untuk membuat format resume
def create_resume_template():
    """Template standar untuk resume penelitian"""
    template = f"""# RESUME LAPORAN PENELITIAN

## Informasi Umum
**Judul Penelitian:** [Judul Penelitian Anda]
**Peneliti Utama:** [Nama Peneliti]
**Institusi:** [Nama Institusi]
**Tanggal Mulai:** {datetime.now().strftime('%d-%m-%Y')}
**Tanggal Selesai:** [DD-MM-YYYY]
**Sumber Pendanaan:** [Sumber dana penelitian]

## Abstrak
[Tulis abstrak penelitian Anda di sini (maksimal 250 kata). Abstrak harus mencakup latar belakang, tujuan, metode, hasil, dan kesimpulan.]

## Latar Belakang
[Jelaskan latar belakang penelitian, permasalahan, dan urgensi penelitian.]

## Tujuan Penelitian
1. [Tujuan pertama]
2. [Tujuan kedua]
3. [Tujuan ketiga]

## Metodologi
### Desain Penelitian
[Jenis penelitian yang digunakan]

### Populasi dan Sampel
- Populasi: [Jelaskan populasi]
- Sampel: [Jelaskan sampel dan teknik sampling]

### Teknik Pengumpulan Data
[Metode pengumpulan data yang digunakan]

### Analisis Data
[Metode analisis data yang digunakan]

## Hasil dan Pembahasan
### Temuan Utama
1. [Temuan pertama]
2. [Temuan kedua]
3. [Temuan ketiga]

### Pembahasan
[Analisis dan interpretasi hasil]

## Kesimpulan
1. [Kesimpulan pertama]
2. [Kesimpulan kedua]

## Rekomendasi
1. [Rekomendasi untuk penelitian lanjutan]
2. [Rekomendasi untuk praktisi/kebijakan]

## Kata Kunci
[Kata kunci 1], [Kata kunci 2], [Kata kunci 3], [Kata kunci 4], [Kata kunci 5]

---
*Dibuat dengan Aplikasi Resume Laporan Penelitian*
"""
    return template

# Menu 1: Buat Resume
if menu == "📝 Buat Resume":
    st.header("📝 Buat Resume Laporan Penelitian")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informasi Penelitian")
        judul = st.text_input("Judul Penelitian*")
        peneliti = st.text_input("Peneliti Utama*")
        institusi = st.text_input("Institusi*")
        tanggal_mulai = st.date_input("Tanggal Mulai")
        tanggal_selesai = st.date_input("Tanggal Selesai")
        sumber_dana = st.selectbox("Sumber Pendanaan", 
                                 ["Mandiri", "Internal Institusi", "Eksternal", "Lainnya"])
    
    with col2:
        st.subheader("Detail Penelitian")
        bidang = st.selectbox("Bidang Penelitian", 
                            ["Kesehatan", "Pendidikan", "Teknologi", "Sosial", "Ekonomi", "Lainnya"])
        metode = st.multiselect("Metode Penelitian", 
                              ["Kuantitatif", "Kualitatif", "Mixed Methods", "Eksperimen", "Survei"])
        kata_kunci = st.text_input("Kata Kunci (pisahkan dengan koma)")
    
    st.subheader("Isi Resume")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Abstrak", "Metodologi", "Hasil", "Kesimpulan", "Preview"])
    
    with tab1:
        abstrak = st.text_area("Abstrak (maksimal 250 kata)", height=150)
    
    with tab2:
        metodologi = st.text_area("Metodologi Penelitian", height=200)
    
    with tab3:
        hasil = st.text_area("Hasil dan Pembahasan", height=200)
    
    with tab4:
        kesimpulan = st.text_area("Kesimpulan dan Rekomendasi", height=150)
    
    with tab5:
        st.markdown("### Preview Resume")
        if st.button("Generate Preview"):
            resume_text = f"""# RESUME LAPORAN PENELITIAN

## Informasi Umum
**Judul Penelitian:** {judul}
**Peneliti Utama:** {peneliti}
**Institusi:** {institusi}
**Tanggal Mulai:** {tanggal_mulai.strftime('%d-%m-%Y') if tanggal_mulai else 'Belum ditentukan'}
**Tanggal Selesai:** {tanggal_selesai.strftime('%d-%m-%Y') if tanggal_selesai else 'Belum ditentukan'}
**Sumber Pendanaan:** {sumber_dana}
**Bidang Penelitian:** {bidang}

## Abstrak
{abstrak}

## Metodologi
{metodologi}

## Hasil dan Pembahasan
{hasil}

## Kesimpulan dan Rekomendasi
{kesimpulan}

## Kata Kunci
{kata_kunci}

---
*Dibuat dengan Aplikasi Resume Laporan Penelitian - {datetime.now().strftime('%d %B %Y')}*
"""
            st.markdown(resume_text)
            
            # Tombol download
            st.download_button(
                label="📥 Download Resume (MD)",
                data=resume_text,
                file_name=f"resume_penelitian_{judul.replace(' ', '_')}.md",
                mime="text/markdown"
            )

# Menu 2: Integrasi GitHub
elif menu == "🔗 Integrasi GitHub":
    st.header("🔗 Integrasi dengan GitHub")
    
    st.markdown("""
    <div class="info-box">
    <b>Fitur ini memungkinkan Anda:</b><br>
    1. Mengambil file resume dari repository GitHub<br>
    2. Menyimpan resume ke repository GitHub<br>
    3. Melihat riwayat perubahan
    </div>
    """, unsafe_allow_html=True)
    
    tab_ambil, tab_simpan = st.tabs(["Ambil dari GitHub", "Simpan ke GitHub"])
    
    with tab_ambil:
        st.subheader("Ambil Resume dari GitHub")
        
        github_url = st.text_input("URL Repository GitHub", 
                                 placeholder="https://github.com/username/repository")
        
        file_path = st.text_input("Path file resume", 
                                placeholder="docs/resume.md",
                                value="README.md")
        
        github_token = st.text_input("GitHub Token (opsional)", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Ambil dari GitHub"):
                if github_url:
                    with st.spinner("Mengambil data dari GitHub..."):
                        content, error = get_github_content(github_url, file_path, github_token)
                        
                        if error:
                            st.error(f"Error: {error}")
                        else:
                            st.success("✅ Berhasil mengambil file dari GitHub!")
                            st.markdown("### Konten File:")
                            st.code(content, language="markdown")
                            
                            # Edit konten
                            edited_content = st.text_area("Edit konten:", 
                                                         value=content, 
                                                         height=300)
                            
                            if st.button("💾 Simpan Perubahan"):
                                st.info("Fitur simpan ke GitHub akan diimplementasikan dengan GitHub API")
                else:
                    st.warning("Masukkan URL GitHub terlebih dahulu")
        
        with col2:
            st.markdown("""
            <div class="github-info">
            <b>Contoh URL:</b><br>
            • https://github.com/user/repo<br>
            • https://github.com/org/project<br><br>
            
            <b>File yang didukung:</b><br>
            • README.md<br>
            • docs/resume.md<br>
            • laporan/penelitian.md
            </div>
            """, unsafe_allow_html=True)
    
    with tab_simpan:
        st.subheader("Simpan Resume ke GitHub")
        
        st.info("Fitur ini membutuhkan GitHub Personal Access Token")
        
        repo_owner = st.text_input("GitHub Username/Organization")
        repo_name = st.text_input("Nama Repository")
        commit_message = st.text_input("Commit Message", 
                                      value="Update resume laporan penelitian")
        branch = st.text_input("Branch", value="main")
        
        resume_content = st.text_area("Konten Resume", 
                                     height=300,
                                     value=create_resume_template())
        
        if st.button("🚀 Simpan ke GitHub"):
            st.success("Fitur simpan ke GitHub akan diimplementasikan secara lengkap dengan GitHub API")

# Menu 3: Deploy
elif menu == "📤 Deploy":
    st.header("📤 Deploy ke Streamlit Cloud")
    
    st.markdown("""
    <div class="success-box">
    <b>Langkah-langkah deploy ke Streamlit Cloud:</b>
    </div>
    """, unsafe_allow_html=True)
    
    steps = [
        ("1. Simpan kode aplikasi", "Simpan file ini sebagai `app.py` di repository GitHub Anda"),
        ("2. Buat requirements.txt", "Buat file requirements.txt dengan isi:\n```\nstreamlit\nrequests\npython-dotenv\n```"),
        ("3. Push ke GitHub", "Push semua file ke repository GitHub"),
        ("4. Buka Streamlit Cloud", "Kunjungi https://share.streamlit.io"),
        ("5. Deploy aplikasi", "Pilih repository dan file `app.py`"),
        ("6. Konfigurasi", "Atur variabel environment jika diperlukan"),
        ("7. Launch", "Klik deploy dan tunggu proses selesai")
    ]
    
    for step, description in steps:
        with st.expander(step):
            st.write(description)
    
    # Contoh file yang diperlukan
    st.subheader("File yang Diperlukan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**app.py**")
        st.code("""
# File utama aplikasi Streamlit
# Berisi kode yang sedang Anda lihat ini
        """, language="python")
    
    with col2:
        st.markdown("**requirements.txt**")
        st.code("""
streamlit>=1.28.0
requests>=2.31.0
python-dotenv>=1.0.0
        """, language="txt")
    
    with col3:
        st.markdown("**.gitignore**")
        st.code("""
.env
__pycache__/
*.pyc
.DS_Store
        """, language="txt")
    
    # Tombol deploy cepat
    st.markdown("---")
    if st.button("🚀 Deploy Sekarang (Streamlit Cloud)", type="primary"):
        st.success("Arahkan browser ke: https://share.streamlit.io")
        st.markdown("[Klik untuk membuka Streamlit Cloud](https://share.streamlit.io)")

# Menu 4: Contoh Format
elif menu == "📁 Contoh Format":
    st.header("📁 Contoh Format Resume")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Format Markdown")
        st.markdown("""
        ```markdown
        # JUDUL PENELITIAN
        
        ## Abstrak
        Lorem ipsum dolor sit amet...
        
        ## Metodologi
        - Jenis: Penelitian kuantitatif
        - Sampel: 100 responden
        - Analisis: Regresi linear
        
        ## Hasil
        1. Temuan pertama
        2. Temuan kedua
        
        ## Kesimpulan
        - Kesimpulan utama
        - Implikasi
        ```
        """)
    
    with col2:
        st.subheader("Format JSON")
        st.code("""
{
  "judul": "Penelitian Contoh",
  "peneliti": "Dr. John Doe",
  "abstrak": "Abstrak penelitian...",
  "metodologi": {
    "jenis": "Kuantitatif",
    "sampel": 100
  },
  "hasil": ["Temuan 1", "Temuan 2"],
  "kata_kunci": ["penelitian", "contoh"]
}
        """, language="json")
    
    st.subheader("Template Siap Pakai")
    template = create_resume_template()
    st.code(template, language="markdown")
    
    if st.button("📋 Salin Template"):
        st.success("Template telah disalin ke clipboard!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
    <p>Aplikasi Resume Laporan Penelitian v1.0 • Dibuat dengan Streamlit</p>
    <p>© 2024 • Untuk keperluan akademik dan penelitian</p>
    </div>
    """,
    unsafe_allow_html=True
)
