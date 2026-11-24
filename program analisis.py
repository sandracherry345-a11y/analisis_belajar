import csv
import os

FILE_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "StudentPerformanceFactors.csv")

KOLOM_WAJIB = [
    "Hours_Studied",
    "Attendance",
    "Previous_Scores",
    "Sleep_Hours",
    "Tutoring_Sessions",
    "Motivation_Level",
    "Physical_Activity",
    "Exam_Score"
]

# kolom yang harus berisi bilangan bulat
KOLOM_ANGKA = [
    "Hours_Studied",
    "Attendance",
    "Previous_Scores",
    "Sleep_Hours",
    "Tutoring_Sessions",
    "Physical_Activity",
    "Exam_Score"
]

# aspek yang boleh diubah siswa (urutan NAMA_ASPEK sama dengan KOLOM_ASPEK)
NAMA_ASPEK = ["Jam belajar", "Kehadiran", "Nilai sebelumnya", "Durasi tidur",
              "Sesi bimbingan", "Motivasi", "Aktivitas fisik", "Nilai ujian"]
KOLOM_ASPEK = ["Hours_Studied", "Attendance", "Previous_Scores", "Sleep_Hours",
               "Tutoring_Sessions", "Motivation_Level", "Physical_Activity", "Exam_Score"]


# --- DATASET ---
def baca_data():
    """Fungsi membaca dataset CSV dan memvalidasi setiap baris."""
    data = []

    if not os.path.exists(FILE_CSV):
        print("Error: File CSV tidak ditemukan.")
        print("Lokasi yang dicari:", FILE_CSV)
        return data

    with open(FILE_CSV, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            print("Error: Dataset tidak memiliki header.")
            return data

        if not all(kolom in reader.fieldnames for kolom in KOLOM_WAJIB):
            kolom_hilang = [kolom for kolom in KOLOM_WAJIB if kolom not in reader.fieldnames]
            print("Error: Kolom berikut tidak ditemukan:")
            for kolom in kolom_hilang:
                print(f"- {kolom}")
            return data

        for nomor_baris, row in enumerate(reader, start=2):
            try:
                for kolom in KOLOM_ANGKA:
                    row[kolom] = int(row[kolom])
            except (ValueError, TypeError):
                print(f"Peringatan baris {nomor_baris}: salah satu nilai angka bukan bilangan bulat valid.")
                continue

            negatif = False
            for kolom in KOLOM_ANGKA:
                if row[kolom] < 0:
                    negatif = True

            if negatif:
                print(f"Peringatan baris {nomor_baris}: nilai numerik tidak boleh bernilai negatif.")
                continue

            row["Kategori"] = kategori_nilai(row["Exam_Score"])
            row["Baris_CSV"] = nomor_baris
            data.append(row)

            if len(data) == 300:
                break
    return data


def validasi_nilai_baru(kolom, nilai):
    """Fungsi memvalidasi nilai baru sebelum disimpan. Mengembalikan True jika valid."""
    if kolom == "Motivation_Level":
        if nilai != "Low" and nilai != "Medium" and nilai != "High":
            print("[ERROR] Motivasi harus Low, Medium, atau High!")
            return False
        return True

    try:
        angka = int(nilai)
    except ValueError:
        print("[ERROR] Nilai harus berupa bilangan bulat!")
        return False

    if angka < 0:
        print("[ERROR] Nilai tidak boleh negatif!")
        return False

    if kolom == "Sleep_Hours" and angka > 24:
        print("[ERROR] Nilai tidak boleh lebih dari 24!")
        return False

    if (kolom == "Attendance" or kolom == "Previous_Scores" or kolom == "Exam_Score") and angka > 100:
        print("[ERROR] Nilai tidak boleh lebih dari 100!")
        return False

    return True


def simpan_ke_csv(nomor_baris, kolom, nilai_baru):
    """Fungsi mengubah satu nilai di file CSV tanpa menghapus data lainnya."""
    try:
        # baca SEMUA baris di file CSV
        semua_baris = []
        with open(FILE_CSV, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            nama_kolom = reader.fieldnames
            for row in reader:
                semua_baris.append(row)

        # ubah satu nilai saja (baris pertama data ada di baris ke-2 file CSV)
        semua_baris[nomor_baris - 2][kolom] = nilai_baru

        # tulis ulang semua baris ke file CSV
        with open(FILE_CSV, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=nama_kolom)
            writer.writeheader()
            for row in semua_baris:
                writer.writerow(row)

    except (OSError, IndexError):
        print("[ERROR] Gagal menyimpan ke file CSV. Pastikan file tidak sedang dibuka di Excel.")
        return False

    return True

# --- ANALISIS ---
def kategori_nilai(nilai):
    """Fungsi menentukan kategori hasil ujian."""
    if nilai >= 85:
        return "Tinggi"
    elif nilai >= 70:
        return "Sedang"
    else:
        return "Perlu Perhatian"


def rata_rata(data, kolom):
    """Fungsi menghitung rata-rata satu kolom."""
    total = 0
    for row in data:
        total += row[kolom]
    return total / len(data)


def ringkasan_data(data):
    """Fungsi menampilkan ringkasan data seluruh siswa."""
    print("\n=== RINGKASAN DATA SISWA ===")
    print("=" * 40)
    print(f"{'Keterangan':<24} | {'Hasil':<11}")
    print("-" * 40)
    print(f"{'Jumlah seluruh siswa':<24} | {len(data)}")
    print(f"{'Rata-rata jam belajar':<24} | {rata_rata(data, 'Hours_Studied'):.2f} jam")
    print(f"{'Rata-rata kehadiran':<24} | {rata_rata(data, 'Attendance'):.2f} %")
    print(f"{'Rata-rata durasi tidur':<24} | {rata_rata(data, 'Sleep_Hours'):.2f} jam")
    print(f"{'Rata-rata nilai ujian':<24} | {rata_rata(data, 'Exam_Score'):.2f}")
    print("=" * 40)


def cetak_kelompok(nama, daftar_nilai):
    """Fungsi mencetak satu baris tabel kelompok durasi belajar."""
    if len(daftar_nilai) > 0:
        rata = round(sum(daftar_nilai) / len(daftar_nilai), 2)
    else:
        rata = "-"
    print(f"{nama:<28} | {len(daftar_nilai):>12} | {rata:>15}")


def analisis_belajar(data):
    """Fungsi menganalisis nilai berdasarkan durasi belajar."""
    rendah = []
    sedang = []
    tinggi = []

    for row in data:
        if row["Hours_Studied"] <= 2:
            rendah.append(row["Exam_Score"])
        elif row["Hours_Studied"] <= 5:
            sedang.append(row["Exam_Score"])
        else:
            tinggi.append(row["Exam_Score"])

    print("\n=== ANALISIS DURASI BELAJAR ===")
    print("=" * 64)
    print(f"{'Kelompok':<28} | {'Jumlah Siswa':>12} | {'Rata-rata Nilai':>15}")
    print("-" * 64)
    cetak_kelompok("Belajar rendah (<= 2 jam)", rendah)
    cetak_kelompok("Belajar sedang (3-5 jam)", sedang)
    cetak_kelompok("Belajar tinggi (> 5 jam)", tinggi)
    print("=" * 64)


def kelompok_nilai(data):
    """Fungsi mengelompokkan siswa berdasarkan kategori hasil ujian."""
    tinggi = 0
    sedang = 0
    rendah = 0

    for row in data:
        if row["Kategori"] == "Tinggi":
            tinggi += 1
        elif row["Kategori"] == "Sedang":
            sedang += 1
        else:
            rendah += 1

    print("\n=== PENGELOMPOKAN HASIL UJIAN ===")
    print("=" * 40)
    print(f"{'Kategori':<24} | {'Jumlah Siswa':>12}")
    print("-" * 40)
    print(f"{'Nilai tinggi (>= 85)':<24} | {tinggi:>12}")
    print(f"{'Nilai sedang (70-84)':<24} | {sedang:>12}")
    print(f"{'Perlu perhatian (< 70)':<24} | {rendah:>12}")
    print("=" * 40)

# --- FITUR UTAMA ---
def cetak_daftar(judul, daftar, kosong):
    """Fungsi mencetak daftar poin, atau teks pengganti jika daftar kosong."""
    print(f"\n=== {judul} ===")
    if len(daftar) == 0:
        print("- " + kosong)
    for isi in daftar:
        print("- " + isi)


def tampilkan_rekap_siswa(nomor, siswa):
    """Fungsi memformat dan menampilkan rekap evaluasi satu siswa ke terminal."""
    selisih = siswa["Exam_Score"] - siswa["Previous_Scores"]

    print(f"\n=== REKAP EVALUASI SISWA NO. {nomor} ===")
    print("=" * 34)
    print(f"{'Aspek':<20} | {'Hasil':<10}")
    print("-" * 34)
    print(f"{'Jam belajar':<20} | {siswa['Hours_Studied']} jam")
    print(f"{'Kehadiran':<20} | {siswa['Attendance']} %")
    print(f"{'Nilai sebelumnya':<20} | {siswa['Previous_Scores']}")
    print(f"{'Durasi tidur':<20} | {siswa['Sleep_Hours']} jam")
    print(f"{'Sesi bimbingan':<20} | {siswa['Tutoring_Sessions']}")
    print(f"{'Motivasi':<20} | {siswa['Motivation_Level']}")
    print(f"{'Aktivitas fisik':<20} | {siswa['Physical_Activity']}")
    print(f"{'Nilai ujian':<20} | {siswa['Exam_Score']}")
    print("=" * 34)

    print("Kategori nilai:", siswa["Kategori"])

    if selisih > 0:
        print(f"Perubahan nilai: naik {selisih} poin dari nilai sebelumnya.")
    elif selisih < 0:
        print(f"Perubahan nilai: turun {abs(selisih)} poin dari nilai sebelumnya.")
    else:
        print("Perubahan nilai: tetap sama dengan nilai sebelumnya.")


def rekomendasi_siswa(siswa):
    """Fungsi menampilkan kebiasaan baik dan rekomendasi untuk siswa."""
    jam = siswa["Hours_Studied"]
    hadir = siswa["Attendance"]
    tidur = siswa["Sleep_Hours"]
    bimbingan = siswa["Tutoring_Sessions"]
    fisik = siswa["Physical_Activity"]
    nilai = siswa["Exam_Score"]
    sebelumnya = siswa["Previous_Scores"]
    motivasi = siswa["Motivation_Level"]

    baik = []
    saran = []

    # kebiasaan yang sudah baik
    if hadir >= 80:
        baik.append("Kehadiranmu sudah baik, pertahankan agar tidak tertinggal materi.")
    if tidur >= 7:
        baik.append("Waktu tidurmu sudah cukup, ini membantu konsentrasi saat belajar.")
    if motivasi == "High":
        baik.append("Motivasi belajarmu tinggi, manfaatkan untuk menjaga konsistensi belajar.")
    if bimbingan > 0:
        baik.append("Kamu sudah mengikuti sesi bimbingan, lanjutkan agar materi yang sulit terbantu.")
    if fisik > 0:
        baik.append("Kamu masih menyempatkan aktivitas fisik, ini baik untuk menjaga kebugaran.")
    if nilai > sebelumnya:
        baik.append("Nilai ujianmu naik dibanding nilai sebelumnya, tandanya usahamu mulai membuahkan hasil.")

    # hal yang perlu diperbaiki
    if jam < 3:
        saran.append("Jam belajarmu masih sedikit. Coba buat jadwal belajar harian yang tetap, walaupun dimulai dari waktu singkat.")
    if hadir < 80:
        saran.append("Kehadiranmu di bawah 80%. Usahakan lebih rutin masuk kelas karena materi yang terlewat bisa menumpuk.")
    if tidur < 7:
        saran.append("Waktu tidurmu kurang dari 7 jam. Atur jam tidur agar tubuh dan pikiran cukup istirahat sebelum belajar.")
    if motivasi == "Low":
        saran.append("Motivasi belajarmu rendah. Tentukan target nilai yang jelas dan belajar bersama teman agar lebih semangat.")
    if bimbingan == 0:
        saran.append("Kamu belum mengikuti sesi bimbingan. Coba ikut, terutama untuk pelajaran yang terasa sulit.")
    if fisik == 0:
        saran.append("Kamu belum punya aktivitas fisik. Olahraga ringan secara rutin bisa membantu fokus dan menjaga kondisi tubuh.")
    if nilai < sebelumnya:
        saran.append("Nilai ujianmu turun dibanding nilai sebelumnya. Coba evaluasi bagian materi yang paling sulit dan ulangi lebih awal.")
    if nilai < 70:
        saran.append("Nilai ujianmu masih di bawah 70. Konsultasikan dengan guru agar mendapat bantuan sesuai kebutuhanmu.")

    cetak_daftar("KEBIASAAN YANG SUDAH BAIK", baik,
                 "Belum ada kebiasaan yang menonjol. Mulai dari perbaikan kecil terlebih dahulu.")
    cetak_daftar("REKOMENDASI UNTUK SISWA", saran,
                 "Kebiasaan belajarmu sudah baik. Pertahankan dan terus evaluasi secara berkala.")


def evaluasi_guru(data):
    """Fungsi menampilkan evaluasi akademik dan rekomendasi untuk guru."""
    jumlah = len(data)
    nilai = rata_rata(data, "Exam_Score")
    hadir = rata_rata(data, "Attendance")

    # menghitung siswa pada tiap kondisi
    nomor_rendah = []
    hadir_rendah = 0
    tidur_kurang = 0
    belajar_singkat = 0
    motivasi_rendah = 0
    tanpa_bimbingan = 0
    nomor = 0

    for row in data:
        nomor += 1

        if row["Exam_Score"] < 70:
            nomor_rendah.append(nomor)
        if row["Attendance"] < 80:
            hadir_rendah += 1
        if row["Sleep_Hours"] < 7:
            tidur_kurang += 1
        if row["Hours_Studied"] < 3:
            belajar_singkat += 1
        if row["Motivation_Level"] == "Low":
            motivasi_rendah += 1
        if row["Tutoring_Sessions"] == 0:
            tanpa_bimbingan += 1

    jumlah_rendah = len(nomor_rendah)
    persentase = jumlah_rendah / jumlah * 100

    # tabel siswa yang perlu diperhatikan
    print("\n=== SISWA YANG PERLU DIPERHATIKAN ===")
    print("=" * 54)
    print(f"{'Kondisi':<30} | {'Jumlah':>6} | {'Persen':>8}")
    print("-" * 54)
    print(f"{'Nilai ujian di bawah 70':<30} | {jumlah_rendah:>6} | {jumlah_rendah / jumlah * 100:>7.2f}%")
    print(f"{'Kehadiran di bawah 80 %':<30} | {hadir_rendah:>6} | {hadir_rendah / jumlah * 100:>7.2f}%")
    print(f"{'Tidur kurang dari 7 jam':<30} | {tidur_kurang:>6} | {tidur_kurang / jumlah * 100:>7.2f}%")
    print(f"{'Jam belajar kurang dari 3 jam':<30} | {belajar_singkat:>6} | {belajar_singkat / jumlah * 100:>7.2f}%")
    print(f"{'Motivasi belajar rendah':<30} | {motivasi_rendah:>6} | {motivasi_rendah / jumlah * 100:>7.2f}%")
    print(f"{'Belum ikut sesi bimbingan':<30} | {tanpa_bimbingan:>6} | {tanpa_bimbingan / jumlah * 100:>7.2f}%")
    print("=" * 54)

    print("\n=== 5 SISWA DENGAN NILAI TERENDAH ===")
    print("=" * 26)
    print(f"{'No. Data':<10} | {'Nilai Ujian':>11}")
    print("-" * 26)

    sudah = []
    for urutan in range(5):
        nomor_min = 0
        nilai_min = 1000
        nomor = 0
        for row in data:
            nomor += 1
            if nomor not in sudah and row["Exam_Score"] < nilai_min:
                nilai_min = row["Exam_Score"]
                nomor_min = nomor
        sudah.append(nomor_min)
        print(f"{nomor_min:<10} | {nilai_min:>11}")
    print("=" * 26)

    # kategori rata-rata nilai, ditulis dengan huruf kecil
    kategori = kategori_nilai(nilai)
    if kategori == "Tinggi":
        kata_kategori = "tinggi"
    elif kategori == "Sedang":
        kata_kategori = "sedang"
    else:
        kata_kategori = "perlu perhatian"

    print("\n=== KESIMPULAN ===")
    print(f"Rata-rata nilai ujian siswa adalah {nilai:.2f} (kategori {kata_kategori}), dengan {jumlah_rendah} dari {jumlah} siswa ({persentase:.2f}%) memperoleh nilai di bawah 70.")

    # rekomendasi untuk guru
    rekomendasi = []

    if nilai < 70:
        rekomendasi.append("Rata-rata nilai kelas masih di bawah 70. Materi yang belum dipahami siswa perlu diulas kembali dan metode pembelajaran sebaiknya dievaluasi.")
    elif nilai < 85:
        rekomendasi.append("Rata-rata nilai berada pada kategori sedang. Latihan tambahan dapat membantu siswa mencapai kategori tinggi.")

    if persentase >= 50:
        rekomendasi.append("Lebih dari separuh siswa memperoleh nilai di bawah 70. Pertimbangkan pembelajaran remedial atau pendampingan khusus bagi siswa tersebut.")
    elif jumlah_rendah > 0:
        rekomendasi.append("Sebagian siswa masih memperoleh nilai di bawah 70. Beri perhatian lebih pada siswa tersebut melalui pendampingan secara berkala.")

    if hadir < 80:
        rekomendasi.append("Rata-rata kehadiran masih rendah. Telusuri penyebab siswa tidak hadir agar tidak tertinggal materi.")
    elif hadir_rendah > 0:
        rekomendasi.append(f"Ada {hadir_rendah} siswa dengan kehadiran di bawah 80%. Perlu dilakukan pendekatan agar mereka lebih rutin mengikuti pelajaran.")

    if tidur_kurang > 0:
        rekomendasi.append(f"Ada {tidur_kurang} siswa yang tidur kurang dari 7 jam. Ingatkan pentingnya istirahat agar konsentrasi saat belajar tetap terjaga.")

    if motivasi_rendah > 0:
        rekomendasi.append(f"Ada {motivasi_rendah} siswa dengan motivasi belajar rendah. Pendekatan personal dan target belajar yang jelas dapat membantu meningkatkan semangat mereka.")

    if tanpa_bimbingan > 0:
        rekomendasi.append(f"Ada {tanpa_bimbingan} siswa yang belum mengikuti sesi bimbingan. Dorong mereka untuk ikut, terutama yang nilainya masih rendah.")

    if belajar_singkat > 0:
        rekomendasi.append(f"Ada {belajar_singkat} siswa dengan jam belajar kurang dari 3 jam. Bantu mereka menyusun jadwal belajar yang lebih teratur.")

    cetak_daftar("REKOMENDASI UNTUK GURU", rekomendasi,
                 "Kebiasaan belajar dan hasil akademik siswa sudah baik. Pertahankan proses pembelajaran dan lakukan pemantauan secara berkala.")


def ubah_data_siswa(data):
    """Fungsi mengubah satu aspek data siswa dan menyimpannya ke file CSV."""
    print("\n========== UBAH DATA SISWA ==========")
    print("Jumlah data siswa tersedia:", len(data))

    try:
        nomor = int(input("Masukkan nomor data siswa: "))
    except ValueError:
        print("[ERROR] Nomor data harus berupa angka!")
        return

    if nomor < 1 or nomor > len(data):
        print("[ERROR] Nomor data tidak tersedia.")
        return

    siswa = data[nomor - 1]

    print(f"\nData siswa nomor {nomor} saat ini:")
    for i in range(len(NAMA_ASPEK)):
        print(f"{i + 1}. {NAMA_ASPEK[i]:<18}: {siswa[KOLOM_ASPEK[i]]}")

    try:
        pilihan = int(input("Pilih aspek yang diubah: "))
    except ValueError:
        print("[ERROR] Pilihan harus berupa angka!")
        return

    if pilihan < 1 or pilihan > len(NAMA_ASPEK):
        print("[ERROR] Pilihan aspek tidak tersedia.")
        return

    nama = NAMA_ASPEK[pilihan - 1]
    kolom = KOLOM_ASPEK[pilihan - 1]
    nilai_baru = input(f"Masukkan nilai baru untuk {nama}: ")

    if not validasi_nilai_baru(kolom, nilai_baru):
        print("[GAGAL] Proses dihentikan karena data input tidak valid.")
        return

    # semua kolom selain motivasi berisi angka
    if kolom != "Motivation_Level":
        nilai_baru = int(nilai_baru)

    yakin = input(f"Ubah {nama} dari {siswa[kolom]} menjadi {nilai_baru}? (y/n): ")
    if yakin != "y" and yakin != "Y":
        print("Perubahan dibatalkan.")
        return

    if not simpan_ke_csv(siswa["Baris_CSV"], kolom, str(nilai_baru)):
        print("[GAGAL] Data tidak diubah.")
        return

    # perbarui data di program agar analisis langsung memakai nilai baru
    siswa[kolom] = nilai_baru
    siswa["Kategori"] = kategori_nilai(siswa["Exam_Score"])

    print("[BERHASIL] Data berhasil diubah dan disimpan ke file CSV.")


# --- MENU ---
def evaluasi_siswa(data):
    """Fungsi menampilkan hasil evaluasi untuk satu siswa."""
    print("\n======== LIHAT HASIL EVALUASI ========")
    print("Jumlah data siswa tersedia:", len(data))

    try:
        nomor = int(input("Masukkan nomor data siswa: "))
    except ValueError:
        print("[ERROR] Nomor data harus berupa angka!")
        return

    if nomor < 1 or nomor > len(data):
        print("[ERROR] Nomor data tidak tersedia.")
        return

    tampilkan_rekap_siswa(nomor, data[nomor - 1])
    rekomendasi_siswa(data[nomor - 1])


def menu_siswa(data):
    """Fungsi menampilkan menu untuk siswa."""
    while True:
        print("\n======== MENU SISWA ========")
        print("1. Lihat Hasil Evaluasi")
        print("2. Ubah Data Kebiasaan")
        print("3. Kembali")

        pilihan = input("Pilihan menu: ")

        if pilihan == "1":
            evaluasi_siswa(data)
        elif pilihan == "2":
            ubah_data_siswa(data)
        elif pilihan == "3":
            break
        else:
            print("[ERROR] Pilihan tidak valid.")


def menu_guru(data):
    """Fungsi menampilkan untuk menu guru."""
    while True:
        print("\n ======= MENU GURU ========")
        print("1. Ringkasan Data Siswa")
        print("2. Analisis Durasi Belajar")
        print("3. Pengelompokkan Hasil Ujian")
        print("4. Evalluasi dan Rekomendasi")
        print("5. Kembali")

        pilihan = input("Pilihan menu: ")

        if pilihan == "1":
            ringkasan_data(data)
        elif pilihan == "2":
            analisis_belajar(data)
        elif pilihan == "3":
            kelompok_nilai(data)
        elif pilihan == "4":
            evaluasi_guru(data)
        elif pilihan == "5":
            break
        else:
            print("[ERROR] Pilihan tidak valid.")


def main():
    data = baca_data()

    if len(data) == 0:
        print("\nError: Dataset kosong atau tidak memiliki data yang valid.")
        return

    while True:
        print("\n==============================")
        print("PROGRAM ANALISIS KEBIASAN BELAJAR")
        print("==============================")
        print("1. Masuk Sebagai Siswa")
        print("2. Masuk Sebagai Guru")
        print("3. Keluar")

        pilihan = input("Pilih pengguna: ")

        if pilihan == "1":
            menu_siswa(data)
        elif pilihan == "2":
            menu_guru(data)
        elif pilihan == "3":
            print("Program Selesai. Terima Kasih.")
            break
        else:
            print("[ERROR] Pilihan tidak vaild.")


if __name__ == "__main__":
    main()
