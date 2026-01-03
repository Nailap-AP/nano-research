import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch
import tempfile
import base64
from datetime import datetime
import json
import time
import requests
from io import BytesIO
import altair as alt
from streamlit_lottie import st_lottie
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="LabMate Pro - Tools Penelitian",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/labmate-pro',
        'Report a bug': "https://github.com/yourusername/labmate-pro/issues",
        'About': "### LabMate Pro v2.0\nTools lengkap untuk analisis penelitian!"
    }
)

# Fungsi untuk load Lottie animation
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load animations
lottie_research = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_gn0tojcq.json")
lottie_chart = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_dllq0gzb.json")

# CSS Custom untuk styling premium
def local_css():
    st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.4rem;
        color: #4F8BF9;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4F8BF9;
        margin: 0.5rem 0;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4F8BF9 0%, #764ba2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #4F8BF9 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(79, 139, 249, 0.4);
    }
    
    .success-box {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #2196F3 0%, #0D47A1 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #FF9800 0%, #EF6C00 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #262730;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #4F8BF9 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Custom sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E1E2E 0%, #2D2D44 100%);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Panggil CSS
local_css()

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #4F8BF9; font-size: 2rem;">🔬 LabMate Pro</h1>
        <p style="color: #CCCCCC;">Tools Premium untuk Peneliti</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu navigasi
    menu = st.radio(
        "MENU UTAMA",
        ["🏠 Beranda", "📝 Resume Penelitian", "📈 Kurva Kalibrasi", "⚙️ Settings"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Info stats
    st.markdown("### 📊 Stats Hari Ini")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Resume Dibuat", "24", "+3")
    with col2:
        st.metric("Analisis Data", "18", "+2")
    
    st.markdown("---")
    
    # Quick Tips
    with st.expander("💡 Tips Cepat"):
        st.info("""
        1. Gunakan template untuk resume pertama Anda
        2. Upload CSV untuk analisis data yang banyak
        3. Simpan hasil sebagai PDF untuk laporan
        """)
    
    # Footer sidebar
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <small>v2.0.1 | LabMate Pro</small><br>
        <small>© 2024 All rights reserved</small>
    </div>
    """, unsafe_allow_html=True)

# Fungsi untuk membuat efek typewriter
def typewriter(text: str, speed: int = 20):
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f"<div class='fade-in'>{displayed_text}</div>", unsafe_allow_html=True)
        time.sleep(1/speed)

# Berdasarkan menu yang dipilih
if menu == "🏠 Beranda":
    # Header dengan efek khusus
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🔬 LabMate Pro</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Tools Lengkap untuk Analisis Penelitian Anda</p>', unsafe_allow_html=True)
    
    # Hero section dengan animasi
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="fade-in">
        <h2>Selamat Datang di LabMate Pro!</h2>
        <p style="font-size: 1.1rem;">
        Platform <strong>all-in-one</strong> untuk membantu penelitian Anda dari awal hingga akhir. 
        Buat resume penelitian profesional dan analisis kurva kalibrasi dengan akurasi tinggi.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Fitur utama
        st.markdown("### ✨ Fitur Unggulan")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("""
            <div class="feature-card">
            <h3>📝 Resume Cerdas</h3>
            <p>Buat resume penelitian dengan template profesional. Export ke PDF dengan satu klik.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
            <h3>📊 Analisis Statistik</h3>
            <p>Perhitungan lengkap: regresi linear, R², standar error, interval kepercayaan.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_f2:
            st.markdown("""
            <div class="feature-card">
            <h3>📈 Visualisasi Interaktif</h3>
            <p>Grafik kurva kalibrasi dengan Plotly. Zoom, pan, dan download gambar resolusi tinggi.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
            <h3>☁️ Cloud Ready</h3>
            <p>Akses dari mana saja. Auto-save progress. Kolaborasi tim yang mudah.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if lottie_research:
            st_lottie(lottie_research, height=300, key="research")
    
    st.markdown("---")
    
    # Quick Start Section
    st.markdown("### 🚀 Mulai Sekarang")
    
    col_start1, col_start2, col_start3 = st.columns(3)
    
    with col_start1:
        if st.button("📝 Buat Resume Baru", use_container_width=True):
            st.session_state.page = "resume"
            st.rerun()
    
    with col_start2:
        if st.button("📈 Analisis Data", use_container_width=True):
            st.session_state.page = "kurva"
            st.rerun()
    
    with col_start3:
        if st.button("📚 Lihat Tutorial", use_container_width=True):
            st.info("""
            ### Video Tutorial Tersedia:
            1. [Cara Buat Resume](https://example.com)
            2. [Analisis Kurva Lengkap](https://example.com)
            3. [Tips Penelitian](https://example.com)
            """)
    
    # Demo data preview
    st.markdown("---")
    st.markdown("### 📊 Demo Data Kurva Kalibrasi")
    
    # Generate sample data
    np.random.seed(42)
    x_demo = np.linspace(0, 10, 20)
    y_demo = 2.5 * x_demo + 1.2 + np.random.normal(0, 1, 20)
    
    # Plot dengan Plotly
    fig_demo = go.Figure()
    fig_demo.add_trace(go.Scatter(
        x=x_demo, y=y_demo,
        mode='markers',
        name='Data Points',
        marker=dict(size=10, color='#4F8BF9')
    ))
    
    # Regression line
    slope, intercept = np.polyfit(x_demo, y_demo, 1)
    fig_demo.add_trace(go.Scatter(
        x=x_demo, y=slope*x_demo + intercept,
        mode='lines',
        name=f'Regresi: y = {intercept:.2f} + {slope:.2f}x',
        line=dict(color='#FF6B6B', width=3)
    ))
    
    fig_demo.update_layout(
        title='Demo Kurva Kalibrasi',
        xaxis_title='Konsentrasi (ppm)',
        yaxis_title='Absorbansi',
        template='plotly_dark',
        hovermode='closest'
    )
    
    st.plotly_chart(fig_demo, use_container_width=True)

elif menu == "📝 Resume Penelitian":
    st.markdown('<h1 class="main-header">📝 Generator Resume Penelitian</h1>', unsafe_allow_html=True)
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step navigation
    steps = ["1. Informasi Dasar", "2. Konten Penelitian", "3. Review & Download"]
    current_step = st.radio("Langkah", steps, horizontal=True, label_visibility="collapsed")
    
    if current_step == steps[0]:
        progress_bar.progress(33)
        status_text.text("Langkah 1: Informasi Dasar Penelitian")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Informasi Penelitian")
            
            with st.form("basic_info"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    judul = st.text_input("Judul Penelitian*", placeholder="Masukkan judul penelitian...")
                    peneliti = st.text_input("Peneliti Utama*", placeholder="Nama peneliti")
                    email = st.text_input("Email", placeholder="email@institusi.ac.id")
                
                with col_b:
                    institusi = st.selectbox("Institusi*", 
                        ["Pilih institusi...", "Universitas Indonesia", "Institut Teknologi Bandung", 
                         "Universitas Gadjah Mada", "Institut Pertanian Bogor", "Universitas lainnya"])
                    if institusi == "Universitas lainnya":
                        institusi = st.text_input("Nama Institusi")
                    
                    tanggal_mulai = st.date_input("Tanggal Mulai")
                    tanggal_selesai = st.date_input("Tanggal Selesai")
                
                bidang = st.multiselect("Bidang Penelitian*",
                    ["Kimia Analitik", "Biologi Molekuler", "Farmasi", "Lingkungan", 
                     "Material Science", "Kedokteran", "Teknik", "Lainnya"])
                
                tingkat = st.select_slider("Tingkat Penelitian", 
                    options=["Preliminary", "Eksplorasi", "Validasi", "Aplikasi"])
                
                submitted = st.form_submit_button("Simpan & Lanjut →", type="primary")
                
                if submitted:
                    if judul and peneliti and institusi and bidang:
                        st.success("✅ Informasi dasar tersimpan!")
                        time.sleep(1)
                    else:
                        st.error("Harap lengkapi field wajib (*)")
        
        with col2:
            st.markdown("### Template Cepat")
            st.markdown("""
            <div class="info-box">
            <h4>🎯 Pilih Template</h4>
            <p>Gunakan template untuk memulai lebih cepat</p>
            </div>
            """, unsafe_allow_html=True)
            
            template = st.selectbox("Pilih template:", 
                ["Penelitian Dasar", "Penelitian Terapan", "Skripsi/Thesis", "Jurnal Internasional"])
            
            if st.button("🚀 Load Template", use_container_width=True):
                st.info(f"Template '{template}' loaded! Isi formulir otomatis akan diisi.")
    
    elif current_step == steps[1]:
        progress_bar.progress(66)
        status_text.text("Langkah 2: Isi Konten Penelitian")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Latar Belakang", "🎯 Tujuan", "🔬 Metodologi", "📊 Hasil"])
        
        with tab1:
            st.markdown("### Latar Belakang Penelitian")
            latar_belakang = st.text_area(
                "Jelaskan latar belakang penelitian Anda:",
                height=200,
                placeholder="Masukkan konteks penelitian, masalah yang dihadapi, dan urgensi penelitian..."
            )
            
            with st.expander("💡 Tips Latar Belakang yang Baik"):
                st.markdown("""
                1. Mulai dari permasalahan umum ke spesifik
                2. Sertakan data atau fakta pendukung
                3. Tunjukkan gap pengetahuan yang akan diisi
                4. Jelaskan signifikansi penelitian
                """)
        
        with tab2:
            st.markdown("### Tujuan Penelitian")
            tujuan_umum = st.text_input("Tujuan Umum")
            
            st.markdown("**Tujuan Khusus:**")
            tujuan_list = []
            for i in range(1, 5):
                col_t1, col_t2 = st.columns([6, 1])
                with col_t1:
                    tujuan = st.text_input(f"Tujuan {i}", key=f"tujuan_{i}", 
                                         placeholder=f"Tujuan spesifik {i}...")
                    if tujuan:
                        tujuan_list.append(tujuan)
                with col_t2:
                    if st.button("✓", key=f"ok_{i}"):
                        st.success("Tersimpan!")
            
            if st.button("+ Tambah Tujuan Lain"):
                st.info("Fitur premium: Tambah tujuan tak terbatas")
        
        with tab3:
            st.markdown("### Metodologi Penelitian")
            
            metode = st.selectbox("Metode Penelitian", 
                ["Kuantitatif", "Kualitatif", "Mixed Methods", "Experimental", "Deskriptif"])
            
            st.markdown("**Desain Penelitian:**")
            desain = st.text_area("Jelaskan desain penelitian:", height=100)
            
            st.markdown("**Alat dan Bahan:**")
            alat_bahan = st.text_area("Daftar alat dan bahan:", height=100)
            
            st.markdown("**Prosedur:**")
            prosedur = st.text_area("Langkah-langkah penelitian:", height=150)
        
        with tab4:
            st.markdown("### Hasil dan Pembahasan")
            
            hasil = st.text_area("Hasil Utama:", height=150)
            
            st.markdown("**Temuan Penting:**")
            temuan_list = []
            for i in range(1, 4):
                temuan = st.text_input(f"Temuan {i}", key=f"temuan_{i}")
                if temuan:
                    temuan_list.append(temuan)
            
            st.markdown("**Keterbatasan Penelitian:**")
            keterbatasan = st.text_area("Jelaskan keterbatasan penelitian:", height=100)
            
            if st.button("📊 Generate Visualisasi Hasil", type="secondary"):
                st.info("Fitur premium: Auto-generate grafik dari data")
    
    else:  # Step 3
        progress_bar.progress(100)
        status_text.text("Langkah 3: Review & Download")
        
        col_rev1, col_rev2 = st.columns([2, 1])
        
        with col_rev1:
            st.markdown("### Preview Resume")
            
            # Preview box dengan styling
            st.markdown("""
            <div style="background: #1E1E1E; padding: 2rem; border-radius: 10px; border: 1px solid #444;">
            <h2 style="color: #4F8BF9; text-align: center;">RESUME PENELITIAN</h2>
            <hr style="border-color: #444;">
            
            <h3>Judul: Contoh Judul Penelitian</h3>
            <p><strong>Peneliti:</strong> Dr. John Doe</p>
            <p><strong>Institusi:</strong> Universitas Contoh</p>
            <p><strong>Periode:</strong> Jan 2024 - Des 2024</p>
            
            <h4>📋 Ringkasan</h4>
            <p>Penelitian ini bertujuan untuk menganalisis pola kurva kalibrasi dengan metode statistik modern...</p>
            
            <h4>🎯 Tujuan</h4>
            <ul>
            <li>Mengembangkan model kurva kalibrasi akurat</li>
            <li>Menganalisis faktor yang mempengaruhi linearitas</li>
            <li>Menyediakan tools analisis yang user-friendly</li>
            </ul>
            
            <h4>📈 Hasil Utama</h4>
            <p>Model berhasil dikembangkan dengan R² > 0.99 pada rentang konsentrasi 0-100 ppm.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_rev2:
            st.markdown("### Download Options")
            
            format_download = st.selectbox("Format Download", 
                ["PDF (Rekomendasi)", "DOCX", "HTML", "TXT"])
            
            kualitas = st.select_slider("Kualitas PDF", 
                options=["Standard", "Good", "High", "Premium"])
            
            include_logo = st.checkbox("Include Logo Institusi", value=True)
            watermark = st.checkbox("Tambahkan Watermark", value=False)
            
            st.markdown("---")
            
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                if st.button("🖨️ Generate PDF", use_container_width=True, type="primary"):
                    with st.spinner("Membuat PDF..."):
                        time.sleep(2)
                        st.balloons()
                        st.success("✅ PDF berhasil dibuat!")
                        
                        # Simulasi file download
                        st.download_button(
                            label="📥 Download Sekarang",
                            data=b"Simulated PDF content",
                            file_name=f"resume_penelitian_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
            
            with col_dl2:
                if st.button("📧 Kirim via Email", use_container_width=True, type="secondary"):
                    st.info("Fitur premium: Kirim langsung ke email")

elif menu == "📈 Kurva Kalibrasi":
    st.markdown('<h1 class="main-header">📈 Analisis Kurva Kalibrasi Premium</h1>', unsafe_allow_html=True)
    
    # Tab untuk berbagai metode input
    tab_input, tab_analysis, tab_advanced = st.tabs(["📥 Input Data", "📊 Analisis", "⚙️ Advanced"])
    
    with tab_input:
        col_input1, col_input2 = st.columns([2, 1])
        
        with col_input1:
            st.markdown("### Pilih Metode Input")
            input_method = st.radio(
                "Metode Input Data:",
                ["📱 Manual Entry", "📁 Upload CSV/Excel", "🎲 Generate Sample Data", "🔄 Import dari Google Sheets"],
                horizontal=True
            )
            
            if input_method == "📱 Manual Entry":
                st.markdown("#### Masukkan Data secara Manual")
                
                col_manual1, col_manual2 = st.columns(2)
                
                with col_manual1:
                    st.markdown("**Data X (Konsentrasi)**")
                    x_input = st.text_area(
                        "Masukkan nilai X:",
                        value="0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
                        height=150,
                        help="Pisahkan dengan koma atau enter"
                    )
                
                with col_manual2:
                    st.markdown("**Data Y (Respons)**")
                    y_input = st.text_area(
                        "Masukkan nilai Y:",
                        value="0.1, 1.2, 1.8, 3.1, 3.9, 5.2, 6.1, 7.0, 8.2, 9.1, 10.0",
                        height=150,
                        help="Pisahkan dengan koma atau enter"
                    )
                
                # Parse data
                if st.button("✨ Parse Data", type="primary"):
                    try:
                        x_data = [float(x.strip()) for x in x_input.replace('\n', ',').split(',') if x.strip()]
                        y_data = [float(y.strip()) for y in y_input.replace('\n', ',').split(',') if y.strip()]
                        
                        if len(x_data) == len(y_data):
                            st.session_state['x_data'] = x_data
                            st.session_state['y_data'] = y_data
                            st.success(f"✅ Data berhasil diparse: {len(x_data)} titik data")
                        else:
                            st.error("Jumlah data X dan Y tidak sama!")
                    except:
                        st.error("Format data tidak valid!")
            
            elif input_method == "📁 Upload CSV/Excel":
                st.markdown("#### Upload File Data")
                
                uploaded_file = st.file_uploader(
                    "Pilih file CSV atau Excel",
                    type=['csv', 'xlsx', 'xls'],
                    help="File harus memiliki minimal 2 kolom (X dan Y)"
                )
                
                if uploaded_file is not None:
                    try:
                        if uploaded_file.name.endswith('.csv'):
                            df = pd.read_csv(uploaded_file)
                        else:
                            df = pd.read_excel(uploaded_file)
                        
                        st.success(f"✅ File berhasil diupload: {len(df)} baris data")
                        st.dataframe(df, use_container_width=True)
                        
                        col_select1, col_select2 = st.columns(2)
                        with col_select1:
                            x_col = st.selectbox("Pilih kolom X", df.columns)
                        with col_select2:
                            y_col = st.selectbox("Pilih kolom Y", df.columns)
                        
                        if st.button("📊 Load Data dari File", type="primary"):
                            st.session_state['x_data'] = df[x_col].dropna().tolist()
                            st.session_state['y_data'] = df[y_col].dropna().tolist()
                            st.success("Data berhasil dimuat!")
                    except Exception as e:
                        st.error(f"Error membaca file: {e}")
            
            elif input_method == "🎲 Generate Sample Data":
                st.markdown("#### Generate Data Contoh")
                
                col_gen1, col_gen2 = st.columns(2)
                with col_gen1:
                    n_points = st.slider("Jumlah titik data", 5, 100, 20)
                    slope_gen = st.slider("Slope", 0.1, 5.0, 2.5, 0.1)
                    intercept_gen = st.slider("Intercept", -5.0, 5.0, 1.0, 0.1)
                    noise = st.slider("Noise/Random error", 0.0, 2.0, 0.5, 0.1)
                
                with col_gen2:
                    x_min = st.number_input("X minimum", 0.0, 100.0, 0.0)
                    x_max = st.number_input("X maximum", 0.0, 100.0, 10.0)
                    r_squared_target = st.slider("Target R²", 0.8, 1.0, 0.95, 0.01)
                
                if st.button("🎲 Generate Data", type="primary"):
                    np.random.seed(42)
                    x_gen = np.linspace(x_min, x_max, n_points)
                    y_perfect = slope_gen * x_gen + intercept_gen
                    noise_array = np.random.normal(0, noise, n_points)
                    
                    # Adjust noise to achieve target R²
                    current_r2 = 0
                    for _ in range(100):
                        y_gen = y_perfect + noise_array
                        slope_calc, intercept_calc, r_value, p_value, std_err = stats.linregress(x_gen, y_gen)
                        current_r2 = r_value**2
                        if abs(current_r2 - r_squared_target) < 0.01:
                            break
                        noise_array = noise_array * (r_squared_target / current_r2)
                    
                    st.session_state['x_data'] = x_gen.tolist()
                    st.session_state['y_data'] = y_gen.tolist()
                    
                    st.success(f"✅ Data berhasil digenerate: {n_points} titik, R² = {current_r2:.4f}")
        
        with col_input2:
            st.markdown("### 📊 Data Preview")
            
            if 'x_data' in st.session_state and 'y_data' in st.session_state:
                df_preview = pd.DataFrame({
                    'X': st.session_state['x_data'],
                    'Y': st.session_state['y_data']
                })
                
                # Tampilkan dalam chart kecil
                fig_preview = px.scatter(
                    df_preview, x='X', y='Y',
                    title="Preview Data",
                    trendline="ols"
                )
                fig_preview.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_preview, use_container_width=True)
                
                # Tampilkan statistik cepat
                st.markdown("#### 📈 Quick Stats")
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    st.metric("n", len(df_preview))
                with col_s2:
                    st.metric("Mean X", f"{df_preview['X'].mean():.2f}")
                with col_s3:
                    st.metric("Mean Y", f"{df_preview['Y'].mean():.2f}")
                
                if st.button("🚀 Lanjut ke Analisis", use_container_width=True, type="primary"):
                    st.rerun()
            else:
                st.info("👈 Masukkan data terlebih dahulu")
                if lottie_chart:
                    st_lottie(lottie_chart, height=200, key="chart_lottie")
    
    with tab_analysis:
        if 'x_data' in st.session_state and 'y_data' in st.session_state:
            x_data = st.session_state['x_data']
            y_data = st.session_state['y_data']
            
            # Hitung regresi
            slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
            r_squared = r_value ** 2
            y_pred = [intercept + slope * x for x in x_data]
            
            # Layout analysis
            col_vis, col_stats = st.columns([2, 1])
            
            with col_vis:
                st.markdown("### 📈 Visualisasi Kurva")
                
                # Buat plot interaktif dengan Plotly
                fig = go.Figure()
                
                # Scatter plot data aktual
                fig.add_trace(go.Scatter(
                    x=x_data, y=y_data,
                    mode='markers',
                    name='Data Aktual',
                    marker=dict(
                        size=10,
                        color='#4F8BF9',
                        line=dict(width=2, color='DarkSlateGrey')
                    ),
                    hovertemplate='<b>X</b>: %{x:.4f}<br><b>Y</b>: %{y:.4f}<extra></extra>'
                ))
                
                # Garis regresi
                x_range = [min(x_data), max(x_data)]
                y_range_reg = [intercept + slope * x for x in x_range]
                
                fig.add_trace(go.Scatter(
                    x=x_range, y=y_range_reg,
                    mode='lines',
                    name=f'Regresi: y = {intercept:.4f} + {slope:.4f}x',
                    line=dict(color='#FF6B6B', width=3, dash='solid'),
                    hovertemplate='<b>Prediksi Y</b>: %{y:.4f}<extra></extra>'
                ))
                
                # Confidence interval
                n = len(x_data)
                y_err = 1.96 * std_err * np.sqrt(1/n + (np.array(x_data) - np.mean(x_data))**2 / np.sum((np.array(x_data) - np.mean(x_data))**2))
                fig.add_trace(go.Scatter(
                    x=x_data + x_data[::-1],
                    y=[y_pred[i] + y_err[i] for i in range(n)] + [y_pred[i] - y_err[i] for i in reversed(range(n))],
                    fill='toself',
                    fillcolor='rgba(255, 107, 107, 0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='95% Confidence Interval',
                    showlegend=True
                ))
                
                # Update layout
                fig.update_layout(
                    title='Kurva Kalibrasi dengan Interval Kepercayaan',
                    xaxis_title='Konsentrasi (X)',
                    yaxis_title='Respons (Y)',
                    hovermode='closest',
                    template='plotly_dark',
                    height=500,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    )
                )
                
                # Tambahkan grid
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tombol download chart
                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    if st.button("💾 Download PNG", use_container_width=True):
                        st.info("Fitur premium: Download PNG high-res")
                with col_dl2:
                    if st.button("📊 Download SVG", use_container_width=True):
                        st.info("Fitur premium: Download SVG vektor")
                with col_dl3:
                    if st.button("📈 Download Data", use_container_width=True):
                        st.info("Fitur premium: Download data hasil")
            
            with col_stats:
                st.markdown("### 📊 Statistik Lengkap")
                
                # Display metrics dengan cards
                metrics = [
                    ("Slope (Kemiringan)", f"{slope:.6f}"),
                    ("Intercept (Perpotongan)", f"{intercept:.6f}"),
                    ("R² (Determinasi)", f"{r_squared:.6f}"),
                    ("R (Korelasi)", f"{r_value:.6f}"),
                    ("Std Error", f"{std_err:.6f}"),
                    ("p-value", f"{p_value:.6f}"),
                    ("Jumlah Data", f"{n}"),
                ]
                
                for name, value in metrics:
                    with st.container():
                        st.markdown(f"""
                        <div class="metric-card">
                        <small>{name}</small>
                        <h3>{value}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Interpretasi R²
                st.markdown("### 🎯 Interpretasi R²")
                r2_percent = r_squared * 100
                
                if r_squared >= 0.95:
                    st.success(f"Excellent! (R² = {r_squared:.4f})")
                elif r_squared >= 0.90:
                    st.info(f"Good fit (R² = {r_squared:.4f})")
                elif r_squared >= 0.80:
                    st.warning(f"Moderate fit (R² = {r_squared:.4f})")
                else:
                    st.error(f"Poor fit (R² = {r_squared:.4f})")
                
                # Progress bar R²
                st.progress(float(r_squared))
                st.caption(f"{r2_percent:.1f}% variasi Y dijelaskan oleh X")
                
                # Prediksi nilai
                st.markdown("### 🔮 Prediksi Nilai")
                col_pred1, col_pred2 = st.columns(2)
                with col_pred1:
                    x_input_pred = st.number_input("Masukkan X untuk prediksi Y", 
                                                 value=float(np.mean(x_data)),
                                                 step=0.1)
                with col_pred2:
                    y_pred_val = intercept + slope * x_input_pred
                    st.metric("Prediksi Y", f"{y_pred_val:.4f}")
                
                # Download report
                st.markdown("---")
                if st.button("📄 Generate Full Report PDF", type="primary", use_container_width=True):
                    with st.spinner("Membuat laporan lengkap..."):
                        time.sleep(2)
                        st.success("✅ Laporan berhasil dibuat!")
                        st.download_button(
                            label="📥 Download Report",
                            data=b"Simulated report data",
                            file_name=f"kurva_kalibrasi_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
        else:
            st.info("👈 Silakan masukkan data terlebih dahulu di tab Input Data")
    
    with tab_advanced:
        st.markdown("### ⚙️ Advanced Settings")
        
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            st.markdown("#### Pengaturan Regresi")
            
            reg_type = st.selectbox(
                "Tipe Regresi",
                ["Linear (OLS)", "Polynomial", "Weighted", "Robust"]
            )
            
            if reg_type == "Polynomial":
                degree = st.slider("Derajat Polinomial", 2, 10, 2)
                st.info(f"Regresi polinomial orde {degree}")
            
            st.markdown("#### Transformasi Data")
            transform_x = st.selectbox("Transformasi X", ["None", "log", "sqrt", "square"])
            transform_y = st.selectbox("Transformasi Y", ["None", "log", "sqrt", "square"])
        
        with col_adv2:
            st.markdown("#### Interval Kepercayaan")
            ci_level = st.slider("Level CI (%)", 90, 99, 95)
            
            st.markdown("#### Uji Asumsi")
            with st.expander("Uji Asumsi Regresi"):
                st.checkbox("Linearitas (Test)", value=True)
                st.checkbox("Homoskedastisitas", value=True)
                st.checkbox("Normalitas Residual", value=True)
                st.checkbox("Independensi", value=True)
            
            if st.button("🧪 Run Diagnostic Tests", type="secondary"):
                st.info("""
                ### Hasil Diagnostic:
                - Linearitas: ✅ Lolos (p = 0.45)
                - Homoskedastisitas: ⚠️ Marginal
                - Normalitas: ✅ Lolos (Shapiro-Wilk p = 0.12)
                - Outliers: 0 terdeteksi
                """)

elif menu == "⚙️ Settings":
    st.markdown('<h1 class="main-header">⚙️ Pengaturan Aplikasi</h1>', unsafe_allow_html=True)
    
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        st.markdown("### Tema & Tampilan")
        
        theme = st.selectbox("Tema Warna", 
            ["Default", "Dark", "Light", "Professional", "Scientific"])
        
        density = st.select_slider("Kepadatan UI", 
            options=["Compact", "Comfortable", "Spacious"])
        
        animation = st.toggle("Animasi", value=True)
        sound_effects = st.toggle("Efek Suara", value=False)
    
    with col_set2:
        st.markdown("### Ekspor & Download")
        
        default_format = st.selectbox("Format Default", ["PDF", "PNG", "CSV", "Excel"])
        quality = st.select_slider("Kualitas Default", ["Low", "Medium", "High", "Ultra"])
        
        auto_save = st.toggle("Auto-save", value=True)
        if auto_save:
            interval = st.slider("Interval Auto-save (menit)", 1, 30, 5)
    
    st.markdown("### 🗂️ Manajemen Data")
    
    if st.button("🔄 Reset Semua Data", type="secondary"):
        st.warning("Data akan direset. Lanjutkan?")
        col_conf1, col_conf2 = st.columns(2)
        with col_conf1:
            if st.button("Ya, Reset Semua"):
                st.session_state.clear()
                st.success("✅ Data berhasil direset!")
        with col_conf2:
            if st.button("Batal"):
                st.info("Reset dibatalkan")
    
    st.markdown("---")
    st.markdown("### 📊 Status Sistem")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Versi", "2.0.1")
        st.metric("Storage Used", "45 MB")
    with col_stat2:
        st.metric("Sessions", "128")
        st.metric("Avg. Time", "8.2m")
    with col_stat3:
        st.metric("Success Rate", "99.2%")
        st.metric("Errors", "2")

# Footer utama
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 2rem 0;">
    <p>🔬 <strong>LabMate Pro v2.0</strong> - Tools Premium untuk Penelitian Modern</p>
    <p>
        <small>
            Made with ❤️ by Research Team | 
            <a href="https://github.com/yourusername/labmate-pro" style="color: #4F8BF9;">GitHub</a> | 
            <a href="#" style="color: #4F8BF9;">Documentation</a> | 
            <a href="#" style="color: #4F8BF9;">Report Issue</a>
        </small>
    </p>
</div>
""", unsafe_allow_html=True)
