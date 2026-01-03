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
from reportlab.lib.units import inch, cm
import tempfile
import base64
from datetime import datetime
import json
import time
from PIL import Image as PILImage
import warnings
warnings.filterwarnings('ignore')

# ===================== KONFIGURASI APLIKASI =====================
st.set_page_config(
    page_title="Nano Research - Kelompok 6 AKA Bogor",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': """
        ## Nano Research v1.0
        Aplikasi Analisis Penelitian oleh Kelompok 6
        Politeknik AKA Bogor - Tahun 2026
        """
    }
)

# ===================== CSS CUSTOM STYLING =====================
def local_css():
    st.markdown("""
    <style>
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0066CC 0%, #00B3B3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #0066CC;
        font-weight: 600;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card Styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,102,204,0.2);
    }
    
    .info-card {
        background: linear-gradient(135deg, #0066CC 0%, #00B3B3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #0066CC 0%, #00B3B3 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 3px 10px rgba(0,102,204,0.3);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0066CC 0%, #004C99 100%);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F0F2F6;
        padding: 5px;
        border-radius: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
        color: #0066CC;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0066CC !important;
        color: white !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0066CC 0%, #00B3B3 100%);
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        padding: 1rem;
        border-radius: 5px;
        color: white;
        margin: 1rem 0;
    }
    
    /* Custom Radio Buttons */
    .stRadio > div {
        flex-direction: row;
        align-items: center;
    }
    
    .stRadio label {
        margin-right: 20px;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Footer */
    .custom-footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 1px solid #E0E0E0;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)

# Panggil CSS
local_css()

# ===================== FUNGSI UTAMA =====================

def create_resume_pdf(resume_data):
    """Membuat file PDF dari data resume"""
    # Buat file temporary
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name
    
    # Buat dokumen PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0066CC'),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#0066CC'),
        spaceBefore=10,
        spaceAfter=5
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=5
    )
    
    # Kumpulkan konten
    content = []
    
    # Header dengan watermark kelompok
    header_text = f"""
    <para alignment="center">
    <font size="12" color="#0066CC"><b>NANO RESEARCH</b></font><br/>
    <font size="10">Kelompok 6 - Politeknik AKA Bogor</font><br/>
    <font size="10">Tahun 2026</font>
    </para>
    """
    content.append(Paragraph(header_text, title_style))
    content.append(Spacer(1, 20))
    
    # Judul Penelitian
    content.append(Paragraph(f"<b>RESUME PENELITIAN</b>", title_style))
    content.append(Spacer(1, 10))
    
    # Informasi Umum
    content.append(Paragraph("1. INFORMASI UMUM PENELITIAN", heading_style))
    info_table_data = [
        ["Judul Penelitian", resume_data.get('judul', '')],
        ["Peneliti", resume_data.get('peneliti', '')],
        ["NIM", resume_data.get('nim', '')],
        ["Kelompok", "6 - AKA Bogor 2026"],
        ["Tanggal", resume_data.get('tanggal', datetime.now().strftime("%d %B %Y"))],
        ["Pembimbing", resume_data.get('pembimbing', '')],
    ]
    
    info_table = Table(info_table_data, colWidths=[3*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F8FF')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    content.append(info_table)
    content.append(Spacer(1, 15))
    
    # Latar Belakang
    if resume_data.get('latar_belakang'):
        content.append(Paragraph("2. LATAR BELAKANG", heading_style))
        content.append(Paragraph(resume_data['latar_belakang'], normal_style))
        content.append(Spacer(1, 10))
    
    # Tujuan
    if resume_data.get('tujuan'):
        content.append(Paragraph("3. TUJUAN PENELITIAN", heading_style))
        tujuan_items = resume_data['tujuan'].split('\n')
        for item in tujuan_items:
            if item.strip():
                content.append(Paragraph(f"• {item.strip()}", normal_style))
        content.append(Spacer(1, 10))
    
    # Metodologi
    if resume_data.get('metodologi'):
        content.append(Paragraph("4. METODOLOGI", heading_style))
        content.append(Paragraph(resume_data['metodologi'], normal_style))
        content.append(Spacer(1, 10))
    
    # Hasil
    if resume_data.get('hasil'):
        content.append(Paragraph("5. HASIL PENELITIAN", heading_style))
        content.append(Paragraph(resume_data['hasil'], normal_style))
        content.append(Spacer(1, 10))
    
    # Kesimpulan
    if resume_data.get('kesimpulan'):
        content.append(Paragraph("6. KESIMPULAN", heading_style))
        content.append(Paragraph(resume_data['kesimpulan'], normal_style))
        content.append(Spacer(1, 10))
    
    # Kata Kunci
    if resume_data.get('kata_kunci'):
        content.append(Paragraph(f"<b>Kata Kunci:</b> {resume_data['kata_kunci']}", normal_style))
    
    # Footer
    content.append(Spacer(1, 30))
    footer_text = """
    <para alignment="center">
    <font size="9" color="#666666">
    Generated by Nano Research App - Kelompok 6 AKA Bogor 2026<br/>
    https://github.com/kelompok6-aka/nano-research
    </font>
    </para>
    """
    content.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(content)
    return pdf_path

def analyze_calibration_curve(x_data, y_data):
    """Menganalisis kurva kalibrasi"""
    x = np.array(x_data)
    y = np.array(y_data)
    
    # Hitung regresi linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value ** 2
    
    # Prediksi Y
    y_pred = intercept + slope * x
    
    # Buat plot dengan matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot data
    ax.scatter(x, y, color='#0066CC', s=80, alpha=0.8, label='Data Aktual', edgecolors='white', linewidth=1)
    ax.plot(x, y_pred, color='#FF6B6B', linewidth=3, label=f'Regresi: y = {intercept:.4f} + {slope:.4f}x')
    
    # Plot confidence interval
    n = len(x)
    y_err = 1.96 * std_err * np.sqrt(1/n + (x - np.mean(x))**2 / np.sum((x - np.mean(x))**2))
    ax.fill_between(x, y_pred - y_err, y_pred + y_err, color='#FF6B6B', alpha=0.2, label='95% Confidence Interval')
    
    # Styling plot
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('Konsentrasi (X)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Respons (Y)', fontsize=12, fontweight='bold')
    ax.set_title('Kurva Kalibrasi - Nano Research', fontsize=14, fontweight='bold', color='#0066CC')
    ax.legend(loc='best')
    
    # Tambah informasi statistik di plot
    stats_text = f'y = {intercept:.4f} + {slope:.4f}x\nR² = {r_squared:.4f}\nn = {n}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    # Buat juga plot interaktif dengan Plotly
    fig_interactive = go.Figure()
    
    fig_interactive.add_trace(go.Scatter(
        x=x, y=y, mode='markers',
        name='Data Aktual',
        marker=dict(size=10, color='#0066CC'),
        hovertemplate='<b>X</b>: %{x:.4f}<br><b>Y</b>: %{y:.4f}<extra></extra>'
    ))
    
    fig_interactive.add_trace(go.Scatter(
        x=x, y=y_pred, mode='lines',
        name=f'Regresi: y = {intercept:.4f} + {slope:.4f}x',
        line=dict(color='#FF6B6B', width=3),
        hovertemplate='<b>Prediksi Y</b>: %{y:.4f}<extra></extra>'
    ))
    
    fig_interactive.update_layout(
        title='Kurva Kalibrasi - Nano Research',
        xaxis_title='Konsentrasi (X)',
        yaxis_title='Respons (Y)',
        hovermode='closest',
        plot_bgcolor='white',
        height=500,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    fig_interactive.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig_interactive.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'r_value': r_value,
        'std_err': std_err,
        'p_value': p_value,
        'n': n,
        'fig_matplotlib': fig,
        'fig_interactive': fig_interactive,
        'equation': f'y = {intercept:.4f} + {slope:.4f}x'
    }

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: white; font-size: 2rem;">🔬</h1>
        <h2 style="color: white; margin: 0;">NANO RESEARCH</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
        Kelompok 6<br>Politeknik AKA Bogor<br>Tahun 2026
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu Navigasi
    selected_page = st.radio(
        "📌 MENU UTAMA",
        ["🏠 Beranda", "📝 Resume Penelitian", "📈 Kurva Kalibrasi", "👥 Tentang Kami"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Informasi Quick Stats
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Analisis", "24", "+3")
    with col2:
        st.metric("Resume", "18", "+2")
    
    st.markdown("---")
    
    # Tips
    with st.expander("💡 Tips Cepat"):
        st.info("""
        1. Simpan data Anda secara berkala
        2. Gunakan format CSV untuk data banyak
        3. Periksa R² > 0.99 untuk akurasi tinggi
        4. Simpan hasil dalam PDF untuk laporan
        """)
    
    st.markdown("---")
    
    # Footer Sidebar
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.8rem;">
        <p>Version 1.0.0</p>
        <p>© 2026 Kelompok 6 AKA Bogor</p>
    </div>
    """, unsafe_allow_html=True)

# ===================== HALAMAN BERANDA =====================
if selected_page == "🏠 Beranda":
    # Header dengan animasi
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🔬 NANO RESEARCH</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Aplikasi Analisis Penelitian oleh Kelompok 6 AKA Bogor 2026</p>', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="info-card">
    <h3 style="color: white; text-align: center;">Selamat Datang di Nano Research!</h3>
    <p style="color: white; text-align: center;">
    Platform lengkap untuk analisis penelitian, pembuatan resume laporan, dan kurva kalibrasi.
    Dikembangkan khusus untuk mendukung penelitian di lingkungan akademik.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fitur Utama
    st.markdown("## ✨ Fitur Utama")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("""
        <div class="feature-card">
        <h4>📝 Resume Penelitian</h4>
        <p>Buat resume penelitian profesional dengan format standar. Export ke PDF dengan mudah.</p>
        <ul>
        <li>Form input terstruktur</li>
        <li>Template profesional</li>
        <li>Export PDF berkualitas</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>📊 Visualisasi Data</h4>
        <p>Grafik interaktif dengan Plotly. Zoom, pan, dan download gambar resolusi tinggi.</p>
        <ul>
        <li>Grafik interaktif</li>
        <li>Multiple format export</li>
        <li>Custom styling</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f2:
        st.markdown("""
        <div class="feature-card">
        <h4>📈 Kurva Kalibrasi</h4>
        <p>Analisis regresi linear lengkap. Hitung slope, intercept, R², dan statistik lainnya.</p>
        <ul>
        <li>Regresi linear</li>
        <li>Interval kepercayaan</li>
        <li>Analisis residual</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h4>📁 Manajemen Data</h4>
        <p>Input data manual atau upload file CSV. Simpan dan load data dengan mudah.</p>
        <ul>
        <li>Input manual/CSV</li>
        <li>Auto-save data</li>
        <li>Format standar</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Start Buttons
    st.markdown("---")
    st.markdown("## 🚀 Mulai Analisis")
    
    col_start1, col_start2, col_start3 = st.columns(3)
    with col_start1:
        if st.button("📝 Buat Resume Baru", use_container_width=True):
            st.session_state.page = "resume"
            st.rerun()
    with col_start2:
        if st.button("📈 Analisis Kurva", use_container_width=True):
            st.session_state.page = "kurva"
            st.rerun()
    with col_start3:
        if st.button("📚 Panduan Penggunaan", use_container_width=True):
            st.info("""
            ### Panduan Singkat:
            1. **Resume Penelitian**: Isi form, preview, download PDF
            2. **Kurva Kalibrasi**: Input data, analisis, simpan hasil
            3. **Data Management**: Simpan sebagai CSV atau PDF
            """)
    
    # Demo Preview
    st.markdown("---")
    st.markdown("## 📊 Preview Aplikasi")
    
    tab_demo1, tab_demo2 = st.tabs(["Demo Resume", "Demo Kurva"])
    
    with tab_demo1:
        st.image("https://via.placeholder.com/800x400/0066CC/FFFFFF?text=Preview+Resume+Penelitian", 
                caption="Tampilan Resume Penelitian")
    
    with tab_demo2:
        # Generate sample plot
        x_demo = np.linspace(0, 10, 20)
        y_demo = 2.5 * x_demo + 1.2 + np.random.normal(0, 0.5, 20)
        
        fig_demo, ax_demo = plt.subplots(figsize=(10, 4))
        ax_demo.scatter(x_demo, y_demo, color='#0066CC')
        
        slope, intercept = np.polyfit(x_demo, y_demo, 1)
        ax_demo.plot(x_demo, slope*x_demo + intercept, color='#FF6B6B')
        
        ax_demo.set_xlabel('Konsentrasi (X)')
        ax_demo.set_ylabel('Respons (Y)')
        ax_demo.set_title('Demo Kurva Kalibrasi')
        ax_demo.grid(True, alpha=0.3)
        
        st.pyplot(fig_demo)

# ===================== HALAMAN RESUME PENELITIAN =====================
elif selected_page == "📝 Resume Penelitian":
    st.markdown('<h1 class="main-header">📝 Resume Penelitian</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Buat resume penelitian profesional dengan format standar</p>', unsafe_allow_html=True)
    
    # Progress Indicator
    progress_value = st.session_state.get('resume_progress', 0)
    progress_bar = st.progress(progress_value)
    
    # Step Navigation
    steps = ["📋 Informasi Dasar", "📝 Konten Penelitian", "👁️ Preview & Download"]
    current_step = st.radio("", steps, horizontal=True, label_visibility="collapsed")
    
    if current_step == steps[0]:
        st.session_state.resume_progress = 33
        progress_bar.progress(33)
        
        st.markdown("### 📋 Informasi Dasar Penelitian")
        
        with st.form("basic_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Identitas Peneliti")
                judul = st.text_input("Judul Penelitian*", placeholder="Masukkan judul penelitian Anda")
                peneliti = st.text_input("Nama Peneliti*", placeholder="Nama lengkap peneliti")
                nim = st.text_input("NIM*", placeholder="Nomor Induk Mahasiswa")
                email = st.text_input("Email", placeholder="email@student.aka.ac.id")
            
            with col2:
                st.markdown("#### Informasi Penelitian")
                pembimbing = st.text_input("Pembimbing", placeholder="Nama pembimbing penelitian")
                tanggal = st.date_input("Tanggal Penelitian", datetime.now())
                kata_kunci = st.text_input("Kata Kunci (pisahkan dengan koma)", 
                                         placeholder="analisis, kalibrasi, penelitian, ...")
                kategori = st.selectbox("Kategori Penelitian", 
                                      ["Skripsi", "Tugas Akhir", "Penelitian Mandiri", "Proyek Kelompok"])
            
            submit_basic = st.form_submit_button("Simpan & Lanjut →", type="primary")
            
            if submit_basic:
                if judul and peneliti and nim:
                    st.session_state.resume_data = {
                        'judul': judul,
                        'peneliti': peneliti,
                        'nim': nim,
                        'email': email,
                        'pembimbing': pembimbing,
                        'tanggal': tanggal.strftime("%d %B %Y"),
                        'kata_kunci': kata_kunci,
                        'kategori': kategori
                    }
                    st.success("✅ Informasi dasar tersimpan!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Harap isi semua field yang wajib (*)")
    
    elif current_step == steps[1]:
        st.session_state.resume_progress = 66
        progress_bar.progress(66)
        
        st.markdown("### 📝 Konten Penelitian")
        
        # Inisialisasi session state jika belum ada
        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = {}
        
        with st.form("content_form"):
            # Latar Belakang
            st.markdown("#### Latar Belakang")
            latar_belakang = st.text_area(
                "Jelaskan latar belakang penelitian:",
                height=150,
                placeholder="Deskripsikan latar belakang, masalah penelitian, dan urgensi penelitian..."
            )
            
            # Tujuan
            st.markdown("#### Tujuan Penelitian")
            tujuan = st.text_area(
                "Tujuan penelitian (satu tujuan per baris):",
                height=150,
                placeholder="Tujuan 1: ...\nTujuan 2: ...\nTujuan 3: ...",
                help="Tuliskan tujuan spesifik penelitian Anda, satu per baris"
            )
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                # Metodologi
                st.markdown("#### Metodologi")
                metodologi = st.text_area(
                    "Metodologi penelitian:",
                    height=200,
                    placeholder="Jelaskan metode, alat, bahan, dan prosedur penelitian..."
                )
            
            with col_m2:
                # Hasil
                st.markdown("#### Hasil Penelitian")
                hasil = st.text_area(
                    "Hasil utama penelitian:",
                    height=200,
                    placeholder="Deskripsikan hasil utama yang diperoleh..."
                )
            
            # Kesimpulan
            st.markdown("#### Kesimpulan")
            kesimpulan = st.text_area(
                "Kesimpulan penelitian:",
                height=100,
                placeholder="Kesimpulan dari penelitian..."
            )
            
            submit_content = st.form_submit_button("Simpan & Preview →", type="primary")
            
            if submit_content:
                st.session_state.resume_data.update({
                    'latar_belakang': latar_belakang,
                    'tujuan': tujuan,
                    'metodologi': metodologi,
                    'hasil': hasil,
                    'kesimpulan': kesimpulan
                })
                st.success("✅ Konten penelitian tersimpan!")
                time.sleep(1)
                st.rerun()
    
    else:  # Step 3: Preview & Download
        st.session_state.resume_progress = 100
        progress_bar.progress(100)
        
        st.markdown("### 👁️ Preview & Download")
        
        if 'resume_data' in st.session_state and st.session_state.resume_data:
            col_preview, col_download = st.columns([2, 1])
            
            with col_preview:
                st.markdown("#### 📄 Preview Resume")
                
                # Display preview in a nice box
                data = st.session_state.resume_data
                
                with st.container():
                    st.markdown(f"""
                    <div style="background: white; padding: 2rem; border-radius: 10px; border: 1px solid #E0E0E0; margin-bottom: 2rem;">
                    <h3 style="color: #0066CC; text-align: center;">RESUME PENELITIAN</h3>
                    <hr>
                    
                    <h4>📋 Informasi Penelitian</h4>
                    <p><strong>Judul:</strong> {data.get('judul', '')}</p>
                    <p><strong>Peneliti:</strong> {data.get('peneliti', '')} ({data.get('nim', '')})</p>
                    <p><strong>Pembimbing:</strong> {data.get('pembimbing', '')}</p>
                    <p><strong>Tanggal:</strong> {data.get('tanggal', '')}</p>
                    <p><strong>Kategori:</strong> {data.get('kategori', '')}</p>
                    
                    <h4>🎯 Tujuan Penelitian</h4>
                    <ul>
                    """, unsafe_allow_html=True)
                    
                    if data.get('tujuan'):
                        for item in data['tujuan'].split('\n'):
                            if item.strip():
                                st.markdown(f"<li>{item.strip()}</li>", unsafe_allow_html=True)
                    
                    st.markdown("""
                    </ul>
                    
                    <h4>📊 Hasil Utama</h4>
                    <p>{}</p>
                    </div>
                    """.format(data.get('hasil', '')[:200] + "..." if len(data.get('hasil', '')) > 200 else data.get('hasil', '')), 
                    unsafe_allow_html=True)
            
            with col_download:
                st.markdown("#### 📥 Download Options")
                
                # Download settings
                include_header = st.checkbox("Include Header Kelompok", value=True)
                quality = st.select_slider("Kualitas PDF", ["Standard", "High"])
                
                # Generate PDF button
                if st.button("🖨️ Generate PDF", type="primary", use_container_width=True):
                    with st.spinner("Membuat PDF..."):
                        try:
                            pdf_path = create_resume_pdf(st.session_state.resume_data)
                            
                            # Read PDF file
                            with open(pdf_path, "rb") as f:
                                pdf_bytes = f.read()
                            
                            # Show success and download button
                            st.success("✅ PDF berhasil dibuat!")
                            
                            st.download_button(
                                label="📥 Download Resume PDF",
                                data=pdf_bytes,
                                file_name=f"resume_penelitian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                            
                            # Show preview
                            st.markdown("**Preview PDF:**")
                            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                            st.markdown(pdf_display, unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"Error membuat PDF: {str(e)}")
                
                # Additional options
                st.markdown("---")
                st.markdown("#### 💾 Simpan Data")
                
                if st.button("💾 Simpan sebagai JSON", use_container_width=True):
                    json_str = json.dumps(st.session_state.resume_data, indent=2)
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_str,
                        file_name="resume_data.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                if st.button("🔄 Reset Form", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key.startswith('resume'):
                            del st.session_state[key]
                    st.success("Form berhasil direset!")
                    time.sleep(1)
                    st.rerun()
        
        else:
            st.warning("Silakan lengkapi form terlebih dahulu di langkah sebelumnya.")
            if st.button("Kembali ke Form"):
                st.session_state.resume_progress = 0
                st.rerun()

# ===================== HALAMAN KURVA KALIBRASI =====================
elif selected_page == "📈 Kurva Kalibrasi":
    st.markdown('<h1 class="main-header">📈 Kurva Kalibrasi</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analisis regresi linear untuk kurva kalibrasi</p>', unsafe_allow_html=True)
    
    # Tab untuk input dan analisis
    tab1, tab2 = st.tabs(["📥 Input Data", "📊 Analisis & Hasil"])
    
    with tab1:
        st.markdown("### 📥 Input Data Kalibrasi")
        
        # Pilihan metode input
        input_method = st.radio(
            "Metode Input:",
            ["📝 Manual Entry", "📁 Upload CSV", "🎲 Contoh Data"],
            horizontal=True
        )
        
        if input_method == "📝 Manual Entry":
            col_manual1, col_manual2 = st.columns(2)
            
            with col_manual1:
                st.markdown("#### Data X (Konsentrasi)")
                x_input = st.text_area(
                    "Masukkan nilai X:",
                    value="0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
                    height=200,
                    help="Pisahkan dengan koma atau baris baru"
                )
            
            with col_manual2:
                st.markdown("#### Data Y (Respons)")
                y_input = st.text_area(
                    "Masukkan nilai Y:",
                    value="0.05, 0.98, 2.1, 2.9, 4.2, 5.1, 6.0, 7.1, 8.2, 9.0, 10.1",
                    height=200,
                    help="Pisahkan dengan koma atau baris baru"
                )
            
            if st.button("📊 Analisis Data", type="primary", use_container_width=True):
                try:
                    # Parse data
                    x_data = [float(x.strip()) for x in x_input.replace('\n', ',').split(',') if x.strip()]
                    y_data = [float(y.strip()) for y in y_input.replace('\n', ',').split(',') if y.strip()]
                    
                    if len(x_data) != len(y_data):
                        st.error(f"Jumlah data tidak sama! X: {len(x_data)}, Y: {len(y_data)}")
                    elif len(x_data) < 2:
                        st.error("Minimal diperlukan 2 titik data untuk analisis!")
                    else:
                        # Simpan ke session state
                        st.session_state.x_data = x_data
                        st.session_state.y_data = y_data
                        st.success(f"✅ Data berhasil diparsing: {len(x_data)} titik data")
                        st.rerun()
                except ValueError:
                    st.error("Format data tidak valid! Pastikan hanya angka yang dimasukkan.")
        
        elif input_method == "📁 Upload CSV":
            st.markdown("#### Upload File CSV")
            
            uploaded_file = st.file_uploader(
                "Pilih file CSV",
                type=['csv'],
                help="Format: Kolom pertama = X, Kolom kedua = Y"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success(f"✅ File berhasil dibaca: {len(df)} baris data")
                    
                    # Tampilkan preview
                    st.dataframe(df.head(), use_container_width=True)
                    
                    # Pilih kolom
                    if len(df.columns) >= 2:
                        col_select1, col_select2 = st.columns(2)
                        with col_select1:
                            x_col = st.selectbox("Pilih kolom untuk X", df.columns)
                        with col_select2:
                            y_col = st.selectbox("Pilih kolom untuk Y", df.columns)
                        
                        if st.button("📊 Load Data dari CSV", type="primary", use_container_width=True):
                            st.session_state.x_data = df[x_col].dropna().tolist()
                            st.session_state.y_data = df[y_col].dropna().tolist()
                            st.success(f"Data berhasil dimuat: {len(st.session_state.x_data)} titik")
                            st.rerun()
                    else:
                        st.error("File harus memiliki minimal 2 kolom!")
                except Exception as e:
                    st.error(f"Error membaca file: {str(e)}")
        
        else:  # Contoh Data
            st.markdown("#### 🎲 Contoh Data Kalibrasi")
            
            # Pilih contoh dataset
            dataset = st.selectbox(
                "Pilih contoh dataset:",
                ["Data Linear Sempurna", "Data dengan Noise Sedang", "Data Non-linear"]
            )
            
            # Generate contoh data
            np.random.seed(42)
            
            if dataset == "Data Linear Sempurna":
                x_example = np.linspace(0, 10, 11)
                y_example = 2.5 * x_example + 1.0
            elif dataset == "Data dengan Noise Sedang":
                x_example = np.linspace(0, 10, 15)
                y_example = 2.0 * x_example + 0.5 + np.random.normal(0, 0.3, 15)
            else:  # Non-linear
                x_example = np.linspace(0, 10, 20)
                y_example = 0.5 * x_example**2 + np.random.normal(0, 1, 20)
            
            # Tampilkan data
            df_example = pd.DataFrame({
                'X (Konsentrasi)': x_example,
                'Y (Respons)': y_example
            })
            
            st.dataframe(df_example, use_container_width=True)
            
            if st.button("📊 Gunakan Contoh Data", type="primary", use_container_width=True):
                st.session_state.x_data = x_example.tolist()
                st.session_state.y_data = y_example.tolist()
                st.success(f"Contoh data diterapkan: {len(x_example)} titik")
                st.rerun()
    
    with tab2:
        if 'x_data' in st.session_state and 'y_data' in st.session_state:
            x_data = st.session_state.x_data
            y_data = st.session_state.y_data
            
            # Lakukan analisis
            with st.spinner("Menganalisis data..."):
                results = analyze_calibration_curve(x_data, y_data)
                
                # Tampilkan hasil dalam dua kolom
                col_results, col_plot = st.columns([1, 2])
                
                with col_results:
                    st.markdown("### 📊 Hasil Analisis")
                    
                    # Tampilkan statistik dalam cards
                    metrics = [
                        ("Slope (Kemiringan)", f"{results['slope']:.6f}", "#4CAF50"),
                        ("Intercept", f"{results['intercept']:.6f}", "#2196F3"),
                        ("R² (Determinasi)", f"{results['r_squared']:.6f}", "#FF9800"),
                        ("Koef. Korelasi (r)", f"{results['r_value']:.6f}", "#9C27B0"),
                        ("Std Error", f"{results['std_err']:.6f}", "#F44336"),
                        ("Jumlah Data (n)", f"{results['n']}", "#607D8B"),
                    ]
                    
                    for name, value, color in metrics:
                        st.markdown(f"""
                        <div style="background: {color}10; border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; border-radius: 5px;">
                        <small style="color: #666;">{name}</small>
                        <h4 style="margin: 0; color: {color};">{value}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Interpretasi R²
                    st.markdown("#### 🎯 Interpretasi R²")
                    r2_val = results['r_squared']
                    if r2_val >= 0.99:
                        st.success(f"Sangat Baik! (R² = {r2_val:.4f})")
                    elif r2_val >= 0.95:
                        st.info(f"Baik (R² = {r2_val:.4f})")
                    elif r2_val >= 0.90:
                        st.warning(f"Cukup (R² = {r2_val:.4f})")
                    else:
                        st.error(f"Kurang Baik (R² = {r2_val:.4f})")
                    
                    st.progress(float(r2_val))
                    st.caption(f"{r2_val*100:.1f}% variasi Y dapat dijelaskan oleh X")
                    
                    # Prediksi nilai
                    st.markdown("#### 🔮 Prediksi Nilai")
                    col_pred1, col_pred2 = st.columns(2)
                    with col_pred1:
                        x_input = st.number_input("Masukkan nilai X", 
                                                value=float(np.mean(x_data)),
                                                step=0.1)
                    with col_pred2:
                        y_pred = results['intercept'] + results['slope'] * x_input
                        st.metric("Prediksi Y", f"{y_pred:.4f}")
                
                with col_plot:
                    st.markdown("### 📈 Grafik Kurva Kalibrasi")
                    
                    # Tampilkan plot interaktif
                    st.plotly_chart(results['fig_interactive'], use_container_width=True)
                    
                    # Tombol download
                    col_dl1, col_dl2, col_dl3 = st.columns(3)
                    with col_dl1:
                        # Save matplotlib figure
                        buf = io.BytesIO()
                        results['fig_matplotlib'].savefig(buf, format='png', dpi=300, bbox_inches='tight')
                        buf.seek(0)
                        
                        st.download_button(
                            label="📷 Download PNG",
                            data=buf,
                            file_name=f"kurva_kalibrasi_{datetime.now().strftime('%Y%m%d')}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    with col_dl2:
                        # Download data sebagai CSV
                        df_results = pd.DataFrame({
                            'X': x_data,
                            'Y': y_data,
                            'Y_Pred': results['intercept'] + results['slope'] * np.array(x_data)
                        })
                        csv = df_results.to_csv(index=False)
                        
                        st.download_button(
                            label="📊 Download CSV",
                            data=csv,
                            file_name=f"data_kalibrasi_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col_dl3:
                        # Download report
                        report_content = f"""
                        LAPORAN ANALISIS KURVA KALIBRASI
                        =================================
                        Tanggal: {datetime.now().strftime("%d %B %Y %H:%M:%S")}
                        Aplikasi: Nano Research - Kelompok 6 AKA Bogor
                        
                        HASIL ANALISIS:
                        - Persamaan: {results['equation']}
                        - Slope: {results['slope']:.6f}
                        - Intercept: {results['intercept']:.6f}
                        - R²: {results['r_squared']:.6f}
                        - Jumlah Data: {results['n']}
                        
                        DATA:
                        X, Y
                        """
                        for x, y in zip(x_data, y_data):
                            report_content += f"\n{x},{y}"
                        
                        st.download_button(
                            label="📄 Download Report",
                            data=report_content,
                            file_name=f"report_kalibrasi_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
            
            # Tampilkan data tabel
            st.markdown("### 📋 Data Kalibrasi")
            df_display = pd.DataFrame({
                'X (Konsentrasi)': x_data,
                'Y (Respons)': y_data,
                'Y Prediksi': results['intercept'] + results['slope'] * np.array(x_data),
                'Residual': np.array(y_data) - (results['intercept'] + results['slope'] * np.array(x_data))
            })
            
            st.dataframe(df_display.style.format({
                'X (Konsentrasi)': '{:.4f}',
                'Y (Respons)': '{:.4f}',
                'Y Prediksi': '{:.4f}',
                'Residual': '{:.4f}'
            }), use_container_width=True)
        
        else:
            st.info("👈 Silakan input data terlebih dahulu di tab Input Data")
            st.image("https://via.placeholder.com/600x300/0066CC/FFFFFF?text=Input+Data+untuk+Analisis", 
                    caption="Masukkan data untuk melihat analisis kurva kalibrasi")

# ===================== HALAMAN TENTANG KAMI =====================
else:
    st.markdown('<h1 class="main-header">👥 Tentang Kami</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Kelompok 6 - Politeknik AKA Bogor 2026</p>', unsafe_allow_html=True)
    
    col_about1, col_about2 = st.columns([2, 1])
    
    with col_about1:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 10px; border: 1px solid #E0E0E0;">
        <h3 style="color: #0066CC;">🔬 Nano Research</h3>
        <p>Aplikasi web ini dikembangkan oleh <strong>Kelompok 6</strong> dari <strong> Prodi D4 Politeknik AKA Bogor</strong> 
        sebagai bagian dari proyek mata kuliah Logika dan Pemrograman Komputer Tahun 2026.</p>
        
        <h4>🎯 Misi Kami</h4>
        <p>Menyediakan tools analisis penelitian yang mudah digunakan, akurat, dan profesional 
        untuk mendukung kegiatan akademik dan penelitian di lingkungan Politeknik AKA Bogor.</p>
        
        <h4>✨ Fitur Unggulan</h4>
        <ul>
        <li><strong>Resume Penelitian Profesional</strong> - Format standar untuk laporan penelitian</li>
        <li><strong>Analisis Kurva Kalibrasi</strong> - Regresi linear dengan statistik lengkap</li>
        <li><strong>User-Friendly Interface</strong> - Mudah digunakan bahkan untuk pemula</li>
        <li><strong>Export Multiple Format</strong> - PDF, CSV, PNG, dan lainnya</li>
        </ul>
        
        <h4>🛠️ Teknologi yang Digunakan</h4>
        <p>Aplikasi ini dibangun dengan:</p>
        <ul>
        <li><strong>Streamlit</strong> - Framework web aplikasi Python</li>
        <li><strong>Plotly & Matplotlib</strong> - Visualisasi data interaktif</li>
        <li><strong>Pandas & NumPy</strong> - Manipulasi dan analisis data</li>
        <li><strong>SciPy</strong> - Analisis statistik</li>
        <li><strong>ReportLab</strong> - Generasi PDF</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_about2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0066CC 0%, #00B3B3 100%); padding: 2rem; border-radius: 10px; color: white;">
        <h3 style="color: white;">👨‍🔬 Anggota Kelompok</h3>
        <ul style="color: white;">
        <li>Dias Subarna</li>
        <li>Grhizzello Auricko Benedict Lamo</li>
        <li>Liza Nurhalizah</li>
        <li>Naila Amanda Putri</li>
        <li>Yudho Pamungkas</li>
        </ul>
        
        <h4 style="color: white;">🏫 Institusi</h4>
        <p style="color: white;">Politeknik AKA Bogor<br>
        Tahun 2026<br>
        Program Studi: [Nama Program Studi]</p>
        
        <h4 style="color: white;">📞 Kontak</h4>
        <p style="color: white;">Email: kelompok6@aka.ac.id<br>
        GitHub: github.com/kelompok6-aka</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Timeline Pengembangan
    st.markdown("---")
    st.markdown("### 📅 Timeline Pengembangan")
    
    timeline_data = {
        'Fase': ['Perencanaan', 'Pengembangan', 'Testing', 'Deployment'],
        'Bulan': ['Jan 2026', 'Feb-Mar 2026', 'Apr 2026', 'Mei 2026'],
        'Status': ['✓ Selesai', '✓ Selesai', '🔄 Berjalan', '⏳ Menunggu']
    }
    
    df_timeline = pd.DataFrame(timeline_data)
    st.dataframe(df_timeline, use_container_width=True, hide_index=True)
    
    # GitHub Stats
    st.markdown("---")
    st.markdown("### 📊 Statistik Proyek")
    
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    with col_stats1:
        st.metric("Versi", "1.0.0")
    with col_stats2:
        st.metric("Commit", "42")
    with col_stats3:
        st.metric("Issues", "3")
    with col_stats4:
        st.metric("Stars", "⭐")

# ===================== FOOTER =====================
st.markdown("""
<div class="custom-footer">
<p>
🔬 <strong>Nano Research</strong> - Aplikasi Analisis Penelitian<br>
Dikembangkan oleh Kelompok 6 - Politeknik AKA Bogor © 2026<br>
<a href="https://github.com/kelompok6-aka/nano-research" style="color: #0066CC;">GitHub Repository</a> | 
<a href="#" style="color: #0066CC;">Documentation</a> | 
<a href="#" style="color: #0066CC;">Report Issue</a>
</p>
</div>
""", unsafe_allow_html=True)
