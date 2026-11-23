# Program Analisis Hubungan Kebiasaan Belajar dengan Hasil Akademik Siswa SMA

## Deskripsi
Program ini dibuat dengan bahasa Python untuk menganalisis hubungan antara kebiasaan belajar dan hasil akademik siswa SMA. Program membaca data siswa dari file CSV, memeriksa apakah datanya valid, lalu mengolahnya menjadi ringkasan, pengelompokan, evaluasi, dan rekomendasi.

Program memiliki dua jenis pengguna:
- Siswa, untuk melihat rekap dan saran perbaikan kebiasaan belajarnya sendiri.
- Guru, untuk memantau kondisi seluruh siswa dan mendapat rekomendasi pembelajaran.

## Latar Belakang
Banyak siswa bingung bagaimana mengubah kebiasaan belajar dan apa yang harus dilakukan agar nilai akademiknya lebih baik. Di sisi lain, guru kesulitan memantau kebiasaan belajar siswa satu per satu. Program ini dibuat untuk membantu keduanya dengan melihat data kebiasaan belajar dan hasil ujian secara terstruktur.

## Tujuan
1. Mengetahui gambaran umum kebiasaan belajar dan nilai ujian siswa.
2. Melihat perbedaan nilai ujian pada siswa dengan durasi belajar yang berbeda.
3. Mengelompokkan siswa berdasarkan hasil ujian.
4. Memberikan rekomendasi yang sesuai untuk siswa maupun guru.

## Fitur

### Menu Siswa
Siswa memasukkan nomor datanya, lalu program menampilkan:
- Rekap evaluasi: jam belajar, kehadiran, nilai sebelumnya, durasi tidur, sesi bimbingan, motivasi, aktivitas fisik, dan nilai ujian.
- Kategori nilai dan perubahan nilai (naik, turun, atau tetap) dibanding nilai sebelumnya.
- Kebiasaan yang sudah baik dan rekomendasi perbaikan.

### Menu Guru
1. Ringkasan Data Siswa: jumlah siswa serta rata-rata jam belajar, kehadiran, durasi tidur, dan nilai ujian.
2. Analisis Durasi Belajar: jumlah siswa dan rata-rata nilai pada kelompok belajar rendah, sedang, dan tinggi.
3. Pengelompokan Hasil Ujian: jumlah siswa pada kategori nilai tinggi, sedang, dan perlu perhatian.
4. Evaluasi dan Rekomendasi: tabel kondisi siswa yang perlu diperhatikan, 5 siswa dengan nilai ujian terendah, kesimpulan, dan rekomendasi untuk guru.

## Dataset
Data diambil dari file `StudentPerformanceFactors.csv`. Program hanya membaca maksimal 300 data yang valid.

Kolom yang digunakan:
- `Hours_Studied`: jumlah jam belajar
- `Attendance`: persentase kehadiran
- `Previous_Scores`: nilai sebelumnya
- `Sleep_Hours`: durasi tidur (jam)
- `Tutoring_Sessions`: jumlah sesi bimbingan yang diikuti
- `Motivation_Level`: tingkat motivasi belajar (Low, Medium, High)
- `Physical_Activity`: aktivitas fisik
- `Exam_Score`: nilai ujian

## Aturan Pengolahan Data

### Validasi data
Program menampilkan pesan error atau peringatan jika:
- file CSV tidak ditemukan,
- file tidak memiliki header,
- ada kolom wajib yang tidak ada,
- nilai pada kolom angka bukan bilangan bulat, atau bernilai negatif (baris tersebut dilewati).

### Kategori nilai ujian
- Nilai 85 ke atas: Tinggi
- Nilai 70 sampai 84: Sedang
- Nilai di bawah 70: Perlu Perhatian

### Kelompok durasi belajar
- 2 jam atau kurang: Rendah
- 3 sampai 5 jam: Sedang
- Lebih dari 5 jam: Tinggi

### Dasar rekomendasi
Rekomendasi muncul berdasarkan kondisi berikut:
- kehadiran minimal 80%,
- tidur minimal 7 jam,
- motivasi belajar (high atau low),
- mengikuti sesi bimbingan atau belum,
- ada aktivitas fisik atau belum,
- nilai ujian naik atau turun dibanding nilai sebelumnya,
- jam belajar kurang dari 3 jam,
- nilai ujian di bawah 70.

## Cara Kerja Program
1. Program membaca dan memvalidasi data dari file CSV (`baca_data`).
2. Setiap siswa diberi kategori nilai (`kategori_nilai`).
3. Pengguna memilih masuk sebagai siswa atau guru.
4. Program menjalankan analisis atau evaluasi sesuai menu yang dipilih, lalu menampilkan hasilnya di terminal.

## Cara Menjalankan

1. Pastikan Python sudah terpasang di komputer.
2. Unduh file `program analisis.py` dan `StudentPerformanceFactors.csv`.
3. Simpan kedua file tersebut dalam folder yang sama agar program dapat menemukan file CSV secara otomatis.
4. Buka terminal pada folder tempat kedua file disimpan.
5. Jalankan program menggunakan perintah berikut:
   python "program analisis.py"
6. Pilih pengguna pada menu utama:
   - `1` untuk masuk sebagai siswa.
   - `2` untuk masuk sebagai guru.
   - `3` untuk keluar dari program.

## Struktur File
- `program analisis.py`: kode program utama
- `StudentPerformanceFactors.csv`: dataset siswa
- `README.md`: dokumentasi proyek

## Anggota Kelompok
1. Cherry Sandra: fitur utama
2. Liyana Maziya Fadhlani: fitur analisis
3. Belva Fitriyah Arzeti Putri: fitur menu
4. Asy Syifa Ramadhani Putri Indrianto: fitur dataset