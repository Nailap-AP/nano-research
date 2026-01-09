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
import warnings
warnings.filterwarnings('ignore')

# ===================== KONFIGURASI APLIKASI =====================
st.set_page_config(
    page_title="Nano Research - Kelompok 6 AKA Bogor",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CSS CUSTOM STYLING =====================
def local_css():
    st.markdown("""
    <style>
    /* Mode Toggle */
    .theme-toggle {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem 0;
    }
    
    .theme-btn {
        background: #FF8C42;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .theme-btn:hover {
        background: #FF6B21;
        transform: scale(1.05);
    }
    
    /* Header Styling - Jingga Muda */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF8C42 0%, #FFB347 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #FF8C42;
        font-weight: 600;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card Styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #FFE5D9;
        box-shadow: 0 4px 12px rgba(255, 140, 66, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(255, 140, 66, 0.2);
    }
    
    .info-card {
        background: linear-gradient(135deg, #FF8C42 0%, #FFB347 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #FF8C42 0%, #FFB347 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 140, 66, 0.3);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FF8C42 0%, #FF6B21 100%);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #FFF5EE;
        padding: 5px;
        border-radius: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
        color: #FF8C42;
        border: 1px solid #FFE5D9;
    }
    
    .stTabs [aria-selected="true"] {
        background: #FF8C42 !important;
        color: white !important;
        border-color: #FF8C42 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF8C42 0%, #FFB347 100%);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF8C42;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(255, 140, 66, 0.1);
    }
    
    /* Dark Mode */
    .dark-mode {
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
    }
    
    .dark-mode .feature-card {
        background: #2d2d2d;
        border-color: #444;
        color: #f0f0f0;
    }
    
    .dark-mode .metric-card {
        background: #2d2d2d;
        color: #f0f0f0;
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
        border-top: 1px solid #FFE5D9;
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
    
    /* Member Card */
    .member-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF8C42;
        box-shadow: 0 2px 8px rgba(255, 140, 66, 0.1);
    }
    
    .dark-mode .member-card {
        background: #2d2d2d;
        color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

# Panggil CSS
local_css()

# ===================== FUNGSI UTAMA =====================

def create_resume_pdf(resume_data):
    """Membuat file PDF dari data resume"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles dengan warna jingga
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#FF8C42'),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#FF8C42'),
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
    
    content = []
    
    # Header
    header_text = f"""
    <para alignment="center">
    <font size="12" color="#FF8C42"><b>NANO RESEARCH</b></font><br/>
    <font size="10">Politeknik AKA Bogor</font><br/>
    <font size="10">Tahun 2026</font>
    </para>
    """
    content.append(Paragraph(header_text, title_style))
    content.append(Spacer(1, 20))
    
    # Judul
    content.append(Paragraph(f"<b>RESUME PENELITIAN</b>", title_style))
    content.append(Spacer(1, 10))
    
    # Informasi Umum
    content.append(Paragraph("1. INFORMASI UMUM PENELITIAN", heading_style))
    info_table_data = [
        ["Judul Penelitian", resume_data.get('judul', '')],
        ["Peneliti", resume_data.get('peneliti', '')],
        ["NIM", resume_data.get('nim', '')],
        ["Tanggal", resume_data.get('tanggal', datetime.now().strftime("%d %B %Y"))],
        ["Pembimbing", resume_data.get('pembimbing', '')],
    ]
    
    info_table = Table(info_table_data, colWidths=[3*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFF5EE')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    content.append(info_table)
    content.append(Spacer(1, 15))
    
    # Konten lainnya
    sections = [
        ("2. LATAR BELAKANG", 'latar_belakang'),
        ("3. TUJUAN PENELITIAN", 'tujuan'),
        ("4. METODOLOGI", 'metodologi'),
        ("5. HASIL PENELITIAN", 'hasil'),
        ("6. KESIMPULAN", 'kesimpulan')
    ]
    
    for title, key in sections:
        if resume_data.get(key):
            content.append(Paragraph(title, heading_style))
            if key == 'tujuan':
                tujuan_items = resume_data[key].split('\n')
                for item in tujuan_items:
                    if item.strip():
                        content.append(Paragraph(f"• {item.strip()}", normal_style))
            else:
                content.append(Paragraph(resume_data[key], normal_style))
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
    Warna tema: Jingga Muda (#FF8C42)
    </font>
    </para>
    """
    content.append(Paragraph(footer_text, normal_style))
    
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
    
    # Plot data dengan warna jingga
    ax.scatter(x, y, color='#FF8C42', s=80, alpha=0.8, label='Data Aktual', 
               edgecolors='white', linewidth=1, zorder=3)
    ax.plot(x, y_pred, color='#FF6B21', linewidth=3, 
            label=f'y = {intercept:.4f} + {slope:.4f}x', zorder=2)
    
    # Confidence interval
    n = len(x)
    y_err = 1.96 * std_err * np.sqrt(1/n + (x - np.mean(x))**2 / np.sum((x - np.mean(x))**2))
    ax.fill_between(x, y_pred - y_err, y_pred + y_err, color='#FF8C42', 
                    alpha=0.2, label='95% CI', zorder=1)
    
    # Styling plot
    ax.grid(True, alpha=0.3, linestyle='--', zorder=0)
    ax.set_xlabel('Konsentrasi (X)', fontsize=12, fontweight='bold', color='#333')
    ax.set_ylabel('Respons (Y)', fontsize=12, fontweight='bold', color='#333')
    ax.set_title('Kurva Kalibrasi - Nano Research', fontsize=14, fontweight='bold', color='#FF8C42')
    ax.legend(loc='best')
    
    # Info statistik
    stats_text = f'y = {intercept:.4f} + {slope:.4f}x\nR² = {r_squared:.4f}\nn = {n}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='#FF8C42'))
    
    plt.tight_layout()
    
    # Plot interaktif dengan Plotly
    fig_interactive = go.Figure()
    
    fig_interactive.add_trace(go.Scatter(
        x=x, y=y, mode='markers',
        name='Data Aktual',
        marker=dict(size=10, color='#FF8C42'),
        hovertemplate='<b>X</b>: %{x:.4f}<br><b>Y</b>: %{y:.4f}<extra></extra>'
    ))
    
    fig_interactive.add_trace(go.Scatter(
        x=x, y=y_pred, mode='lines',
        name=f'Regresi: y = {intercept:.4f} + {slope:.4f}x',
        line=dict(color='#FF6B21', width=3),
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
    
    fig_interactive.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#FFE5D9')
    fig_interactive.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#FFE5D9')
    
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

        Peringatan! 
        Menu sidebar jangan ditutup
        
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mode Toggle
    col_theme1, col_theme2 = st.columns([1, 2])
    with col_theme1:
        st.markdown("")
    with col_theme2:
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
        
        if st.button("🌙 Mode Gelap" if not st.session_state.dark_mode else "☀️ Mode Terang", 
                    use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")

    # Menu Navigasi
    selected_page = st.radio(
        "📌 MENU UTAMA",
        ["🏠 Beranda", "📝 Resume Penelitian", "📈 Kurva Kalibrasi", "👥 Tentang Kami"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Tips
    with st.expander("💡 Tips Aplikasi"):
        st.info("""
        1. Gunakan Excel/CSV untuk memuat data banyak
        2. R² mendekati 1 = korelasi kuat
        3. Simpan hasil resume sebagai PDF
        """)
    
    st.markdown("---")
    
    # Footer Sidebar
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.8rem;">
        <p>Version 1.1.0</p>
        <p>© 2026 Kelompok 6 AKA Bogor</p>
    </div>
    """, unsafe_allow_html=True)

# ===================== HALAMAN BERANDA =====================
if selected_page == "🏠 Beranda":
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🔬 NANO RESEARCH</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Aplikasi Analisis Penelitian oleh Kelompok 6 AKA Bogor 2026</p>', unsafe_allow_html=True)
    
    # Mode Indikator
    if st.session_state.dark_mode:
        st.info("🌙 **Mode Gelap Aktif** - Tema warna gelap menyesuaikan mood malam")
    else:
        st.info("☀️ **Mode Terang Aktif** - Tema warna cerah untuk menyinari harimu!")
    
    # Hero Section
    col_hero1, col_hero2 = st.columns([2, 1])
    
    with col_hero1:
        st.markdown("""
        <div class="info-card">
        <h3 style="color: white; text-align: center;">Selamat Datang di Nano Research!</h3>
        <p style="color: white; text-align: center;">
        Platform mudah untuk analisis penelitian oleh Kelompok 6. 
        Dilengkapi dengan mode gelap/terang untuk kenyamanan visual.
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
            <p>Buat resume penelitian profesional dengan format standar akademik.</p>
            <ul>
            <li>Form terstruktur</li>
            <li>Export PDF berkualitas</li>
            <li>Auto-save progress</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
            <h4>🎨 Tema Dinamis</h4>
            <p>Switch antara mode terang dan gelap sesuai preferensi.</p>
            <ul>
            <li>Mode terang (default)</li>
            <li>Mode gelap</li>
            <li>Warna jingga muda</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col_f2:
            st.markdown("""
            <div class="feature-card">
            <h4>📈 Kurva Kalibrasi</h4>
            <p>Analisis regresi linear lengkap untuk data kalibrasi.</p>
            <ul>
            <li>Input Excel/CSV</li>
            <li>Statistik lengkap</li>
            <li>Grafik interaktif</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
            <h4>📁 Multi-Format</h4>
            <p>Support berbagai format file untuk kemudahan.</p>
            <ul>
            <li>Excel (.xlsx, .xls)</li>
            <li>CSV (.csv)</li>
            <li>PDF export</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🚀 Buat Resume Baru", use_container_width=True):
            selected_page = "📝 Resume Penelitian"
            st.rerun()
        
        if st.button("📊 Analisis Data", use_container_width=True):
            selected_page = "📈 Kurva Kalibrasi"
            st.rerun()

# ===================== HALAMAN RESUME PENELITIAN =====================
elif selected_page == "📝 Resume Penelitian":
    st.markdown('<h1 class="main-header">📝 Resume Penelitian</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Buat resume penelitian profesional dengan format standar</p>', unsafe_allow_html=True)
    
    # Progress Indicator
    if 'resume_progress' not in st.session_state:
        st.session_state.resume_progress = 0
    
    progress_bar = st.progress(st.session_state.resume_progress)
    
    # Step Navigation
    steps = ["📋 Informasi Dasar", "📝 Konten Penelitian", "📥 Preview & Download"]
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
                                      ["Penelitian Mandiri", "Proyek Kelompok"])
            
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
        
        st.markdown("### 📥 Preview & Download")
        
        if 'resume_data' in st.session_state and st.session_state.resume_data:
            col_preview, col_download = st.columns([2, 1])
            
            with col_preview:
                st.markdown("#### 📄 Preview Resume")
                
                data = st.session_state.resume_data
                
                with st.container():
                    st.markdown(f"""
                    <div style="background: {'#2d2d2d' if st.session_state.dark_mode else 'white'}; 
                                color: {'#f0f0f0' if st.session_state.dark_mode else '#333'};
                                padding: 2rem; border-radius: 10px; border: 1px solid #FF8C42; margin-bottom: 2rem;">
                    <h3 style="color: #FF8C42; text-align: center;">RESUME PENELITIAN</h3>
                    <hr style="border-color: #FF8C42;">
                    
                    <h4 style="color: #FF8C42;">📋 Informasi Penelitian</h4>
                    <p><strong>Judul:</strong> {data.get('judul', '')}</p>
                    <p><strong>Peneliti:</strong> {data.get('peneliti', '')} ({data.get('nim', '')})</p>
                    <p><strong>Pembimbing:</strong> {data.get('pembimbing', '')}</p>
                    <p><strong>Tanggal:</strong> {data.get('tanggal', '')}</p>
                    <p><strong>Kategori:</strong> {data.get('kategori', '')}</p>
                    
                    <h4 style="color: #FF8C42;">🎯 Tujuan Penelitian</h4>
                    <ul>
                    """, unsafe_allow_html=True)
                    
                    if data.get('tujuan'):
                        for item in data['tujuan'].split('\n'):
                            if item.strip():
                                st.markdown(f"<li>{item.strip()}</li>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    </ul>
                    
                    <h4 style="color: #FF8C42;">📊 Hasil Utama</h4>
                    <p>{data.get('hasil', '')[:200] + "..." if len(data.get('hasil', '')) > 200 else data.get('hasil', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
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
                            
                            with open(pdf_path, "rb") as f:
                                pdf_bytes = f.read()
                            
                            st.success("✅ PDF berhasil dibuat!")
                            
                            st.download_button(
                                label="📥 Download Resume PDF",
                                data=pdf_bytes,
                                file_name=f"resume_penelitian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                            
                            # PDF Preview
                            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                            st.markdown(pdf_display, unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"Error membuat PDF: {str(e)}")
                
                # Additional options
                st.markdown("---")
                st.markdown("#### 💾 Simpan Data")
                
                if st.button("🔄 Reset Form", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key.startswith('resume'):
                            del st.session_state[key]
                    st.success("Form berhasil direset!")
                    time.sleep(1)
                    st.rerun()
        
        else:
            st.warning("Silakan lengkapi form terlebih dahulu di langkah sebelumnya.")

# ===================== HALAMAN KURVA KALIBRASI =====================
elif selected_page == "📈 Kurva Kalibrasi":
    st.markdown('<h1 class="main-header">📈 Kurva Kalibrasi</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analisis regresi linear untuk kurva kalibrasi</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📥 Input Data", "📊 Analisis & Hasil"])
    
    with tab1:
        st.markdown("### 📥 Input Data Kalibrasi")
        
        input_method = st.radio(
            "Metode Input:",
            ["📝 Manual", "📁 Upload File", "🗃️ Contoh Data"],
            horizontal=True
        )
        
        if input_method == "📝 Manual":
            col_manual1, col_manual2 = st.columns(2)
            
            with col_manual1:
                st.markdown("#### Data X (Variabel Bebas)")
                x_input = st.text_area(
                    "Masukkan nilai X:",
                    value="0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
                    height=200,
                    help="Pisahkan dengan koma atau baris baru"
                )
            
            with col_manual2:
                st.markdown("#### Data Y (Variabel Terikat)")
                y_input = st.text_area(
                    "Masukkan nilai Y:",
                    value="0.05, 0.98, 2.1, 2.9, 4.2, 5.1, 6.0, 7.1, 8.2, 9.0, 10.1",
                    height=200,
                    help="Pisahkan dengan koma atau baris baru"
                )
            
            if st.button("📊 Analisis Data", type="primary", use_container_width=True):
                try:
                    x_data = [float(x.strip()) for x in x_input.replace('\n', ',').split(',') if x.strip()]
                    y_data = [float(y.strip()) for y in y_input.replace('\n', ',').split(',') if y.strip()]
                    
                    if len(x_data) != len(y_data):
                        st.error(f"Jumlah data tidak sama! X: {len(x_data)}, Y: {len(y_data)}")
                    elif len(x_data) < 2:
                        st.error("Minimal diperlukan 2 titik data untuk analisis!")
                    else:
                        st.session_state.x_data = x_data
                        st.session_state.y_data = y_data
                        st.success(f"✅ Data berhasil diparsing: {len(x_data)} titik data")
                        st.rerun()
                except ValueError:
                    st.error("Format data tidak valid! Pastikan hanya angka yang dimasukkan.")
        
        elif input_method == "📁 Upload File":
            st.markdown("#### Upload File Data")
            
            uploaded_file = st.file_uploader(
                "Pilih file Excel atau CSV",
                type=['csv', 'xlsx', 'xls'],
                help="Format: Excel (.xlsx, .xls) atau CSV (.csv)"
            )
            
            if uploaded_file is not None:
                try:
                    # Cek ekstensi file
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:  # Excel file
                        df = pd.read_excel(uploaded_file)
                    
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
                        
                        if st.button("📊 Load Data dari File", type="primary", use_container_width=True):
                            st.session_state.x_data = df[x_col].dropna().tolist()
                            st.session_state.y_data = df[y_col].dropna().tolist()
                            st.success(f"Data berhasil dimuat: {len(st.session_state.x_data)} titik")
                            st.rerun()
                    else:
                        st.error("File harus memiliki minimal 2 kolom!")
                except Exception as e:
                    st.error(f"Error membaca file: {str(e)}")
        
        else:  # Contoh Data
            st.markdown("#### 🗃️ Contoh Data Kalibrasi")
            
            dataset = st.selectbox(
                "Pilih contoh dataset:",
                ["Data Linear Sempurna", "Data dengan Noise Sedang", "Data Non-linear"]
            )
            
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
            
            with st.spinner("Menganalisis data..."):
                results = analyze_calibration_curve(x_data, y_data)
                
                col_results, col_plot = st.columns([1, 2])
                
                with col_results:
                    st.markdown("### 📊 Hasil Analisis")
                    
                    # Tampilkan statistik
                    metrics = [
                        ("Slope (Kemiringan)", f"{results['slope']:.6f}", "#FF8C42"),
                        ("Intercept", f"{results['intercept']:.6f}", "#FFB347"),
                        ("R² (Determinasi)", f"{results['r_squared']:.6f}", "#FF6B21"),
                        ("Koef. Korelasi (r)", f"{results['r_value']:.6f}", "#FF8C42"),
                        ("Std Error", f"{results['std_err']:.6f}", "#FFB347"),
                        ("Jumlah Data (n)", f"{results['n']}", "#FF6B21"),
                    ]
                    
                    for name, value, color in metrics:
                        st.markdown(f"""
                        <div class="metric-card">
                        <small style="color: {color};">{name}</small>
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
                    
                    # Prediksi
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
                        Warna Tema: Jingga Muda (#FF8C42)
                        
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

# ===================== HALAMAN ANGGOTA KELOMPOK =====================
else:
    st.markdown('<h1 class="main-header">👥 Anggota Kelompok 6</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Politeknik AKA Bogor - Tahun 2026</p>', unsafe_allow_html=True)
    
    # Informasi Kelompok
    col_info1, col_info2 = st.columns([2, 1])
    
    with col_info1:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 10px; border: 1px solid #FFE5D9;">
        <h3 style="color: #FF8C42;">🔬 Tentang Kelompok 6</h3>
        <p>Kelompok 6 terdiri dari 5 anggota yang mengembangkan aplikasi <strong>Nano Research</strong> 
        sebagai proyek mata kuliah Logika Pemrogramaman Komputer di Politeknik AKA Bogor tahun 2026.</p>
        
        <h4 style="color: #FF8C42;">🎯 Misi Kelompok</h4>
        <p>Mengembangkan aplikasi analisis penelitian yang mudah dengan fitur lengkap 
        untuk membantu mahasiswa dalam proses penelitian akademik.</p>
        
        <h4 style="color: #FF8C42;">✨ Keterangan Web</h4>
        <ul>
        <strong>Aplikasi berbasis web yang dirancang untuk membantu pengguna dalam menyusun resume laporan
        <strong>secara sistematis serta memfasilitasi pembuatan kurva kalibrasi secara otomatis, sehingga</strong>
        <strong>mendukung efisiensi analisis data dan penyusunan laporan ilmiah</strong>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        # Daftar Anggota dalam Card
        st.markdown("### 📋 Daftar Anggota")
        
        members = [
            "Dias Subarna",
            "Grhizzello Auricko Benedict Lamo", 
            "Liza Nurhalizah",
            "Naila Amanda Putri",
            "Yudho Pamungkas"
        ]
        
        for i, member in enumerate(members):
            st.markdown(f"""
            <div class="member-card">
            <h4 style="margin: 0; color: #FF8C42;">{member}</h4>
            <p style="margin: 0; font-size: 0.9rem; color: #666;">
            Anggota {i+1} - Kelompok 6
            </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Timeline Proyek
    st.markdown("---")
    st.markdown("### 📅 Timeline Pengembangan")
    
    timeline_data = {
        'Fase': ['Perencanaan', 'Pengembangan', 'Testing', 'Presentasi'],
        'Bulan': ['Des 2025', 'Des 2025', 'Jan 2026', '8 Jan 2026'],
        'Status': ['✓ Selesai', '✓ Selesai', '✓ Selesai', '🔄 Berjalan']
    }
    
    df_timeline = pd.DataFrame(timeline_data)
    st.dataframe(df_timeline, use_container_width=True, hide_index=True)

# ===================== FOOTER =====================
st.markdown("""
<div class="custom-footer">
<p>
🔬 <strong>Nano Research</strong> - Aplikasi Analisis Penelitian<br>
Dikembangkan oleh Kelompok 6 - Politeknik AKA Bogor © 2026<br>
<strong>Anggota:</strong> Dias Subarna • Grhizzello Auricko Benedict Lamo • Liza Nurhalizah • Naila Amanda Putri • Yudho Pamungkas<br>
<strong>Mode:</strong> {} • <strong>Version:</strong> 1.1.0
</p>
</div>
""".format("🌙 Gelap" if st.session_state.dark_mode else "☀️ Terang"), unsafe_allow_html=True)

# ===================== DARK MODE STYLING =====================
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #f0f0f0;
    }
    
    .st-emotion-cache-1y4p8pa {
        background-color: #2d2d2d;
    }
    
    .stDataFrame {
        background-color: #2d2d2d;
    }
    
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #f0f0f0;
        border-color: #444;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #2d2d2d;
        color: #f0f0f0;
        border-color: #444;
    }
    
    .stSelectbox > div > div > select {
        background-color: #2d2d2d;
        color: #f0f0f0;
        border-color: #444;
    }
    
    .stDateInput > div > div > input {
        background-color: #2d2d2d;
        color: #f0f0f0;
        border-color: #444;
    }
    
    .stNumberInput > div > div > input {
        background-color: #2d2d2d;
        color: #f0f0f0;
        border-color: #444;
    }
    </style>
    """, unsafe_allow_html=True)
