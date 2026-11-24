# Program Analisis Hubungan Kebiasaan Belajar dengan Hasil Akademik

## Deskripsi
Program ini dibuat dengan bahasa Python untuk menganalisis hubungan antara kebiasaan belajar dan hasil akademik siswa SMA. Program membaca data siswa dari file CSV, memeriksa apakah datanya valid, lalu mengolahnya menjadi ringkasan, pengelompokan, evaluasi, dan rekomendasi.

Program memiliki dua jenis pengguna:
- Siswa, untuk melihat rekap dan saran perbaikan kebiasaan belajarnya sendiri, serta memperbarui data kebiasaannya jika sudah berubah.
- Guru, untuk memantau kondisi seluruh siswa dan mendapat rekomendasi pembelajaran.

## Latar Belakang
Banyak siswa bingung bagaimana mengubah kebiasaan belajar dan apa yang harus dilakukan agar nilai akademiknya lebih baik. Di sisi lain, guru kesulitan memantau kebiasaan belajar siswa satu per satu. Program ini dibuat untuk membantu keduanya dengan melihat data kebiasaan belajar dan hasil ujian secara terstruktur.

Kebiasaan siswa juga bisa berubah setelah siswa memperbaikinya, misalnya jadwal tidur yang sebelumnya buruk menjadi lebih baik. Karena itu program menyediakan fitur untuk mengubah data siswa, dan perubahan tersebut langsung tersimpan di file CSV tanpa perlu membuka file secara manual.

## Tujuan
1. Mengetahui gambaran umum kebiasaan belajar dan nilai ujian siswa.
2. Melihat perbedaan nilai ujian pada siswa dengan durasi belajar yang berbeda.
3. Mengelompokkan siswa berdasarkan hasil ujian.
4. Memberikan rekomendasi yang sesuai untuk siswa maupun guru.
5. Memungkinkan siswa memperbarui data kebiasaannya, sehingga analisis berikutnya memakai data yang terbaru.

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

Catatan:
- Nomor data siswa adalah urutan data yang valid, bukan nomor baris di file CSV. Jika ada baris yang rusak dan dilewati, nomor data tetap berurutan.
- Fitur Ubah Data Kebiasaan mengubah isi file `StudentPerformanceFactors.csv` secara permanen. Simpan salinan file aslinya terlebih dahulu sebagai cadangan.

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

### Contoh mengubah data
Misalnya siswa nomor 40 ingin memperbarui durasi tidurnya menjadi 7 jam:

1. Pilih `1` (Masuk Sebagai Siswa), lalu `2` (Ubah Data Kebiasaan).
2. Masukkan nomor data `40`.
3. Pilih aspek `4` (Durasi tidur).
4. Masukkan nilai baru `7`.
5. Jawab `y` untuk menyimpan. Program menampilkan `[BERHASIL] Data berhasil diubah dan disimpan ke file CSV.`
6. Pilih `1` (Lihat Hasil Evaluasi) lalu nomor `40`. Durasi tidur sudah tampil 7 jam, dan kolom `Sleep_Hours` di file CSV juga sudah berubah.

## Batasan
- Program hanya membaca maksimal 300 data valid pertama dari file CSV.
- Program belum memiliki sistem login, sehingga siswa dapat mengubah data siapa pun dengan memasukkan nomor datanya.
- Setiap perubahan langsung mengubah file CSV dan tidak dapat dibatalkan dari dalam program setelah disimpan.
- Satu kali perubahan hanya untuk satu aspek pada satu siswa.

## Struktur File
- `program analisis.py`: kode program utama
- `StudentPerformanceFactors.csv`: dataset siswa
- `README.md`: dokumentasi proyek

## Anggota Kelompok
1. Cherry Sandra: fitur utama
2. Liyana Maziya Fadhlani: fitur analisis
3. Belva Fitriyah Arzeti Putri: fitur menu
4. Asy Syifa Ramadhani Putri Indrianto: fitur dataset