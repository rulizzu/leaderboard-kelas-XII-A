import streamlit as st
import base64
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Leaderboard Kelas", layout="wide")

# --- INISIALISASI DATA SISWA (Maks 22 Siswa) ---
# Menggunakan session_state agar data tersimpan dan update real-time
if 'students' not in st.session_state:
    # Membuat data awal kosong untuk 22 siswa
    st.session_state.students = {f"Siswa {i+1}": 0 for i in range(22)}

# --- FUNGSI UNTUK BACKGROUND GAMBAR LOKAL ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# Masukkan nama file background papan tulis Anda di sini
bg_image_file = "pngtree-doodles-on-green-chalkboard-background-back-to-school-background-image_389839.jpg"
bg_base64 = get_base64_of_bin_file(bg_image_file)

# --- CSS KUSTOM (STYLING VISUAL) ---
page_bg_img = f"""
<style>
/* Mengambil font mirip kapur dari Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');

[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{bg_base64}");
    background-size: cover;
    background-attachment: fixed;
}}

/* Styling untuk teks agar terlihat seperti kapur putih di papan tulis */
html, body, [class*="css"]  {{
    font-family: 'Caveat', cursive !important;
    color: #F8F8FF !important; 
}}

/* Styling Baris Leaderboard */
.leaderboard-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 30px;
    margin-bottom: 12px;
    border-radius: 8px;
    background-color: rgba(0, 0, 0, 0.5); /* Latar transparan gelap agar tulisan terbaca */
    border-left: 8px solid transparent;
    font-size: 26px;
    letter-spacing: 2px;
}}

/* Highlight Warna Ranking */
.rank-1 {{ border-left-color: #FFD700; color: #FFD700 !important; font-size: 36px; font-weight: bold; text-shadow: 2px 2px 5px rgba(255, 215, 0, 0.5); }} /* Emas */
.rank-2 {{ border-left-color: #C0C0C0; color: #C0C0C0 !important; font-size: 32px; font-weight: bold; text-shadow: 2px 2px 5px rgba(192, 192, 192, 0.5); }} /* Perak */
.rank-3 {{ border-left-color: #CD7F32; color: #CD7F32 !important; font-size: 30px; font-weight: bold; text-shadow: 2px 2px 5px rgba(205, 127, 50, 0.5); }} /* Perunggu */
.rank-4, .rank-5 {{ border-left-color: #B76E79; color: #B76E79 !important; font-size: 28px; }} /* Rose Gold */

.tally-marks {{
    font-family: Arial, sans-serif; /* Tally mark butuh font standar agar rapi */
    font-size: 24px;
    color: white;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- FUNGSI TALLY MARKS ---
def get_tally_html(points):
    """Mengubah angka poin menjadi visualisasi Tally Marks menggunakan HTML (mirip coretan kapur)"""
    if points == 0:
        return "0"
    
    fives = points // 5
    ones = points % 5
    
    # Menggunakan efek coret (strike-through) untuk mewakili 5 poin (卌 atau <s>||||</s>)
    tally_5 = "<span style='text-decoration: line-through; margin-right: 5px;'>||||</span>" 
    tally_1 = "|" * ones
    
    return f"<span class='tally-marks'>{tally_5 * fives}{tally_1}</span>"

# --- TATA LETAK APLIKASI (UI) ---
st.title("🏆 Leaderboard Kelas")

# Membagi layar menjadi 2 kolom (Kiri untuk Input, Kanan untuk Leaderboard)
col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### 📝 Panel Input Guru")
    st.write("Edit nama siswa dan update poin mereka di sini.")
    
    # 1. Input untuk mengganti/update nama siswa
    selected_slot = st.selectbox("Pilih Slot Siswa:", list(st.session_state.students.keys()))
    new_name = st.text_input("Ubah Nama Siswa (Biarkan jika tidak ingin diubah):", value=selected_slot)
    
    if st.button("Simpan Nama"):
        if new_name != selected_slot and new_name not in st.session_state.students:
            # Pindahkan poin dari nama lama ke nama baru
            st.session_state.students[new_name] = st.session_state.students.pop(selected_slot)
            st.rerun()

    st.divider()

    # 2. Input untuk menambah poin
    add_points = st.number_input("Tambah Poin:", min_value=1, max_value=100, value=1)
    if st.button(f"➕ Tambah {add_points} Poin ke {new_name}"):
        st.session_state.students[new_name] += add_points
        st.rerun()
        
    if st.button("➖ Kurangi 1 Poin (Koreksi)"):
        if st.session_state.students[new_name] > 0:
            st.session_state.students[new_name] -= 1
            st.rerun()

with col2:
    st.markdown("### 📊 Papan Peringkat Live")
    
    # Mengurutkan siswa berdasarkan poin tertinggi (Descending)
    sorted_students = sorted(st.session_state.students.items(), key=lambda x: x[1], reverse=True)
    
    # Menampilkan data
    for rank, (name, points) in enumerate(sorted_students):
        rank_num = rank + 1
        
        # Menentukan class CSS berdasarkan ranking
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

        # Format tampilan HTML tiap baris
        tally_visual = get_tally_html(points)
        
        row_html = f"""
        <div class="leaderboard-row {css_class}">
            <div style="width: 10%;">#{rank_num}</div>
            <div style="width: 40%;">{name}</div>
            <div style="width: 15%; text-align: center;">{points} pt</div>
            <div style="width: 35%; text-align: right;">{tally_visual}</div>
        </div>
        """
        st.markdown(row_html, unsafe_allow_html=True)