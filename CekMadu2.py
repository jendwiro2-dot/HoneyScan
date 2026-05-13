import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🍯 HONEY SCAN")

st.write("Unggah foto madu dari Telepon Genggam untuk dianalisis")
# ======================
# UPLOAD FILE
# ======================
img_file = st.file_uploader("Unggah gambar madu", type=["jpg","png","jpeg"])

if img_file is not None:

    # LOAD IMAGE
    image = Image.open(img_file)
    img = np.array(image)

    # PERBAIKAN WARNA (WAJIB!)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    st.image(image, caption="Input Gambar", width="stretch")

    # ======================
    # PREPROCESSING
    # ======================
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ======================
    # FITUR
    # ======================
    hue_mean = np.mean(hsv[:,:,0])
    sat_mean = np.mean(hsv[:,:,1])
    val_mean = np.mean(hsv[:,:,2])
    texture_score = np.std(gray)
    brightness = val_mean
    color_variance = np.std(hsv[:,:,0])

    # ======================
    # SCORING
    # ======================
    score = 0

    if sat_mean > 80:
        score += 20
    elif sat_mean > 50:
        score += 15
    else:
        score += 10

    if texture_score < 25:
        score += 25
    elif texture_score < 40:
        score += 15
    else:
        score += 5

    if 80 < brightness < 180:
        score += 20
    else:
        score += 10

    if color_variance < 20:
        score += 20
    else:
        score += 10

    score += 10

    # ======================
    # OUTPUT
    # ======================
    st.subheader("📊 Hasil Analisis")

    st.write(f"🌈 Tingkat Kepekatan Madu: {sat_mean:.2f}")
    st.write(f"💡 Tingkat Kecerahan Madu: {brightness:.2f}")
    st.write(f"🧪 Tekstur Madu: {texture_score:.2f}")
    st.write(f"🎨 Variansi Warna Madu: {color_variance:.2f}")

    st.markdown("---")

    st.subheader("🏆 Skor Kualitas Madu")
    st.write(f"Skor: {score}/100")

    if score >= 80:
        st.success("Kualitas: SANGAT BAIK 🍯✨")
    elif score >= 60:
        st.info("Kualitas: BAIK 👍")
    elif score >= 40:
        st.warning("Kualitas: SEDANG ⚠️")
    else:
        st.error("Kualitas: RENDAH ❌")

    st.caption("Catatan: Analisis berbasis visual, bukan uji laboratorium.")