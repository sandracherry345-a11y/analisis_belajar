# Program Analisis Hubungan Kebiasaan Belajar dengan Hasil Akademik

## Fitur

### Menu Siswa
Setelah masuk sebagai siswa, tersedia dua pilihan:

**1. Lihat Hasil Evaluasi**

Siswa memasukkan nomor datanya, lalu program menampilkan:
- Rekap evaluasi: jam belajar, kehadiran, nilai sebelumnya, durasi tidur, sesi bimbingan, motivasi, aktivitas fisik, dan nilai ujian.
- Kategori nilai dan perubahan nilai (naik, turun, atau tetap) dibanding nilai sebelumnya.
- Kebiasaan yang sudah baik dan rekomendasi perbaikan.

**2. Ubah Data Kebiasaan**

Siswa dapat mengubah satu aspek datanya, lalu perubahan tersimpan otomatis ke file CSV. Langkahnya:
1. Masukkan nomor data siswa.
2. Program menampilkan data siswa tersebut saat ini.
3. Pilih aspek yang ingin diubah: jam belajar, kehadiran, nilai sebelumnya, durasi tidur, sesi bimbingan, motivasi, aktivitas fisik, atau nilai ujian.
4. Masukkan nilai baru. Program memeriksa apakah nilai tersebut valid.
5. Jawab `y` untuk menyimpan atau `n` untuk membatalkan.
6. Jika disimpan, file CSV langsung berubah. Hasil evaluasi berikutnya sudah memakai nilai yang baru, tanpa perlu menjalankan ulang program.

Hanya satu nilai yang berubah. Data siswa lain dan kolom lain di file CSV tidak ikut berubah.

### Menu Guru
1. Ringkasan Data Siswa: jumlah siswa serta rata-rata jam belajar, kehadiran, durasi tidur, dan nilai ujian.
2. Analisis Durasi Belajar: jumlah siswa dan rata-rata nilai pada kelompok belajar rendah, sedang, dan tinggi.
3. Pengelompokan Hasil Ujian: jumlah siswa pada kategori nilai tinggi, sedang, dan perlu perhatian.
4. Evaluasi dan Rekomendasi: tabel kondisi siswa yang perlu diperhatikan, 5 siswa dengan nilai ujian terendah, kesimpulan, dan rekomendasi untuk guru.

Karena data yang diubah siswa langsung tersimpan, laporan guru selalu memakai data yang terbaru.

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

### Validasi saat mengubah data
Perubahan ditolak dan file CSV tidak berubah jika:
- nomor data atau pilihan aspek bukan angka, atau tidak tersedia,
- nilai baru bukan bilangan bulat atau bernilai negatif,
- kehadiran, nilai sebelumnya, atau nilai ujian lebih dari 100,
- durasi tidur lebih dari 24 jam,
- motivasi selain `Low`, `Medium`, atau `High` (huruf pertama harus kapital).

Jika siswa menjawab `n` pada konfirmasi, perubahan dibatalkan. Jika file CSV gagal disimpan (misalnya sedang dibuka di Excel), program menampilkan pesan error dan isi file tidak rusak.

### Kategori nilai ujian
- Nilai 85 ke atas: Tinggi
- Nilai 70 sampai 84: Sedang
- Nilai di bawah 70: Perlu Perhatian

Jika siswa mengubah nilai ujian, kategorinya dihitung ulang.

### Kelompok durasi belajar
- 2 jam atau kurang: Rendah
- 3 sampai 5 jam: Sedang
- Lebih dari 5 jam: Tinggi

## Cara Kerja Program
1. Program membaca dan memvalidasi data dari file CSV (`baca_data`). Setiap data juga mencatat baris aslinya di file CSV.
2. Setiap siswa diberi kategori nilai (`kategori_nilai`).
3. Pengguna memilih masuk sebagai siswa atau guru.
4. Program menjalankan analisis atau evaluasi sesuai menu yang dipilih, lalu menampilkan hasilnya di terminal.
5. Jika siswa mengubah data (`ubah_data_siswa`), nilai baru diperiksa (`validasi_nilai_baru`), disimpan ke file CSV (`simpan_ke_csv`), lalu data di program diperbarui agar analisis berikutnya memakai nilai yang baru.

## Cara Menjalankan

1. Pastikan Python sudah terpasang di komputer.
2. Unduh file `program analisis.py` dan `StudentPerformanceFactors.csv`.
3. Simpan kedua file tersebut dalam folder yang sama agar program dapat menemukan file CSV secara otomatis.
4. Pastikan file CSV tidak sedang dibuka di Excel.
5. Buka terminal pada folder tempat kedua file disimpan.
6. Jalankan program menggunakan perintah berikut:
   python "program analisis.py"
7. Pilih pengguna pada menu utama:
   - `1` untuk masuk sebagai siswa.
   - `2` untuk masuk sebagai guru.
   - `3` untuk keluar dari program.

## Struktur File
- `program analisis.py`: kode program utama
- `StudentPerformanceFactors.csv`: dataset siswa
- `README.md`: dokumentasi proyek
