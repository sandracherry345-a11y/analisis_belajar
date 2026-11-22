import csv
import os

FILE_CSV = r"c:\Users\USER\Downloads\StudentPerformanceFactors.csv"

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

KOLOM_ANGKA = [kolom for kolom in KOLOM_WAJIB if kolom != "Motivation_Level"]


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

        kolom_hilang = [kolom for kolom in KOLOM_WAJIB if kolom not in reader.fieldnames]
        if len(kolom_hilang) > 0:
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

            if any(row[kolom] < 0 for kolom in KOLOM_ANGKA):
                print(f"Peringatan baris {nomor_baris}: nilai numerik tidak boleh bernilai negatif.")
                continue

            row["Kategori"] = kategori_nilai(row["Exam_Score"])
            data.append(row)

            if len(data) == 300:
                break

# --- ANALISIS ---


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

    aspek = [
        ("Jam belajar", f"{siswa['Hours_Studied']} jam"),
        ("Kehadiran", f"{siswa['Attendance']} %"),
        ("Nilai sebelumnya", siswa["Previous_Scores"]),
        ("Durasi tidur", f"{siswa['Sleep_Hours']} jam"),
        ("Sesi bimbingan", siswa["Tutoring_Sessions"]),
        ("Motivasi", siswa["Motivation_Level"]),
        ("Aktivitas fisik", siswa["Physical_Activity"]),
        ("Nilai ujian", siswa["Exam_Score"])
    ]

    print(f"\n=== REKAP EVALUASI SISWA NO. {nomor} ===")
    print("=" * 34)
    print(f"{'Aspek':<20} | {'Hasil':<10}")
    print("-" * 34)
    for nama, hasil in aspek:
        print(f"{nama:<20} | {hasil}")
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
    motivasi = siswa["Motivation_Level"].strip().lower()

    # setiap pasangan berisi (kondisi, pesan)
    kebiasaan = [
        (hadir >= 80, "Kehadiranmu sudah baik, pertahankan agar tidak tertinggal materi."),
        (tidur >= 7, "Waktu tidurmu sudah cukup, ini membantu konsentrasi saat belajar."),
        (motivasi == "high", "Motivasi belajarmu tinggi, manfaatkan untuk menjaga konsistensi belajar."),
        (bimbingan > 0, "Kamu sudah mengikuti sesi bimbingan, lanjutkan agar materi yang sulit terbantu."),
        (fisik > 0, "Kamu masih menyempatkan aktivitas fisik, ini baik untuk menjaga kebugaran."),
        (nilai > sebelumnya, "Nilai ujianmu naik dibanding nilai sebelumnya, tandanya usahamu mulai membuahkan hasil.")
    ]

    perbaikan = [
        (jam < 3, "Jam belajarmu masih sedikit. Coba buat jadwal belajar harian yang tetap, walaupun dimulai dari waktu singkat."),
        (hadir < 80, "Kehadiranmu di bawah 80%. Usahakan lebih rutin masuk kelas karena materi yang terlewat bisa menumpuk."),
        (tidur < 7, "Waktu tidurmu kurang dari 7 jam. Atur jam tidur agar tubuh dan pikiran cukup istirahat sebelum belajar."),
        (motivasi == "low", "Motivasi belajarmu rendah. Tentukan target nilai yang jelas dan belajar bersama teman agar lebih semangat."),
        (bimbingan == 0, "Kamu belum mengikuti sesi bimbingan. Coba ikut, terutama untuk pelajaran yang terasa sulit."),
        (fisik == 0, "Kamu belum punya aktivitas fisik. Olahraga ringan secara rutin bisa membantu fokus dan menjaga kondisi tubuh."),
        (nilai < sebelumnya, "Nilai ujianmu turun dibanding nilai sebelumnya. Coba evaluasi bagian materi yang paling sulit dan ulangi lebih awal."),
        (nilai < 70, "Nilai ujianmu masih di bawah 70. Konsultasikan dengan guru agar mendapat bantuan sesuai kebutuhanmu.")
    ]

    baik = [pesan for kondisi, pesan in kebiasaan if kondisi]
    saran = [pesan for kondisi, pesan in perbaikan if kondisi]

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
    nomor_rendah = [nomor for nomor, row in enumerate(data, start=1) if row["Exam_Score"] < 70]
    jumlah_rendah = len(nomor_rendah)
    hadir_rendah = sum(1 for row in data if row["Attendance"] < 80)
    tidur_kurang = sum(1 for row in data if row["Sleep_Hours"] < 7)
    belajar_singkat = sum(1 for row in data if row["Hours_Studied"] < 3)
    motivasi_rendah = sum(1 for row in data if row["Motivation_Level"].strip().lower() == "low")
    tanpa_bimbingan = sum(1 for row in data if row["Tutoring_Sessions"] == 0)
    persentase = jumlah_rendah / jumlah * 100

    kondisi = [
        ("Nilai ujian di bawah 70", jumlah_rendah),
        ("Kehadiran di bawah 80 %", hadir_rendah),
        ("Tidur kurang dari 7 jam", tidur_kurang),
        ("Jam belajar kurang dari 3 jam", belajar_singkat),
        ("Motivasi belajar rendah", motivasi_rendah),
        ("Belum ikut sesi bimbingan", tanpa_bimbingan)
    ]

    # tabel siswa yang perlu diperhatikan
    print("\n=== SISWA YANG PERLU DIPERHATIKAN ===")
    print("=" * 54)
    print(f"{'Kondisi':<30} | {'Jumlah':>6} | {'Persen':>8}")
    print("-" * 54)
    for nama, banyak in kondisi:
        print(f"{nama:<30} | {banyak:>6} | {banyak / jumlah * 100:>7.2f}%")
    print("=" * 54)

    print("Nomor data siswa dengan nilai di bawah 70:")
    if jumlah_rendah > 0:
        print(", ".join(str(n) for n in nomor_rendah))
    else:
        print("Tidak ada")

    print("\n=== KESIMPULAN ===")
    print(f"Rata-rata nilai ujian siswa adalah {nilai:.2f} (kategori {kategori_nilai(nilai).lower()}), dengan {jumlah_rendah} dari {jumlah} siswa ({persentase:.2f}%) memperoleh nilai di bawah 70.")

    # rekomendasi untuk guru, setiap pasangan berisi (kondisi, pesan)
    daftar = [
        (nilai < 70, "Rata-rata nilai kelas masih di bawah 70. Materi yang belum dipahami siswa perlu diulas kembali dan metode pembelajaran sebaiknya dievaluasi."),
        (70 <= nilai < 85, "Rata-rata nilai berada pada kategori sedang. Latihan tambahan dapat membantu siswa mencapai kategori tinggi."),
        (persentase >= 50, "Lebih dari separuh siswa memperoleh nilai di bawah 70. Pertimbangkan pembelajaran remedial atau pendampingan khusus bagi siswa tersebut."),
        (0 < persentase < 50, "Sebagian siswa masih memperoleh nilai di bawah 70. Beri perhatian lebih pada siswa tersebut melalui pendampingan secara berkala."),
        (hadir < 80, "Rata-rata kehadiran masih rendah. Telusuri penyebab siswa tidak hadir agar tidak tertinggal materi."),
        (hadir >= 80 and hadir_rendah > 0, f"Ada {hadir_rendah} siswa dengan kehadiran di bawah 80%. Perlu dilakukan pendekatan agar mereka lebih rutin mengikuti pelajaran."),
        (tidur_kurang > 0, f"Ada {tidur_kurang} siswa yang tidur kurang dari 7 jam. Ingatkan pentingnya istirahat agar konsentrasi saat belajar tetap terjaga."),
        (motivasi_rendah > 0, f"Ada {motivasi_rendah} siswa dengan motivasi belajar rendah. Pendekatan personal dan target belajar yang jelas dapat membantu meningkatkan semangat mereka."),
        (tanpa_bimbingan > 0, f"Ada {tanpa_bimbingan} siswa yang belum mengikuti sesi bimbingan. Dorong mereka untuk ikut, terutama yang nilainya masih rendah."),
        (belajar_singkat > 0, f"Ada {belajar_singkat} siswa dengan jam belajar kurang dari 3 jam. Bantu mereka menyusun jadwal belajar yang lebih teratur.")
    ]
    rekomendasi = [pesan for syarat, pesan in daftar if syarat]

    cetak_daftar("REKOMENDASI UNTUK GURU", rekomendasi,
                 "Kebiasaan belajar dan hasil akademik siswa sudah baik. Pertahankan proses pembelajaran dan lakukan pemantauan secara berkala.")


# --- MENU ---