import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from datetime import datetime
import requests
import os
import pytz
import urllib.parse

# 🌟 Konfigurasi Halaman
st.set_page_config(
    page_title="☕ Coffee Quality Classifier Ultimate 2025",
    page_icon="☕",
    layout="wide"
)

# 🌗 AUTO LIGHT/DARK MODE berdasarkan waktu lokal
hour = datetime.now(pytz.timezone("Asia/Jakarta")).hour
is_dark = hour >= 18 or hour < 6  # malam → dark mode

background_color = "#1B0E07" if is_dark else "#FFF8E1"
text_color = "#F5F5F5" if is_dark else "#3E2723"
accent_color = "#FFD54F" if is_dark else "#6D4C41"

# 🎨 CSS Dinamis sesuai mode
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@600&display=swap');

        body {{
            font-family: 'Montserrat', sans-serif;
            background: radial-gradient(circle at top left, {background_color}, {'#2E1A12' if is_dark else '#D7CCC8'} 90%);
            color: {text_color};
        }}

        .main-card {{
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 25px 30px;
            margin-bottom: 25px;
            box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
        }}

        .title {{
            font-family: 'Playfair Display', serif;
            font-size: 45px;
            font-weight: 700;
            color: {accent_color};
            text-shadow: 2px 2px 15px rgba(255, 213, 79, 0.3);
        }}

        .subtitle {{
            color: #D7CCC8;
            font-size: 18px;
            margin-bottom: 20px;
        }}

        .stButton button {{
            background: linear-gradient(135deg, #8B4513, #D2B48C);
            color: #fff;
            font-weight: bold;
            border: none;
            border-radius: 12px;
            padding: 10px 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: 0.3s;
        }}

        .stButton button:hover {{
            transform: scale(1.05);
            background: linear-gradient(135deg, #A0522D, #E5C28E);
        }}

        .footer {{
            color: #BCAAA4;
            font-size: 14px;
            text-align: center;
            margin-top: 40px;
        }}
    </style>
""", unsafe_allow_html=True)

# 🧭 Header
st.markdown(f"""
    <div style="text-align:center;">
        <img src="https://cdn-icons-png.flaticon.com/512/924/924514.png" width="90">
        <h1 class="title">Coffee Quality Classifier ☕</h1>
        <p class="subtitle">Nikmati aroma data, cuaca, dan sains dalam satu cangkir</p>
    </div>
""", unsafe_allow_html=True)

# 🔧 Load Model
try:
    model = joblib.load("model_klasifikasi_kualitas_kopi.joblib")
except:
    st.warning("⚠️ Model belum tersedia. Pastikan file 'model_klasifikasi_kualitas_kopi.joblib' ada di folder project.")
    st.stop()

# 🎛️ Input Section
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

# 🌦️ Integrasi Cuaca dengan Open-Meteo
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.subheader("🌦️ Cuaca & Saran Roasting Kopi")
city = st.text_input("🌍 Masukkan kota kamu:", "Jakarta")

if st.button("☁️ Ambil Data Cuaca"):
    try:
        city_encoded = urllib.parse.quote(city)
        url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={city_encoded}&count=1"
        geo = requests.get(url_geo, timeout=10).json()

        if "results" in geo:
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            cuaca = requests.get(url_weather, timeout=10).json()
            suhu = cuaca["current_weather"]["temperature"]

            if suhu < 20:
                saran = "Cuaca dingin — cocok untuk **Dark Roast** biar hangat 🔥"
            elif suhu < 28:
                saran = "Cuaca sedang — pilih **Medium Roast** ☕"
            else:
                saran = "Cuaca panas — **Light Roast** lebih pas 🌞"

            st.success(f"Suhu di {city}: {suhu}°C\n\n{saran}")
        else:
            st.error("❌ Kota tidak ditemukan, coba periksa ejaan.")
    except Exception as e:
        st.error(f"Gagal mengambil data cuaca 😢 ({e})")
st.markdown('</div>', unsafe_allow_html=True)

# 🔮 Prediksi Kualitas Kopi
if st.button("✨ Prediksi Kualitas Kopi"):
    df = pd.DataFrame([[kadar_kafein, tingkat_keasaman, jenis_proses]],
                      columns=["Kadar Kafein", "Tingkat Keasaman", "Jenis Proses"])
    
    prediksi = model.predict(df)[0]
    proba = model.predict_proba(df)[0]

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"<h3>☕ Hasil Prediksi: <span style='color:{accent_color};'>{prediksi}</span></h3>", unsafe_allow_html=True)
    st.caption(f"Model confidence: {max(proba)*100:.2f}%")

    # 🎨 Warna kopi custom
    px.colors.sequential.Coffee = ['#3E2723', '#6D4C41', '#A1887F', '#D7CCC8', '#EFEBE9']

    proba_df = pd.DataFrame({
        "Kualitas": model.classes_,
        "Probabilitas": proba
    })

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
        font_color=text_color,
        title_font_color=accent_color
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 🧾 Simpan riwayat ke CSV
    history_file = "riwayat_prediksi_kopi.csv"
    new_entry = pd.DataFrame({
        "Waktu": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Kafein": [kadar_kafein],
        "pH": [tingkat_keasaman],
        "Proses": [jenis_proses],
        "Prediksi": [prediksi],
        "Kepercayaan (%)": [max(proba)*100]
    })

    if os.path.exists(history_file):
        old = pd.read_csv(history_file)
        pd.concat([old, new_entry], ignore_index=True).to_csv(history_file, index=False)
    else:
        new_entry.to_csv(history_file, index=False)

    st.success("Riwayat prediksi disimpan ke 'riwayat_prediksi_kopi.csv' 📁")
    st.balloons()

# 📅 Footer
st.markdown(
    f'<div class="footer">© {datetime.now().year} — Dibuat dengan cinta, data, dan kopi oleh <b>Khairul Faiz Ramadhan</b></div>',
    unsafe_allow_html=True
)
