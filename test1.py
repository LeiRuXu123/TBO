import csv
import pandas as pd
import os

class FiniteStateAutomata:
    def __init__(self):
        self.state = 'Kondisi_awal'
    
    def transition(self, event):
        print(f"Pengecekan {self.state} pada {event}")
        if self.state == 'Kondisi_awal':
            if event == 'semester_ok':
                self.state = 'SEMESTER'
            else:
                self.state = 'DITOLAK'
        
        elif self.state == 'SEMESTER_CHECKED':
            if event == 'nilai_ok':
                self.state = 'DITERIMA'
            elif event == 'pengecekan_tambahan':
                self.state = 'Pengecekan Tambahan Diperlukan'
            else:
                self.state = 'DITOLAK'
        
        elif self.state == 'Pengecekan Tambahan Diperlukan':
            if event == 'nilai_tambahan_ok':
                self.state = 'DITERIMA'
            else:
                self.state = 'DITOLAK'
    
    def is_DITERIMA(self):
        return self.state == 'DITERIMA'
    
    def is_DITOLAK(self):
        return self.state == 'DITOLAK'

# Fungsi untuk screening awal mahasiswa dengan konsentrasi RPL
def screening_mahasiswa(mahasiswa):
    fsa = FiniteStateAutomata()
    
    # Memproses kondisi semester
    if mahasiswa['semester'] >= 5:
        fsa.transition('semester_ok')
    else:
        fsa.transition('semester_not_ok')
    
    if fsa.is_DITOLAK():
        return "Mahasiswa ditolak"
    
    # Memproses kondisi nilai mata kuliah
    relevant_courses = [
        mahasiswa['pbo'],
        mahasiswa['pw'],
        mahasiswa['rpl'],
        mahasiswa['imk']
    ]
    
    # Menghitung jumlah mata kuliah dengan nilai B atau lebih baik
    DITERIMA_grades = ['A', 'B']
    count_DITERIMA_grades = sum(1 for grade in relevant_courses if grade in DITERIMA_grades)
    
    if count_DITERIMA_grades >= 3:
        fsa.transition('nilai_ok')
    elif count_DITERIMA_grades == 2:
        fsa.transition('pengecekan_tambahan')
        # Memproses nilai Algoritma dan Pemrograman
        algoritma_nilai = input("Masukkan nilai Algoritma dan Pemrograman (A/B/C/D/E): ").upper()
        if algoritma_nilai in DITERIMA_grades:
            fsa.transition('nilai algoritma dan pemrograman memenuhi')
        else:
            fsa.transition('nilai algoritma dan pemrograman tidak memenuhi')
    else:
        fsa.transition('nilai tidak memenuhi')
    
    if fsa.is_DITERIMA():
        return "Mahasiswa diterima"
    else:
        return "Mahasiswa ditolak"

# Fungsi untuk menyimpan hasil ke dalam file CSV
def save_to_csv(mahasiswa_list, filename="hasil_screening.csv"):
    # Memeriksa apakah file sudah ada
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Tulis header hanya jika file belum ada
        if not file_exists:
            writer.writerow(["Nama", "Semester", "PBO", "PW", "RPL", "IMK", "Status"])
        for mahasiswa in mahasiswa_list:
            writer.writerow([
                mahasiswa['nama'],
                mahasiswa['semester'],
                mahasiswa['pbo'],
                mahasiswa['pw'],
                mahasiswa['rpl'],
                mahasiswa['imk'],
                mahasiswa['status']
            ])

# Fungsi untuk mendapatkan input dari pengguna
def get_mahasiswa_input():
    mahasiswa_list = []
    while True:
        nama = input("Masukkan nama mahasiswa: ")
        
        while True:
            try:
                semester = int(input("Masukkan semester mahasiswa: "))
                break
            except ValueError:
                print("Input tidak valid. Silakan masukkan angka untuk semester.")
        
        valid_grades = ['A', 'B', 'C', 'D', 'E']
        
        while True:
            pbo = input("Masukkan nilai Pemrograman Berbasis Objek (A/B/C/D/E): ").upper()
            if pbo in valid_grades:
                break
            else:
                print("Input tidak valid. Silakan masukkan nilai yang valid (A/B/C/D/E).")
        
        while True:
            pw = input("Masukkan nilai Pemrograman Web (A/B/C/D/E): ").upper()
            if pw in valid_grades:
                break
            else:
                print("Input tidak valid. Silakan masukkan nilai yang valid (A/B/C/D/E).")
        
        while True:
            rpl = input("Masukkan nilai Rekayasa Perangkat Lunak (A/B/C/D/E): ").upper()
            if rpl in valid_grades:
                break
            else:
                print("Input tidak valid. Silakan masukkan nilai yang valid (A/B/C/D/E).")
        
        while True:
            imk = input("Masukkan nilai Interaksi Manusia dan Komputer (A/B/C/D/E): ").upper()
            if imk in valid_grades:
                break
            else:
                print("Input tidak valid. Silakan masukkan nilai yang valid (A/B/C/D/E).")
        
        mahasiswa = {
            'nama': nama,
            'semester': semester,
            'pbo': pbo,
            'pw': pw,
            'rpl': rpl,
            'imk': imk
        }
        
        mahasiswa['status'] = screening_mahasiswa(mahasiswa)
        mahasiswa_list.append(mahasiswa)
        
        more = input("Apakah Anda ingin menambahkan mahasiswa lain? (yes/no): ").lower()
        if more != 'yes':
            break
    
    return mahasiswa_list

# Mendapatkan input dari pengguna
mahasiswa_list = get_mahasiswa_input()

# Menyimpan hasil ke dalam file CSV
save_to_csv(mahasiswa_list)

# Membaca hasil screening dari file CSV dan menampilkannya dengan pandas DataFrame
df = pd.read_csv("hasil_screening.csv")
print(df)