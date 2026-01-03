import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
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

# ===================== INISIALISASI SESSION STATE =====================
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {}

if 'x_data' not in st.session_state:
    st.session_state.x_data = []

if 'y_data' not in st.session_state:
    st.session_state.y_data = []

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
def get_css_theme():
    if st.session_state.theme == 'dark':
        return """
        <style>
        /* Dark Theme */
        .stApp {
            background-color: #0E1117;
        }
        
        .main-header {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #4F8BF9 0%, #00B3B3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
            color: #4F8BF9;
            font-weight: 600;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .feature-card {
            background: #262730;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #444;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            margin: 1rem 0;
            transition: all 0.3s ease;
            color: white;
        }
        
        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(79,139,249,0.2);
        }
        
        .info-card {
            background: linear-gradient(135deg, #4F8BF9 0%, #00B3B3 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin: 1rem 0;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(90deg, #4F8BF9 0%, #00B3B3 100%);
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 3px 10px rgba(79,139,249,0.3);
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E1E2E 0%, #2D2D44 100%);
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: #262730;
            padding: 5px;
            border-radius: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: #1E1E2E;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: 600;
            color: #4F8BF9;
        }
        
        .stTabs [aria-selected="true"] {
            background: #4F8BF9 !important;
            color: white !important;
        }
        
        /* Custom Footer */
        .custom-footer {
            text-align: center;
            padding: 1rem;
            margin-top: 2rem;
            border-top: 1px solid #444;
            color: #888;
            font-size: 0.9rem;
        }
        </style>
        """
    else:
        return """
        <style>
        /* Light Theme */
        .stApp {
            background-color: #FFFFFF;
        }
        
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
        
        /* Custom Footer */
        .custom-footer {
            text-align: center;
            padding: 1rem;
            margin-top: 2rem;
            border-top: 1px solid #E0E0E0;
            color: #666;
            font-size: 0.9rem;
        }
        </style>
        """

# ===================== FUNGSI UTAMA =====================

def create_resume_pdf(resume_data):
    """Membuat file PDF dari data resume"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    
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
    
    content = []
    
    # Header
    header_text = f"""
    <para alignment="center">
    <font size="12" color="#0066CC"><b>NANO RESEARCH</b></font><br/>
    <font size="10">Kelompok 6 - Politeknik AKA Bogor</font><br/>
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
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value ** 2
    y_pred = intercept + slope * x
    
    # Buat plot dengan matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if st.session_state.theme == 'dark':
        plt.style.use('dark_background')
        color_point = '#4F8BF9'
        color_line = '#FF6B6B'
        bg_color = 'none'
    else:
        color_point = '#0066CC'
        color_line = '#FF6B6B'
        bg_color = 'white'
    
    ax.scatter(x, y, color=color_point, s=80, alpha=0.8, label='Data Aktual', 
               edgecolors='white' if st.session_state.theme == 'dark' else 'black', linewidth=1)
    ax.plot(x, y_pred, color=color_line, linewidth=3, label=f'Regresi: y = {intercept:.4f} + {slope:.4f}x')
    
    # Styling plot
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('Konsentrasi (X)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Respons (Y)', fontsize=12, fontweight='bold')
    ax.set_title('Kurva Kalibrasi - Nano Research', fontsize=14, fontweight='bold', 
                color=color_point if st.session_state.theme == 'light' else color_line)
    ax.legend(loc='best')
    ax.set_facecolor(bg_color)
    fig.patch.set_facecolor(bg_color)
    
    # Tambah informasi statistik
    stats_text = f'y = {intercept:.4f} + {slope:.4f}x\nR² = {r_squared:.4f}\nn = {len(x)}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='white' if st.session_state.theme == 'light' else '#2D2D44', 
                     alpha=0.8))
    
    plt.tight_layout()
    
    # Plot interaktif dengan Plotly
    if st.session_state.theme == 'dark':
        plot_template = 'plotly_dark'
        color_point_plotly = '#4F8BF9'
    else:
        plot_template = 'plotly_white'
        color_point_plotly = '#0066CC'
    
    fig_interactive = go.Figure()
    
    fig_interactive.add_trace(go.Scatter(
        x=x, y=y, mode='markers',
        name='Data Aktual',
        marker=dict(size=10, color=color_point_plotly),
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
        template=plot_template,
        height=500,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    fig_interactive.update_xaxes(showgrid=True, gridwidth=1, 
                                 gridcolor='lightgray' if st.session_state.theme == 'light' else '#444')
    fig_interactive.update_yaxes(showgrid=True, gridwidth=1, 
                                 gridcolor='lightgray' if st.session_state.theme == 'light' else '#444')
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'r_value': r_value,
        'std_err': std_err,
        'p_value': p_value,
        'n': len(x),
        'fig_matplotlib': fig,
        'fig_interactive': fig_interactive,
        'equation': f'y = {intercept:.4f} + {slope:.4f}x'
    }

# ===================== SIDEBAR =====================
with st.sidebar:
    # Toggle Theme
    col_theme1, col_theme2 = st.columns([3, 1])
    with col_theme1:
        st.markdown("### 🌓 Tema Aplikasi")
    with col_theme2:
        theme_toggle = st.toggle("", value=st.session_state.theme == 'dark', 
                                label_visibility="collapsed")
        if theme_toggle:
            st.session_state.theme = 'dark'
        else:
            st.session_state.theme = 'light'
    
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
        ["🏠 Beranda", "📝 Resume Penelitian", "📈 Kurva Kalibrasi", "👥 Anggota Kelompok"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Analisis", "24", "+3")
    with col2:
        st.metric("Resume", "18", "+2")
    
    st.markdown("---")
    
    # Quick Tips
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

# ===================== APLIKASI CSS =====================
st.markdown(get_css_theme(), unsafe_allow_html=True)

# ===================== HALAMAN BERANDA =====================
if selected_page == "🏠 Beranda":
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
    with col_start2:
        if st.button("📈 Analisis Kurva", use_container_width=True):
            st.session_state.page = "kurva"
    with col_start3:
        if st.button("👥 Lihat Anggota", use_container_width=True):
            st.session_state.page = "anggota"
    
    # Demo Preview
    st.markdown("---")
    st.markdown("## 📊 Preview Aplikasi")
    
    tab_demo1, tab_demo2 = st.tabs(["Demo Resume", "Demo Kurva"])
    
    with tab_demo1:
        st.markdown("""
        <div style="padding: 2rem; background-color: #f5f5f5; border-radius: 10px;">
        <h4 style="color: #0066CC;">Contoh Format Resume:</h4>
        <p><strong>Judul:</strong> Analisis Kurva Kalibrasi Metode Spektrofotometri</p>
        <p><strong>Peneliti:</strong> Dias Subarna</p>
        <p><strong>Tujuan:</strong> Menentukan linearitas metode analisis...</p>
        <p><strong>Hasil:</strong> R² = 0.998, menunjukkan hubungan linear yang baik...</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab_demo2:
        # Generate sample plot
        x_demo = np.linspace(0, 10, 20)
        y_demo = 2.5 * x_demo + 1.2 + np.random.normal(0, 0.5, 20)
        
        fig_demo, ax_demo = plt.subplots(figsize=(10, 4))
        
        if st.session_state.theme == 'dark':
            plt.style.use('dark_background')
            color_demo = '#4F8BF9'
        else:
            color_demo = '#0066CC'
        
        ax_demo.scatter(x_demo, y_demo, color=color_demo)
        
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
    
    # Step Navigation
    steps = ["📋 Informasi Dasar", "📝 Konten Penelitian", "👁️ Preview & Download"]
    current_step = st.radio("", steps, horizontal=True, label_visibility="collapsed")
    
    if current_step == steps[0]:
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
        st.markdown("### 📝 Konten Penelitian")
        
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
        st.markdown("### 👁️ Preview & Download")
        
        if 'resume_data' in st.session_state and st.session_state.resume_data:
            col_preview, col_download = st.columns([2, 1])
            
            with col_preview:
                st.markdown("#### 📄 Preview Resume")
                
                data = st.session_state.resume_data
                
                with st.container():
                    if st.session_state.theme == 'dark':
                        bg_color = "#262730"
                        text_color = "white"
                        border_color = "#444"
                    else:
                        bg_color = "white"
                        text_color = "black"
                        border_color = "#E0E0E0"
                    
                    st.markdown(f"""
                    <div style="background: {bg_color}; padding: 2rem; border-radius: 10px; border: 1px solid {border_color}; margin-bottom: 2rem; color: {text_color};">
                    <h3 style="color: #0066CC; text-align: center;">RESUME PENELITIAN</h3>
                    <hr style="border-color: {border_color}">
                    
                    <h4>📋 Informasi Penelitian</h4>
                    <p><strong>Judul:</strong> {data.get('judul', '')}</p>
                    <p><strong>Peneliti:</strong> {data.get('peneliti', '')} ({data.get('nim', '')})</p>
                    <p><strong>Pembimbing:</strong> {data.get('pembimbing', '')}</p>
                    <p><strong>Tanggal:</strong> {data.get('tanggal', '')}</p>
                    <p><strong>Kategori:</strong> {data.get('kategori', '')}</p>
                    
                    <h4>🎯 Tujuan Penelitian</h4>
                    """, unsafe_allow_html=True)
                    
                    if data.get('tujuan'):
                        for item in data['tujuan'].split('\n'):
                            if item.strip():
                                st.markdown(f"<li>{item.strip()}</li>", unsafe_allow_html=True)
                    
                    st.markdown("""
                    <h4>📊 Hasil Utama</h4>
                    <p>{}</p>
                    </div>
                    """.format(data.get('hasil', '')[:200] + "..." if len(data.get('hasil', '')) > 200 else data.get('hasil', '')), 
                    unsafe_allow_html=True)
            
            with col_download:
                st.markdown("#### 📥 Download Options")
                
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
        
        else:
            st.warning("Silakan lengkapi form terlebih dahulu di langkah sebelumnya.")

# ===================== HALAMAN KURVA KALIBRASI =====================
elif selected_page == "📈 Kurva Kalibrasi":
    st.markdown('<h1 class="main-header">📈 Kurva Kalibrasi</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analisis regresi linear untuk kurva kalibrasi</p>', unsafe_allow_html=True)
    
    # Tab untuk input dan analisis
    tab1, tab2 = st.tabs(["📥 Input Data", "📊 Analisis & Hasil"])
    
    with tab1:
        st.markdown("### 📥 Input Data Kalibrasi")
        
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
                    
                    st.dataframe(df.head(), use_container_width=True)
                    
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
        if 'x_data' in st.session_state and 'y_data' in st.session_state and len(st.session_state.x_data) > 0:
            x_data = st.session_state.x_data
            y_data = st.session_state.y_data
            
            with st.spinner("Menganalisis data..."):
                results = analyze_calibration_curve(x_data, y_data)
                
                col_results, col_plot = st.columns([1, 2])
                
                with col_results:
                    st.markdown("### 📊 Hasil Analisis")
                    
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
                        <small style="color: {'white' if st.session_state.theme == 'dark' else '#666'};">{name}</small>
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
                    
                    st.plotly_chart(results['fig_interactive'], use_container_width=True)
                    
                    # Tombol download
                    col_dl1, col_dl2, col_dl3 = st.columns(3)
                    with col_dl1:
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
        if st.session_state.theme == 'dark':
            card_bg = "#262730"
            card_border = "#444"
            text_color = "white"
        else:
            card_bg = "white"
            card_border = "#E0E0E0"
            text_color = "black"
        
        st.markdown(f"""
        <div style="background: {card_bg}; padding: 2rem; border-radius: 10px; border: 1px solid {card_border}; margin-bottom: 2rem; color: {text_color};">
        <h3 style="color: #0066CC;">🔬 Tentang Kelompok 6</h3>
        <p>Kelompok 6 terdiri dari 5 anggota mahasiswa <strong>Politeknik AKA Bogor</strong> yang mengembangkan 
        aplikasi Nano Research sebagai bagian dari proyek mata kuliah Tahun 2026.</p>
        
        <h4 style="color: #0066CC;">🎯 Misi Kelompok</h4>
        <p>Mengembangkan aplikasi analisis penelitian yang user-friendly, akurat, dan profesional 
        untuk mendukung kegiatan akademik di lingkungan Politeknik AKA Bogor.</p>
        
        <h4 style="color: #0066CC;">📚 Latar Belakang</h4>
        <p>Aplikasi ini dikembangkan dengan pendekatan <strong>Problem-Based Learning</strong> untuk 
        memecahkan permasalahan nyata dalam analisis data penelitian di laboratorium.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0066CC 0%, #00B3B3 100%); padding: 2rem; border-radius: 10px; color: white;">
        <h4 style="color: white;">🏫 Institusi</h4>
        <p style="color: white;"><strong>Politeknik AKA Bogor</strong></p>
        <p style="color: white;">Tahun: 2026<br>
        Program Studi: Analis Kimia<br>
        Kelas: [Kelas]</p>
        
        <h4 style="color: white;">📅 Timeline</h4>
        <p style="color: white;">• Perencanaan: Jan 2026<br>
        • Pengembangan: Feb-Mar 2026<br>
        • Testing: Apr 2026<br>
        • Presentasi: Mei 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Daftar Anggota
    st.markdown("## 👨‍🔬 Daftar Anggota Kelompok")
    
    # Data anggota
    anggota_data = [
        {
            "nama": "Dias Subarna",
        },
        {
            "nama": "Grhizzello Auricko Benedict Lamo",
        },
        {
            "nama": "Liza Nurhalizah",
        },
        {
            "nama": "Naila Amanda Putri",
        },
        {
            "nama": "Yudho Pamungkas",
        }
    ]
    
    # Tampilkan anggota dalam cards
    for i, anggota in enumerate(anggota_data):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.session_state.theme == 'dark':
                member_bg = "#1E1E2E"
                member_border = "#444"
                member_text = "white"
            else:
                member_bg = "#F8F9FA"
                member_border = "#E0E0E0"
                member_text = "black"
            
            st.markdown(f"""
            <div style="background: {member_bg}; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #0066CC; margin-bottom: 1rem; color: {member_text};">
            <h4 style="margin: 0; color: #0066CC;">{anggota['nama']}</h4>
            <p style="margin: 0.5rem 0; color: #666;">NIM: {anggota['nim']} | Peran: {anggota['peran']}</p>
            <p style="margin: 0.5rem 0;"><strong>Tugas:</strong> {anggota['tugas']}</p>
            <div style="margin-top: 1rem;">
            """, unsafe_allow_html=True)
            
            for skill in anggota['skills']:
                st.markdown(f'<span style="background: #0066CC; color: white; padding: 0.2rem 0.5rem; border-radius: 3px; margin-right: 0.5rem; font-size: 0.8rem;">{skill}</span>', unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        with col2:
            # Avatar placeholder
            avatar_color = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"][i % 5]
            st.markdown(f"""
            <div style="width: 80px; height: 80px; background: {avatar_color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
            <span style="font-size: 2rem; color: white;">{anggota['nama'][0]}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Kontribusi masing-masing
    st.markdown("---")
    st.markdown("## 📊 Distribusi Tugas")
    
    tugas_data = pd.DataFrame({
        'Area': ['Backend Development', 'Frontend Development', 'UI/UX Design', 
                'Testing & QA', 'Documentation', 'Deployment'],
        'Persentase': [25, 20, 15, 20, 10, 10]
    })
    
    fig_tugas = px.bar(tugas_data, x='Persentase', y='Area', orientation='h',
                      color='Persentase', color_continuous_scale='Blues',
                      title='Distribusi Tugas Kelompok')
    
    if st.session_state.theme == 'dark':
        fig_tugas.update_layout(template='plotly_dark')
    
    st.plotly_chart(fig_tugas, use_container_width=True)

# ===================== FOOTER =====================
st.markdown("""
<div class="custom-footer">
<p>
🔬 <strong>Nano Research</strong> - Aplikasi Analisis Penelitian<br>
Dikembangkan oleh Kelompok 6 - Politeknik AKA Bogor © 2026<br>
Anggota: Dias Subarna • Grhizzello Auricko • Liza Nurhalizah • Naila Amanda • Yudho Pamungkas
</p>
</div>
""", unsafe_allow_html=True)
