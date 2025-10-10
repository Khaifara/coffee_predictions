import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
	page_title = "Klasifikasi Kualitas Kopi",
	page_icon = "☕"
)

model = joblib.load("model_klasifikasi_kualitas.joblib")

st.title("Klasifikasi Kualitas Kopi")
st.markdown("Klasifikasi kualitas kopi berdasarkan fitur Kadar Kafein, Tingkat Keasaman dan Jenis Proses")

kadar_kafein = st.slider("Kadar Kafein", 50.0, 200.0, 110.0)
tingkat_keasaman = st.slider("Tingkat Keasaman", 0.1, 7.0, 5.1)
jenis_proses = st.pills("Jenis Proses", ["Natural","Honey","Washed"], default="Natural")

if st.button("Prediksi", type="primary"):
	data = pd.DataFrame([[kadar_kafein,tingkat_keasaman,jenis_proses]],columns=["Kadar Kafein","Tingkat Keasaman","Jenis Proses"])
	prediksi = model.predict(data)[0]
	presentase = max(model.predict_proba(data)[0])
	st.success(f"Prediksi {prediksi} dengan keyakinan {presentase*100:.2f}%")
	st.balloons()


st.divider()
st.caption("Dibuat dengan ☕ oleh **Khairul Faiz Ramadhan**")


