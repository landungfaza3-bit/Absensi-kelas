# ==========================================
# APLIKASI ABSENSI SISWA
# Menggunakan:
# - Python
# - Tkinter (GUI)
# - SQLite (Database)
# ==========================================

import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ==========================================
# MEMBUAT DATABASE
# ==========================================

conn = sqlite3.connect("absensi.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS absensi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    tanggal TEXT,
    status TEXT
)
""")

conn.commit()

# ==========================================
# FUNGSI SIMPAN ABSENSI
# ==========================================

def simpan_absensi(status):

    # Mengambil nama dari input
    nama = entry_nama.get()

    # Validasi jika nama kosong
    if nama == "":
        messagebox.showwarning("Peringatan", "Nama siswa harus diisi!")
        return

    # Mengambil tanggal hari ini otomatis
    tanggal = datetime.now().strftime("%Y-%m-%d")

    # Menyimpan data ke database
    cursor.execute("""
    INSERT INTO absensi (nama, tanggal, status)
    VALUES (?, ?, ?)
    """, (nama, tanggal, status))

    conn.commit()

    # Menampilkan pesan sukses
    messagebox.showinfo(
        "Sukses",
        f"{nama} berhasil absen {status}"
    )

    # Mengosongkan input setelah submit
    entry_nama.delete(0, tk.END)

# ==========================================
# FUNGSI REKAP ABSENSI
# ==========================================

def lihat_rekap():

    nama = entry_nama.get()

    # Validasi
    if nama == "":
        messagebox.showwarning(
            "Peringatan",
            "Masukkan nama siswa terlebih dahulu!"
        )
        return

    # Mengambil data berdasarkan nama siswa
    cursor.execute("""
    SELECT status, COUNT(*)
    FROM absensi
    WHERE nama = ?
    GROUP BY status
    """, (nama,))

    hasil = dict(cursor.fetchall())

    # Mengambil jumlah masing-masing status
    hadir = hasil.get("Hadir", 0)
    izin = hasil.get("Izin", 0)
    alfa = hasil.get("Alfa", 0)

    # Menghitung total absensi
    total = hadir + izin + alfa

    # Menghindari error pembagian 0
    if total == 0:
        messagebox.showinfo(
            "Rekap",
            "Data absensi belum tersedia!"
        )
        return

    # Menghitung presentase kehadiran
    presentase = (hadir / total) * 100

    # Menampilkan hasil rekap
    teks = f"""
REKAP ABSENSI 1 BULAN

Nama : {nama}

Hadir : {hadir}
Izin  : {izin}
Alfa  : {alfa}

Presentase Kehadiran :
{presentase:.2f} %
"""

    messagebox.showinfo("Rekap Bulanan", teks)

# ==========================================
# MEMBUAT GUI
# ==========================================

root = tk.Tk()
root.title("Aplikasi Absensi Siswa")
root.geometry("350x300")

# Judul
judul = tk.Label(
    root,
    text="APLIKASI ABSENSI SISWA",
    font=("Arial", 14, "bold")
)

judul.pack(pady=10)

# Label Nama
label_nama = tk.Label(
    root,
    text="Masukkan Nama Siswa"
)

label_nama.pack()

# Input Nama
entry_nama = tk.Entry(root, width=30)
entry_nama.pack(pady=5)

# Tombol Hadir
btn_hadir = tk.Button(
    root,
    text="Hadir",
    width=20,
    bg="green",
    fg="white",
    command=lambda: simpan_absensi("Hadir")
)

btn_hadir.pack(pady=5)

# Tombol Izin
btn_izin = tk.Button(
    root,
    text="Izin",
    width=20,
    bg="orange",
    fg="white",
    command=lambda: simpan_absensi("Izin")
)

btn_izin.pack(pady=5)

# Tombol Alfa
btn_alfa = tk.Button(
    root,
    text="Alfa",
    width=20,
    bg="red",
    fg="white",
    command=lambda: simpan_absensi("Alfa")
)

btn_alfa.pack(pady=5)

# Tombol Rekap
btn_rekap = tk.Button(
    root,
    text="Lihat Rekap",
    width=20,
    command=lihat_rekap
)

btn_rekap.pack(pady=15)

# Menjalankan aplikasi
root.mainloop()
