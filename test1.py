import csv
import pandas as pd

class FiniteStateAutomata:
    def __init__(self):
        self.state = 'START'
    
    def transition(self, event):
        if self.state == 'START':
            if event == 'semester_ok':
                self.state = 'SEMESTER_CHECKED'
            else:
                self.state = 'REJECTED'
        
        elif self.state == 'SEMESTER_CHECKED':
            if event == 'grades_ok':
                self.state = 'ACCEPTED'
            else:
                self.state = 'REJECTED'
    
    def is_accepted(self):
        return self.state == 'ACCEPTED'
    
    def is_rejected(self):
        return self.state == 'REJECTED'

# Fungsi untuk screening awal mahasiswa dengan konsentrasi RPL
def screening_mahasiswa(mahasiswa):
    fsa = FiniteStateAutomata()
    
    # Memproses kondisi semester
    if mahasiswa['semester'] >= 5:
        fsa.transition('semester_ok')
    else:
        fsa.transition('semester_not_ok')
    
    if fsa.is_rejected():
        return "Mahasiswa ditolak"
    
    # Memproses kondisi nilai mata kuliah
    relevant_courses = [
        mahasiswa['pbo'],
        mahasiswa['pw'],
        mahasiswa['rpl'],
        mahasiswa['imk']
    ]
    
    # Menghitung jumlah mata kuliah dengan nilai B atau lebih baik
    accepted_grades = ['A', 'B']
    count_accepted_grades = sum(1 for grade in relevant_courses if grade in accepted_grades)
    
    if count_accepted_grades >= 3:
        fsa.transition('grades_ok')
    else:
        fsa.transition('grades_not_ok')
    
    if fsa.is_accepted():
        return "Mahasiswa diterima"
    else:
        return "Mahasiswa ditolak"

# Fungsi untuk menyimpan hasil ke dalam file CSV
def save_to_csv(mahasiswa_list, filename="hasil_screening.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
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
        semester = int(input("Masukkan semester mahasiswa: "))
        pbo = input("Masukkan nilai Pemrograman Berbasis Objek (A/B/C/D/E): ").upper()
        pw = input("Masukkan nilai Pemrograman Web (A/B/C/D/E): ").upper()
        rpl = input("Masukkan nilai Rekayasa Perangkat Lunak (A/B/C/D/E): ").upper()
        imk = input("Masukkan nilai Interaksi Manusia dan Komputer (A/B/C/D/E): ").upper()
        
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
