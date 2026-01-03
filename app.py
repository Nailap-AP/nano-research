import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
import tempfile
import base64
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Resume Penelitian & Kurva Kalibrasi",
    page_icon="📊",
    layout="wide"
)

# Fungsi untuk membuat download link
def get_download_link(file_path, filename, link_text):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

# Fungsi untuk menghasilkan PDF resume
def generate_resume_pdf(data_resume):
    # Buat file PDF sementara
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name
    
    # Buat dokumen PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Buat style kustom
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
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
    
    # Konten PDF
    content = []
    
    # Judul
    content.append(Paragraph("RESUME LAPORAN PENELITIAN", title_style))
    content.append(Spacer(1, 10))
    
    # Informasi penelitian
    content.append(Paragraph("1. INFORMASI UMUM", heading_style))
    content.append(Paragraph(f"<b>Judul Penelitian:</b> {data_resume['judul']}", normal_style))
    content.append(Paragraph(f"<b>Peneliti:</b> {data_resume['peneliti']}", normal_style))
    content.append(Paragraph(f"<b>Institusi:</b> {data_resume['institusi']}", normal_style))
    content.append(Paragraph(f"<b>Tanggal:</b> {data_resume['tanggal']}", normal_style))
    content.append(Spacer(1, 10))
    
    # Latar Belakang
    content.append(Paragraph("2. LATAR BELAKANG", heading_style))
    content.append(Paragraph(data_resume['latar_belakang'], normal_style))
    content.append(Spacer(1, 10))
    
    # Tujuan
    content.append(Paragraph("3. TUJUAN PENELITIAN", heading_style))
    tujuan_items = data_resume['tujuan'].split('\n')
    for item in tujuan_items:
        if item.strip():
            content.append(Paragraph(f"• {item.strip()}", normal_style))
    content.append(Spacer(1, 10))
    
    # Metodologi
    content.append(Paragraph("4. METODOLOGI", heading_style))
    content.append(Paragraph(data_resume['metodologi'], normal_style))
    content.append(Spacer(1, 10))
    
    # Hasil Utama
    content.append(Paragraph("5. HASIL UTAMA", heading_style))
    content.append(Paragraph(data_resume['hasil'], normal_style))
    content.append(Spacer(1, 10))
    
    # Kesimpulan
    content.append(Paragraph("6. KESIMPULAN", heading_style))
    content.append(Paragraph(data_resume['kesimpulan'], normal_style))
    content.append(Spacer(1, 10))
    
    # Kata Kunci
    if data_resume['kata_kunci']:
        content.append(Paragraph(f"<b>Kata Kunci:</b> {data_resume['kata_kunci']}", normal_style))
    
    # Build PDF
    doc.build(content)
    
    return pdf_path

# Fungsi untuk analisis kurva kalibrasi
def analyze_calibration_curve(x_data, y_data):
    # Konversi ke numpy array
    x = np.array(x_data)
    y = np.array(y_data)
    
    # Hitung regresi linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Hitung prediksi y
    y_pred = intercept + slope * x
    
    # Hitung koefisien determinasi (R²)
    r_squared = r_value ** 2
    
    # Hitung standar error
    residuals = y - y_pred
    std_error = np.std(residuals, ddof=2)
    
    # Buat plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, color='blue', s=50, label='Data Aktual')
    ax.plot(x, y_pred, color='red', linewidth=2, label=f'Regresi: y = {intercept:.4f} + {slope:.4f}x')
    
    # Tambah grid dan label
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Konsentrasi (X)', fontsize=12)
    ax.set_ylabel('Respons (Y)', fontsize=12)
    ax.set_title('Kurva Kalibrasi', fontsize=14, fontweight='bold')
    ax.legend()
    
    # Tambah info statistik di plot
    text_str = f'Persamaan: y = {intercept:.4f} + {slope:.4f}x\nR² = {r_squared:.4f}\nn = {len(x)}'
    ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'r_value': r_value,
        'std_err': std_err,
        'std_error': std_error,
        'fig': fig
    }

# Fungsi utama
def main():
    st.title("📊 Aplikasi Resume Penelitian & Kurva Kalibrasi")
    st.markdown("""
    Aplikasi ini membantu Anda dalam:
    1. Membuat resume laporan penelitian yang dapat diunduh dalam format PDF
    2. Membuat kurva kalibrasi dengan perhitungan statistik lengkap
    """)
    
    # Buat tab untuk kedua fungsi
    tab1, tab2 = st.tabs(["📝 Generator Resume Penelitian", "📈 Analisis Kurva Kalibrasi"])
    
    # Tab 1: Generator Resume Penelitian
    with tab1:
        st.header("Generator Resume Laporan Penelitian")
        st.markdown("Isi form di bawah ini untuk membuat resume penelitian Anda.")
        
        with st.form("form_resume"):
            col1, col2 = st.columns(2)
            
            with col1:
                judul = st.text_input("Judul Penelitian*", placeholder="Masukkan judul penelitian Anda")
                peneliti = st.text_input("Nama Peneliti*", placeholder="Nama lengkap peneliti")
                institusi = st.text_input("Institusi*", placeholder="Nama institusi/universitas")
                tanggal = st.date_input("Tanggal Penelitian", value=datetime.now())
                kata_kunci = st.text_input("Kata Kunci (pisahkan dengan koma)", placeholder="analisis, metode, hasil, ...")
            
            with col2:
                latar_belakang = st.text_area("Latar Belakang*", 
                                              placeholder="Jelaskan latar belakang penelitian...",
                                              height=150)
                
                tujuan = st.text_area("Tujuan Penelitian* (satu tujuan per baris)", 
                                      placeholder="Tujuan 1: ...\nTujuan 2: ...",
                                      height=150)
            
            metodologi = st.text_area("Metodologi*", 
                                      placeholder="Jelaskan metodologi penelitian yang digunakan...",
                                      height=150)
            
            hasil = st.text_area("Hasil Utama*", 
                                 placeholder="Jelaskan hasil utama penelitian...",
                                 height=150)
            
            kesimpulan = st.text_area("Kesimpulan*", 
                                      placeholder="Jelaskan kesimpulan penelitian...",
                                      height=150)
            
            submitted = st.form_submit_button("📄 Generate Resume PDF")
            
            if submitted:
                if not all([judul, peneliti, institusi, latar_belakang, tujuan, metodologi, hasil, kesimpulan]):
                    st.error("Harap lengkapi semua field yang wajib diisi (*)")
                else:
                    with st.spinner("Membuat PDF resume..."):
                        # Siapkan data resume
                        data_resume = {
                            'judul': judul,
                            'peneliti': peneliti,
                            'institusi': institusi,
                            'tanggal': tanggal.strftime("%d %B %Y"),
                            'latar_belakang': latar_belakang,
                            'tujuan': tujuan,
                            'metodologi': metodologi,
                            'hasil': hasil,
                            'kesimpulan': kesimpulan,
                            'kata_kunci': kata_kunci
                        }
                        
                        # Generate PDF
                        pdf_path = generate_resume_pdf(data_resume)
                        
                        # Tampilkan preview dan download link
                        st.success("✅ Resume berhasil dibuat!")
                        
                        col_preview, col_download = st.columns(2)
                        
                        with col_preview:
                            st.subheader("Preview Data Resume")
                            st.json(data_resume, expanded=False)
                        
                        with col_download:
                            st.subheader("Unduh Resume")
                            with open(pdf_path, "rb") as pdf_file:
                                pdf_bytes = pdf_file.read()
                            
                            st.download_button(
                                label="📥 Download Resume PDF",
                                data=pdf_bytes,
                                file_name=f"resume_penelitian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf"
                            )
    
    # Tab 2: Analisis Kurva Kalibrasi
    with tab2:
        st.header("Analisis Kurva Kalibrasi")
        st.markdown("Masukkan data X (konsentrasi) dan Y (respons) untuk membuat kurva kalibrasi.")
        
        # Pilihan input data
        input_method = st.radio("Metode Input Data:", 
                                ["Input Manual", "Upload File CSV"], 
                                horizontal=True)
        
        x_data = []
        y_data = []
        
        if input_method == "Input Manual":
            st.subheader("Input Data Manual")
            
            col_x, col_y = st.columns(2)
            
            with col_x:
                st.markdown("**Data X (Konsentrasi)**")
                x_input = st.text_area("Masukkan nilai X (pisahkan dengan koma atau baris baru)", 
                                       value="0, 1, 2, 3, 4, 5",
                                       height=150)
            
            with col_y:
                st.markdown("**Data Y (Respons)**")
                y_input = st.text_area("Masukkan nilai Y (pisahkan dengan koma atau baris baru)", 
                                       value="0.1, 0.9, 2.1, 3.2, 4.0, 5.1",
                                       height=150)
            
            # Parse input
            if x_input and y_input:
                # Konversi input ke list angka
                try:
                    x_data = [float(x.strip()) for x in x_input.replace('\n', ',').split(',') if x.strip()]
                    y_data = [float(y.strip()) for y in y_input.replace('\n', ',').split(',') if y.strip()]
                    
                    if len(x_data) != len(y_data):
                        st.warning("Jumlah data X dan Y harus sama!")
                    elif len(x_data) < 2:
                        st.warning("Minimal diperlukan 2 data point untuk analisis!")
                    else:
                        # Tampilkan tabel data
                        df_data = pd.DataFrame({
                            'X (Konsentrasi)': x_data,
                            'Y (Respons)': y_data
                        })
                        
                        st.subheader("Data yang Dimasukkan")
                        st.dataframe(df_data, use_container_width=True)
                        
                        # Tombol untuk analisis
                        if st.button("📊 Analisis Kurva Kalibrasi", type="primary"):
                            with st.spinner("Menganalisis data..."):
                                # Lakukan analisis
                                results = analyze_calibration_curve(x_data, y_data)
                                
                                # Tampilkan hasil
                                st.subheader("Hasil Analisis")
                                
                                col_stats, col_plot = st.columns(2)
                                
                                with col_stats:
                                    st.markdown("### Parameter Statistik")
                                    
                                    metrics_df = pd.DataFrame({
                                        'Parameter': ['Slope (Kemiringan)', 'Intercept (Perpotongan)', 
                                                     'Koefisien Korelasi (r)', 'Koefisien Determinasi (R²)', 
                                                     'Standard Error', 'Jumlah Data (n)'],
                                        'Nilai': [
                                            f"{results['slope']:.6f}",
                                            f"{results['intercept']:.6f}",
                                            f"{results['r_value']:.6f}",
                                            f"{results['r_squared']:.6f}",
                                            f"{results['std_err']:.6f}",
                                            f"{len(x_data)}"
                                        ]
                                    })
                                    
                                    st.dataframe(metrics_df, use_container_width=True, hide_index=True)
                                    
                                    # Persamaan regresi
                                    st.markdown("### Persamaan Regresi")
                                    st.markdown(f"**y = {results['intercept']:.4f} + {results['slope']:.4f}x**")
                                    
                                    # Interpretasi R²
                                    st.markdown("### Interpretasi Koefisien Determinasi (R²)")
                                    r2_percent = results['r_squared'] * 100
                                    st.markdown(f"Nilai R² = **{results['r_squared']:.4f}**")
                                    st.progress(float(results['r_squared']))
                                    st.markdown(f"Ini berarti **{r2_percent:.2f}%** variasi dalam Y dapat dijelaskan oleh variasi dalam X melalui model regresi.")
                                
                                with col_plot:
                                    st.markdown("### Grafik Kurva Kalibrasi")
                                    st.pyplot(results['fig'])
                                    
                                    # Simpan plot sebagai gambar
                                    buf = io.BytesIO()
                                    results['fig'].savefig(buf, format='png', dpi=300)
                                    buf.seek(0)
                                    
                                    # Tombol download plot
                                    st.download_button(
                                        label="📥 Download Grafik (PNG)",
                                        data=buf,
                                        file_name=f"kurva_kalibrasi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                        mime="image/png"
                                    )
                                
                                # Prediksi nilai Y dari X
                                st.subheader("Prediksi Nilai Y dari X")
                                col_pred, col_info = st.columns([1, 2])
                                
                                with col_pred:
                                    x_pred_input = st.text_input("Masukkan nilai X untuk prediksi Y", value="")
                                    
                                    if x_pred_input:
                                        try:
                                            x_pred = float(x_pred_input)
                                            y_pred = results['intercept'] + results['slope'] * x_pred
                                            st.metric(label=f"Prediksi Y untuk X = {x_pred}", 
                                                     value=f"{y_pred:.4f}")
                                        except ValueError:
                                            st.warning("Masukkan angka yang valid untuk prediksi")
                                
                                with col_info:
                                    st.markdown("### Interpretasi Hasil")
                                    st.markdown("""
                                    - **Slope (Kemiringan)**: Perubahan rata-rata dalam Y untuk setiap unit perubahan dalam X
                                    - **Intercept (Perpotongan)**: Nilai Y ketika X = 0
                                    - **R² (Koefisien Determinasi)**: Proporsi variasi dalam Y yang dapat dijelaskan oleh X (0-1)
                                    - **Standard Error**: Ukuran variabilitas titik data di sekitar garis regresi
                                    """)
                
                except ValueError:
                    st.error("Pastikan data yang dimasukkan berupa angka!")
        
        else:  # Upload File CSV
            st.subheader("Upload File CSV")
            uploaded_file = st.file_uploader("Pilih file CSV", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    
                    st.subheader("Preview Data")
                    st.dataframe(df, use_container_width=True)
                    
                    # Pilih kolom X dan Y
                    if len(df.columns) >= 2:
                        col_x_select, col_y_select = st.columns(2)
                        
                        with col_x_select:
                            x_column = st.selectbox("Pilih kolom untuk X (konsentrasi)", df.columns)
                        
                        with col_y_select:
                            y_column = st.selectbox("Pilih kolom untuk Y (respons)", df.columns)
                        
                        if st.button("📊 Analisis Data dari CSV", type="primary"):
                            x_data = df[x_column].dropna().astype(float).tolist()
                            y_data = df[y_column].dropna().astype(float).tolist()
                            
                            if len(x_data) != len(y_data):
                                st.warning("Jumlah data X dan Y harus sama!")
                            elif len(x_data) < 2:
                                st.warning("Minimal diperlukan 2 data point untuk analisis!")
                            else:
                                # Lanjutkan dengan analisis yang sama seperti di atas
                                with st.spinner("Menganalisis data..."):
                                    results = analyze_calibration_curve(x_data, y_data)
                                    
                                    # Tampilkan hasil (sama seperti di bagian input manual)
                                    st.subheader("Hasil Analisis")
                                    
                                    col_stats, col_plot = st.columns(2)
                                    
                                    with col_stats:
                                        st.markdown("### Parameter Statistik")
                                        
                                        metrics_df = pd.DataFrame({
                                            'Parameter': ['Slope (Kemiringan)', 'Intercept (Perpotongan)', 
                                                         'Koefisien Korelasi (r)', 'Koefisien Determinasi (R²)', 
                                                         'Standard Error', 'Jumlah Data (n)'],
                                            'Nilai': [
                                                f"{results['slope']:.6f}",
                                                f"{results['intercept']:.6f}",
                                                f"{results['r_value']:.6f}",
                                                f"{results['r_squared']:.6f}",
                                                f"{results['std_err']:.6f}",
                                                f"{len(x_data)}"
                                            ]
                                        })
                                        
                                        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
                                        
                                        st.markdown("### Persamaan Regresi")
                                        st.markdown(f"**y = {results['intercept']:.4f} + {results['slope']:.4f}x**")
                                    
                                    with col_plot:
                                        st.markdown("### Grafik Kurva Kalibrasi")
                                        st.pyplot(results['fig'])
                                        
                                        # Simpan plot sebagai gambar
                                        buf = io.BytesIO()
                                        results['fig'].savefig(buf, format='png', dpi=300)
                                        buf.seek(0)
                                        
                                        # Tombol download plot
                                        st.download_button(
                                            label="📥 Download Grafik (PNG)",
                                            data=buf,
                                            file_name=f"kurva_kalibrasi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                            mime="image/png"
                                        )
                    else:
                        st.error("File CSV harus memiliki minimal 2 kolom data!")
                
                except Exception as e:
                    st.error(f"Error membaca file: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Dikembangkan dengan ❤️ menggunakan Streamlit</p>
        <p>© 2023 Aplikasi Resume Penelitian & Kurva Kalibrasi</p>
    </div>
    """,
    unsafe_allow_html=True
)

if __name__ == "__main__":
    main()
