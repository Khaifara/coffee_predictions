import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from datetime import datetime

# 🌟 Konfigurasi Halaman
st.set_page_config(
    page_title="☕ Coffee Quality Classifier Premium",
    page_icon="☕",
    layout="wide"
)

# 🎨 CSS Custom: efek kaca, font premium, dan warna kopi
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@600&display=swap');

        body {
            font-family: 'Montserrat', sans-serif;
            background: radial-gradient(circle at top left, #2E1A12, #1B0E07 90%);
            color: #F5F5F5;
        }

        .main-card {
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 25px 30px;
            margin-bottom: 25px;
            box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
        }

        .title {
            font-family: 'Playfair Display', serif;
            font-size: 45px;
            font-weight: 700;
            color: #FFD54F;
            text-shadow: 2px 2px 15px rgba(255, 213, 79, 0.3);
        }

        .subtitle {
            color: #D7CCC8;
            font-size: 18px;
            margin-bottom: 20px;
        }

        .stButton button {
            background: linear-gradient(135deg, #8B4513, #D2B48C);
            color: #fff;
            font-weight: bold;
            border: none;
            border-radius: 12px;
            padding: 10px 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: 0.3s;
        }

        .stButton button:hover {
            transform: scale(1.05);
            background: linear-gradient(135deg, #A0522D, #E5C28E);
        }

        .footer {
            color: #BCAAA4;
            font-size: 14px;
            text-align: center;
            margin-top: 40px;
        }

        .emoji {
            font-size: 24px;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# 🧭 Header / Navbar
st.markdown("""
    <div style="text-align:center;">
        <img src="https://cdn-icons-png.flaticon.com/512/924/924514.png" width="90">
        <h1 class="title">Coffee Quality Classifier ☕</h1>
        <p class="subtitle">Nikmati aroma data sains dengan rasa premium</p>
    </div>
""", unsafe_allow_html=True)

# 🔧 Load Model
try:
    model = joblib.load("model_klasifikasi_kualitas_kopi.joblib")
except:
    st.warning("⚠️ Model belum tersedia. Pastikan file 'model_klasifikasi_kualitas_kopi.joblib' ada di folder project.")
    st.stop()

# 🎛️ Input Section (Glass Card)
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🔧 Masukkan Parameter Kopi")
    col1, col2, col3 = st.columns(3)
    with col1:
        kadar_kafein = st.slider("☕ Kadar Kafein (mg)", 50.0, 200.0, 120.0)
    with col2:
        tingkat_keasaman = st.slider("🍋 Keasaman (pH)", 0.1, 7.0, 5.0)
    with col3:
        jenis_proses = st.selectbox("⚙️ Jenis Proses", ["Natural", "Honey", "Washed"])
    st.markdown('</div>', unsafe_allow_html=True)

# 🔮 Prediksi & Visualisasi
if st.button("✨ Prediksi Kualitas Kopi"):
    df = pd.DataFrame([[kadar_kafein, tingkat_keasaman, jenis_proses]],
                      columns=["Kadar Kafein", "Tingkat Keasaman", "Jenis Proses"])
    
    prediksi = model.predict(df)[0]
    proba = model.predict_proba(df)[0]

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"<h3>☕ Hasil Prediksi: <span style='color:#FFD54F;'>{prediksi}</span></h3>", unsafe_allow_html=True)
    st.caption(f"Model confidence: {max(proba)*100:.2f}%")

    # 🎯 Warna kopi custom
    px.colors.sequential.Coffee = ['#3E2723', '#6D4C41', '#A1887F', '#D7CCC8', '#EFEBE9']

    # 🪄 Gunakan DataFrame agar aman di semua versi Plotly
    proba_df = pd.DataFrame({
        "Kualitas": model.classes_,
        "Probabilitas": proba
    })

    # 📊 Visualisasi probabilitas
    fig = px.bar(
        proba_df,
        x="Kualitas",
        y="Probabilitas",
        title="Distribusi Probabilitas Prediksi",
        color="Kualitas",
        color_discrete_sequence=px.colors.sequential.Coffee
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#fff',
        title_font_color='#FFD54F'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.success("Prediksi berhasil! Selamat menikmati kopi terbaikmu ☕✨")
    st.balloons()

# 📅 Footer
st.markdown(
    f'<div class="footer">© {datetime.now().year} — Dibuat dengan cinta & kopi oleh <b>Khairul Faiz Ramadhan</b></div>',
    unsafe_allow_html=True
)
