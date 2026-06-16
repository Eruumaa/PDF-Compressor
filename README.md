# 🗜️ Exact 1MB PDF Compressor

Sebuah *script* Python ajaib yang tidak hanya mengecilkan ukuran file PDF, tetapi memaksanya menjadi **tepat 1 MB (1.048.576 Bytes)** secara presisi tidak kurang dan tidak lebih satu *byte* pun! 🎯

Sangat cocok untuk memenuhi persyaratan *upload* dokumen sistem (seperti pendaftaran beasiswa, CPNS, atau portal akademik) yang mewajibkan file dengan batas ukuran atau ukuran spesifik tertentu.

## ✨ Fitur Utama
- **Algoritma Binary Search:** Secara cerdas dan otomatis mencari tingkat kualitas gambar (JPEG *quality*) paling optimal untuk mendekati target 1 MB tanpa membuat gambar terlalu buram.
- **Rasterize & Compress:** Mengonversi setiap halaman PDF menjadi gambar yang dikompresi, lalu membungkusnya kembali menjadi PDF. Menghapus semua metadata dan kode "sampah" tersembunyi.
- **Smart Byte Padding:** Jika hasil kompresi optimal masih memiliki sisa ruang (misal: 950 KB), *script* akan menyuntikkan *dummy bytes* (`\0`) di akhir struktur file agar ukurannya menyentuh angka absolut 1.048.576 Bytes. Aman dan file tetap bisa dibuka dengan normal!

## 🛠️ Persyaratan Sistem (*Prerequisites*)
Pastikan kamu sudah menginstal **Python 3**. 
Script ini sangat bergantung pada *library* `PyMuPDF` untuk manipulasi struktur PDF.

Buka terminal kesayanganmu dan jalankan:
```bash
pip install PyMuPDF

```

## 🚀 Cara Penggunaan

1. Masukkan *script* `main.py` dan file PDF yang ingin kamu kompres ke dalam folder yang sama.
2. Buka file `main.py` dengan *code editor*.
3. Ubah nama file pada variabel `file_input` sesuai dengan nama file PDF aslimu:
```python
file_input = 'Sertifikat_Asli.pdf' 

```


4. Jalankan *script* melalui terminal:
```bash
python main.py

```


5. Tunggu proses kompresi (pencarian kualitas terbaik) selesai. File baru dengan nama `Sertifikat_PAS_1MB.pdf` akan otomatis dibuat!

## 🧠 Cara Kerja (*Under the Hood*)

Script ini berjalan dalam 3 fase utama:

1. **Fase Mencari Kualitas:** Menggunakan *Binary Search* (`low_q = 5`, `high_q = 95`) untuk me-*render* ulang halaman PDF dan mencari konfigurasi *JPEG quality* tertinggi yang menghasilkan ukuran file mentok di bawah 1 MB.
2. **Fase Pembuatan:** Membuat ulang (Generate) dokumen PDF baru dengan kualitas terbaik yang didapatkan dari Fase 1.
3. **Fase Injeksi:** Menghitung selisih *byte* antara dokumen yang dihasilkan dengan target 1 MB. Selisih ini ditutupi dengan menambahkan *null bytes* (`b'\0'`) pada ekor file (*append mode*).

## ⚠️ Troubleshooting

Jika di akhir log terminal kamu mendapatkan pesan:

> `[WARNING] Resolusi dokumen terlalu besar.`

Artinya, bahkan dengan kualitas terendah sekalipun, ukuran gambarmu masih di atas 1 MB.
**Solusi:** Buka `main.py`, cari baris ini:

```python
mat = fitz.Matrix(0.8, 0.8)

```

Ubah angkanya menjadi lebih kecil, misalnya `fitz.Matrix(0.6, 0.6)` atau `(0.5, 0.5)` untuk menurunkan resolusi dasar halamannya, lalu jalankan ulang *script*-nya.

---
Dibuat dengan ❤️ oleh **Akil**
---
