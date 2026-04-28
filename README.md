# Mini Project 1 — Image Restoration

**Mata Kuliah:** Pengolahan Citra dan Video  
**Nama:** Athaya Khairani Adi  
**NRP:** 5024241007  

---

##  Daftar Isi

1. [Detail Masalah](#1-detail-masalah)  

2. [Pipeline Restorasi](#2-pipeline-restorasi)  

3. [Perbandingan Visual](#3-perbandingan-visual)  

4. [Analisis Hasil](#4-analisis-hasil)   

5. [Cara Menjalankan Program](#5-cara-menjalankan-program)  
     
---
## 1. Detail Masalah
Citra yang digunakan sebagai input merupakan citra (Lena.png) yang telah mengalami empat macam degradasi/kerusakan.

| Jenis Degradasi | Penjelasan | Dampak pada Citra |
|----------------|----------|------------------|
| Low Contrast | Rentang intensitas piksel sempit (tidak menyebar dari 0–255), sehingga sebagian besar piksel berada di area tengah (mid-tone) | Gambar terlihat pucat, tidak tajam, dan detail sulit dibedakan |
| Gaussian Noise | Noise acak yang mengikuti distribusi normal dan tersebar di seluruh citra | Muncul butiran halus (grain), membuat citra tampak kasar dan mengganggu detail kecil |
| Salt-and-Pepper Noise | Piksel acak bernilai ekstrem, yaitu 0 (hitam) dan 255 (putih) | Terlihat sebagai titik-titik kontras tinggi yang mengganggu visual secara signifikan |
| Blur | Terjadi akibat proses konvolusi yang meratakan nilai piksel antar tetangga, blur mengurangi komponen frekuensi tinggi (high-frequency) yang berisi informasi detail dan tepi objek | Tepi objek menjadi kabur, detail halus hilang, dan citra terlihat tidak tajam |

---

###  Tujuan Restorasi

Berdasarkan permasalahan di atas, tujuan utama restorasi citra adalah:

- Mengurangi atau menghilangkan berbagai jenis noise (salt-and-pepper dan Gaussian)
- Memperbaiki kontras agar distribusi intensitas lebih merata
- Mengembalikan detail yang hilang akibat blur
- Menghasilkan citra yang lebih jelas, tajam, dan mendekati kondisi ideal

---

## 2. Pipeline Restorasi

| Tahap | Teknik | Apa yang Dilakukan | Alasan Dipilih | Dampak |
|------|--------|------------------|---------------|--------|
| 1 | Median Filter | Mengganti nilai piksel dengan median dari tetangganya dalam kernel | Efektif menghilangkan salt-and-pepper noise tanpa merusak edge | Noise impuls hilang, struktur objek tetap |
| 2 | Gaussian Filter | Melakukan smoothing menggunakan kernel Gaussian berbobot | Mengurangi Gaussian noise (noise halus) | Citra lebih halus, noise berkurang |
| 3A | HEQ (YCbCr) | Equalization hanya pada channel Y (luminance) | Memperbaiki kontras tanpa mengubah warna | Kontras naik, warna tetap natural |
| 3B | HEQ (BGR) | Equalization pada tiap channel warna secara terpisah | Meningkatkan kontras lebih agresif | Kontras tinggi, namun warna bisa berubah |
| 4 | Unsharp Masking | Meningkatkan komponen frekuensi tinggi (detail dan edge) | Mengembalikan detail yang hilang akibat blur | Edge dan detail menjadi lebih tajam |

---

###  Urutan Pipeline
Input → Median → Gaussian → Histogram Equalization → Sharpening → Output

## 3. Perbandingan Visual

## 3.1 Sebelum dan Sesudah Restorasi

Berikut perbandingan antara citra awal yang rusak dengan hasil restorasi menggunakan dua metode histogram equalization.
| Citra Noisy (Input) | Restored (HEQ BGR) | Restored (HEQ YCbCr) |
|--------------------|-------------------|----------------------|
| ![](input/lena.png) | ![](output_bgr/hasil_restorasi_BGR.png) | ![](output_ycbcr/hasil_restorasi_YCbCr.png) |

## 3.2 Perbandingan Tiap Tahap Pipeline dengan 2 Metode
## 3.2.1 Pipeline dengan HEQ Luminance-Only (YCbCr)
![](output_ycbcr/hasil_V1.png)

### Analisis Gambar

- Pada tahap **citra awal (original)**, terlihat bahwa gambar mengalami beberapa degradasi sekaligus. Noise cukup dominan, baik berupa bintik halus (Gaussian noise) maupun titik ekstrem hitam-putih (salt-and-pepper). Selain itu, citra juga tampak blur sehingga detail seperti tepi objek dan tekstur menjadi kurang jelas. Ditambah lagi, kontras yang rendah membuat perbedaan antara area terang dan gelap tidak terlalu terlihat.
- Setelah melalui **median filter**, perubahan paling terlihat adalah berkurangnya salt-and-pepper noise. Titik-titik hitam dan putih yang sebelumnya mengganggu mulai hilang. Kelebihan dari median filter terlihat di sini, yaitu mampu menghilangkan noise impuls tanpa merusak bentuk objek. Struktur wajah dan tepi utama tetap terjaga, meskipun masih terdapat noise halus.
- Pada tahap **Gaussian filter**, noise halus yang sebelumnya masih tersisa mulai berkurang. Citra terlihat lebih halus dan bersih dibandingkan sebelumnya. Namun, efek sampingnya adalah gambar menjadi sedikit lebih blur karena Gaussian filter meratakan nilai piksel di sekitarnya. Jadi pada tahap ini, noise berkurang cukup signifikan, tetapi ketajaman detail sedikit menurun.
- Ketika masuk ke tahap **histogram equalization pada channel Y (YCbCr)**, perubahan kontras menjadi sangat jelas. Distribusi intensitas yang sebelumnya sempit menjadi lebih lebar, sehingga perbedaan antara area terang dan gelap lebih terlihat. Karena hanya channel luminance yang diubah, warna pada citra tetap terlihat natural dan tidak mengalami distorsi. Ini membuat gambar terlihat lebih jelas tanpa mengubah karakter warna aslinya.
- Pada tahap akhir yaitu **sharpening (unsharp masking)**, detail yang sebelumnya hilang akibat blur mulai kembali. Tepi objek menjadi lebih tegas dan tekstur lebih terlihat. Proses ini bekerja dengan menambahkan kembali komponen detail ke citra. Hasil akhirnya adalah citra yang lebih tajam, dengan kontras yang sudah baik dan warna yang tetap natural. Secara keseluruhan, pipeline YCbCr menghasilkan restorasi yang seimbang antara pengurangan noise, peningkatan kontras, dan ketajaman.

### Analisis Histogram

- **Original**: Histogram sempit dan terpusat di tengah sehingga kontras rendah.  
- **Median Filter**: Spike ekstrem berkurang, noise impuls berhasil dihilangkan.  
- **Gaussian Filter**: Histogram lebih halus, noise frekuensi tinggi berkurang.  
- **Histogram Equalization (YCbCr)**: Histogram melebar merata ke 0–255, kontras global meningkat secara seimbang.  
- **Sharpening**: Peningkatan pada area gelap dan terang, kontras lokal meningkat tanpa distribusi menjadi ekstrem.  

Distribusi intensitas menjadi lebih merata dan stabil.

---

## 3.2.2 Pipeline dengan HEQ Per-Channel (BGR)
![](output_bgr/hasil_V2.png)

### Analisis Gambar

- Pada tahap **citra awal (original)**, kondisi yang terlihat sama seperti sebelumnya, yaitu citra memiliki noise tinggi, blur, dan kontras rendah. Detail objek sulit dikenali karena kombinasi dari noise dan rendahnya kontras.
- Setelah **median filter**, salt-and-pepper noise berkurang secara signifikan. Titik-titik ekstrem mulai hilang dan citra terlihat lebih bersih. Seperti pada pipeline sebelumnya, median filter tetap menjaga bentuk objek sehingga tidak terjadi distorsi pada struktur utama gambar.
- Pada tahap **Gaussian filter**, noise halus semakin berkurang dan citra menjadi lebih smooth. Namun, seperti sebelumnya, efek blur sedikit meningkat karena proses smoothing. Pada titik ini, citra sudah cukup bersih dari noise, tetapi masih kurang tajam.
- Perubahan besar mulai terlihat pada tahap **histogram equalization per-channel (BGR)**. Karena equalization dilakukan pada masing-masing channel warna secara terpisah, kontras meningkat secara lebih agresif dibandingkan metode YCbCr. Detail menjadi lebih menonjol, namun efek sampingnya adalah perubahan warna. Hubungan antar channel tidak lagi seimbang, sehingga warna bisa terlihat tidak natural atau terlalu mencolok (over-saturated).
- Pada tahap **sharpening (unsharp masking)**, ketajaman citra semakin meningkat. Tepi objek menjadi sangat jelas dan detail terlihat lebih jelas. Namun, karena sebelumnya kontras sudah tinggi akibat HEQ BGR, proses sharpening dapat membuat citra menjadi terlalu tajam. Selain itu, noise yang masih tersisa juga bisa ikut diperkuat. Akibatnya, hasil akhir memang terlihat sangat kontras dan tajam, tetapi kurang natural dibandingkan metode YCbCr.

### Analisis Histogram

- **Original**: Histogram sempit sehingga intensitas terkonsentrasi di mid-range.  
- **Median Filter**: Spike ekstrem berkurang, noise salt-pepper hilang.  
- **Gaussian Filter**: Histogram lebih smooth, noise halus berkurang.  
- **Histogram Equalization (BGR)**: Histogram tiap channel melebar sendiri, distribusi tidak seimbang antar channel.  
- **Sharpening**: Spike kuat di 0 dan 255,  kontras meningkat secara agresif.  

Distribusi intensitas menjadi lebih ekstrem dibanding YCbCr.

---

##  Kesimpulan Perbandingan
Dari kedua metode HEQ tersebut, dapat disimpulkan bahwa:
- HEQ **Luminance-Only (YCbCr)** menghasilkan citra yang lebih natural dan seimbang, karena hanya memperbaiki luminance tanpa mengganggu warna. Distribusi histogram lebih stabil, hasil natural  
- HEQ **Per-Channel (BGR)** menghasilkan citra yang lebih kontras dan tajam, tetapi berisiko menimbulkan distorsi warna dan peningkatan yang berlebihan pada kontras dan detail. Distribusi lebih agresif, kontras tinggi tetapi kurang natural  

---
## 4. Analisis Hasil
### 4.1 Yang berhasil : 
- Pipeline restorasi yang digunakan berhasil meningkatkan kualitas citra secara signifikan.
- Proses denoising menggunakan median dan Gaussian filter mampu mengurangi noise salt-and-pepper maupun Gaussian tanpa merusak struktur utama objek, sehingga citra menjadi lebih bersih.
- Selanjutnya, histogram equalization berhasil meningkatkan kontras dengan memperlebar distribusi intensitas, di mana metode YCbCr menghasilkan kontras yang lebih seimbang dan natural, sedangkan metode BGR memberikan kontras yang lebih kuat.
- Tahap sharpening dengan unsharp masking juga efektif dalam mengembalikan detail dan mempertegas tepi objek, sehingga citra terlihat lebih tajam. 
### 4.2 Yang bisa di tingkatkan : 
- Penggunaan histogram equalization global terkadang menghasilkan kontras yang terlalu kuat, terutama pada metode BGR, sehingga dapat menyebabkan perubahan warna yang kurang natural. Untuk mengatasi hal ini, dapat digunakan metode CLAHE (Contrast Limited Adaptive Histogram Equalization) yang mampu meningkatkan kontras secara lebih adaptif pada setiap area citra.
- Selain itu, Gaussian filter yang digunakan untuk mengurangi noise juga menyebabkan sedikit blur, sehingga ketajaman citra berkurang. Agar hasil lebih jernih, dapat dilakukan penyesuaian ukuran kernel Gaussian, penggunaan teknik denoising yang lebih selektif, serta pengaturan parameter sharpening agar tidak terlalu agresif.

---
## 5. Cara Menjalankan Program
1. Install Dependency.
Pastikan Python sudah terpasang, lalu install library yang dibutuhkan:
```bash
pip install numpy opencv-python matplotlib
```
2. Siapkan File Input. 
Letakkan file citra lena.png ke dalam folder input
3. Jalankan Program,
program terdiri dari dua file berbeda:
- Metode HEQ YCbCr
```bash
restorationV1.py
```
Hasil akan ditampilkan dalam bentuk visualisasi (matplotlib). 
Disimpan ke:
```bash
output_ycbcr/hasil_restorasi_YCbCr.png
```
- Metode HEQ BGR
```bash
restorationV2.py
```

Hasil akan ditampilkan dalam bentuk visualisasi (matplotlib). 
Disimpan ke:
```bash
output_bgr/hasil_restorasi_BGR.png
```
4. Struktur Direktori 
```bash
mp1-image-restoration/
│
├── input/
│   └── lena.png
│
├── output_ycbcr/
│   └── hasil_restorasi_YCbCr.png
│
├── output_bgr/
│   └── hasil_restorasi_BGR.png
│
├── README.md
├── restorationV1.py
└── restorationV2.py
```
5. Output yang dihasilkan yaitu
- Citra hasil restorasi
- Visualisasi tahapan:
  - Original
  - Median Filter
  - Gaussian Filter
  - Histogram Equalization
  - Final Result
- Histogram tiap tahap
