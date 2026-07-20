import streamlit as st
import base64
import os
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Leaderboard Kelas", layout="wide")

# --- KONEKSI GOOGLE SHEETS ---
# MASUKKAN LINK GOOGLE SHEETS ANDA YANG SUDAH JADI 'EDITOR' DI SINI
URL_SHEET = "https://docs.google.com/spreadsheets/d/1l9eXqB5wHRqSHnTzYQAaNbJakXcIS6afIhS1fga6S3Q/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Membaca data dari Google Sheets
    df = conn.read(spreadsheet=URL_SHEET, ttl=0) # ttl=0 memastikan data selalu fresh
    
    # Mengubah dataframe menjadi dictionary agar cocok dengan kode leaderboard sebelumnya
    students_data = dict(zip(df['Nama'], df['Poin']))
except Exception as e:
    st.error("Gagal terhubung ke Google Sheets. Pastikan link sudah benar dan diatur sebagai 'Anyone with link can Edit'.")
    st.stop()

# Fungsi untuk menyimpan data kembali ke Google Sheets
def save_to_sheets(updated_dict):
    import pandas as pd
    new_df = pd.DataFrame(list(updated_dict.items()), columns=['Nama', 'Poin'])
    conn.update(spreadsheet=URL_SHEET, data=new_df)
    st.cache_data.clear() # Membersihkan cache agar perubahan langsung terlihat

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

# --- TATA LETAK APLIKASI (UI) ---
st.title("🏆 Leaderboard Kelas XII-A")

col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### 📝 Panel Input Guru")
    
    password = st.text_input("Masukkan Password Guru:", type="password")
    
    # Silakan ganti "rahasia123" dengan password Anda
    if password == "orcinusorca":
        st.success("Akses Diterima")
        
        selected_slot = st.selectbox("Pilih Slot Siswa:", list(students_data.keys()))
        new_name = st.text_input("Ubah Nama Siswa:", value=selected_slot)
        
        if st.button("Simpan Nama"):
            if new_name != selected_slot and new_name not in students_data:
                students_data[new_name] = students_data.pop(selected_slot)
                save_to_sheets(students_data)
                st.rerun()

        st.divider()

        add_points = st.number_input("Tambah Poin:", min_value=1, max_value=100, value=1)
        if st.button(f"➕ Tambah {add_points} Poin ke {new_name}"):
            students_data[new_name] = int(students_data[new_name]) + int(add_points)
            save_to_sheets(students_data)
            st.rerun()
            
        if st.button("➖ Kurangi 1 Poin (Koreksi)"):
            if int(students_data[new_name]) > 0:
                students_data[new_name] = int(students_data[new_name]) - 1
                save_to_sheets(students_data)
                st.rerun()
    elif password != "":
        st.error("Password Salah!")
    else:
        st.info("Silahkan masukkan password untuk mengakses panel input.")

with col2:
    st.markdown("### 📊 Papan Peringkat Live")
    
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
