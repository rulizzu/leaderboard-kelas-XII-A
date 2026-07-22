import streamlit as st
import base64
import os
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Leaderboard Kelas", layout="wide")

# --- MEMBACA DATA DARI FILE EXCEL ---
EXCEL_FILE = "leaderboard.xlsx"

@st.cache_data(ttl=0) # ttl=0 agar selalu membaca data paling baru
def load_data_from_excel():
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE)
            df['Poin'] = df['Poin'].fillna(0).astype(int)
            return dict(zip(df['Nama'], df['Poin']))
        except Exception as e:
            st.error(f"Gagal membaca file Excel: {e}")
            st.stop()
    else:
        st.error(f"File '{EXCEL_FILE}' tidak ditemukan di GitHub. Pastikan Anda sudah mengunggahnya.")
        st.stop()

students_data = load_data_from_excel()

# --- FUNGSI UNTUK BACKGROUND GAMBAR LOKAL ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

bg_image_file = "pngtree-doodles-on-green-chalkboard-background-back-to-school-background-image_389839.jpg"
bg_base64 = get_base64_of_bin_file(bg_image_file)

# --- CSS KUSTOM (STYLING VISUAL) ---
page_bg_img = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{bg_base64}");
    background-size: cover;
    background-attachment: fixed;
}}
html, body, [class*="css"]  {{
    font-family: 'Caveat', cursive !important;
    color: #F8F8FF !important; 
}}
.leaderboard-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 30px;
    margin-bottom: 12px;
    border-radius: 8px;
    background-color: rgba(0, 0, 0, 0.5);
    border-left: 8px solid transparent;
    font-size: 26px;
    letter-spacing: 2px;
}}
.rank-1 {{ border-left-color: #FFD700; color: #FFD700 !important; font-size: 36px; font-weight: bold; text-shadow: 2px 2px 5px rgba(255, 215, 0, 0.5); }}
.rank-2 {{ border-left-color: #C0C0C0; color: #C0C0C0 !important; font-size: 32px; font-weight: bold; text-shadow: 2px 2px 5px rgba(192, 192, 192, 0.5); }}
.rank-3 {{ border-left-color: #CD7F32; color: #CD7F32 !important; font-size: 30px; font-weight: bold; text-shadow: 2px 2px 5px rgba(205, 127, 50, 0.5); }}
.rank-4, .rank-5 {{ border-left-color: #B76E79; color: #B76E79 !important; font-size: 28px; }}
.tally-marks {{
    font-family: Arial, sans-serif;
    font-size: 24px;
    color: white;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- FUNGSI TALLY MARKS ---
def get_tally_html(points):
    points = int(points)
    if points <= 0:
        return "0"
    fives = points // 5
    ones = points % 5
    tally_5 = "<span style='text-decoration: line-through; margin-right: 5px;'>||||</span>" 
    tally_1 = "|" * ones
    return f"<span class='tally-marks'>{tally_5 * fives}{tally_1}</span>"

# --- TATA LETAK APLIKASI (HANYA MENAMPILKAN PERINGKAT) ---
st.title("🏆 Leaderboard Kelas XII-A")

# Mengurutkan siswa berdasarkan poin tertinggi
sorted_students = sorted(students_data.items(), key=lambda x: int(x[1]), reverse=True)

for rank, (name, points) in enumerate(sorted_students):
    rank_num = rank + 1
    
    if rank_num == 1:
        css_class = "rank-1"
    elif rank_num == 2:
        css_class = "rank-2"
    elif rank_num == 3:
        css_class = "rank-3"
    elif rank_num in [4, 5]:
        css_class = "rank-4"
    else:
        css_class = ""

    tally_visual = get_tally_html(points)
    
    row_html = f"""
    <div class="leaderboard-row {css_class}">
        <div style="width: 10%;">#{rank_num}</div>
        <div style="width: 40%;">{name}</div>
        <div style="width: 15%; text-align: center;">{int(points)} pt</div>
        <div style="width: 35%; text-align: right;">{tally_visual}</div>
    </div>
    """
    st.markdown(row_html, unsafe_allow_html=True)
