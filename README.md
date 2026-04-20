# Mini Project 1 — Image Restoration

**Mata Kuliah:** Pengolahan Citra dan Video  
**Nama:** Athaya Khairani Adi  
**NRP:** 5024241007  

---

## Penjelasan Pipeline Restorasi

Untuk menghasilkan citra yang lebih bersih dan tetap terlihat natural, digunakan pipeline restorasi bertahap yang terdiri dari proses denoising, smoothing, enhancement, dan sharpening.

### Tabel Pipeline

| Urutan | Teknik | Penjelasan Teknis | Tujuan & Alasan |
|--------|--------|------------------|----------------|
| 1 | Split Channel (BGR) | Citra dipisahkan menjadi tiga channel (Blue, Green, Red) untuk diproses secara independen | Distribusi noise berbeda tiap channel, sehingga hasil filtering lebih optimal |
| 2 | Median Filter (5x5) | Filter non-linear berbasis median dari window lokal | Menghilangkan noise impuls (salt-and-pepper) tanpa merusak edge |
| 3 | Gaussian Filter | Filter linear berbasis konvolusi dengan kernel Gaussian | Menghaluskan noise residual dan menghasilkan smoothing natural |
| 4 | Konversi ke YCrCb | Transformasi ruang warna untuk memisahkan luminance dan chrominance | Memungkinkan peningkatan kontras tanpa merusak warna |
| 5 | Histogram Equalization | Redistribusi intensitas menggunakan CDF | Meningkatkan kontras global citra |
| 6 | Unsharp Masking | Menambahkan kembali detail dari selisih citra asli dan blur | Menajamkan edge dan detail |
| 7 | Merge & Convert | Menggabungkan channel dan kembali ke BGR | Menghasilkan citra akhir dengan warna natural |

### Alur Pipeline
Denoising → Smoothing → Contrast Enhancement → Sharpening


---

## Perbandingan Visual

Berikut hasil perbandingan sebelum dan sesudah restorasi:

![Perbandingan](asset/hasil%20tugas1.png)

### Observasi

- **Original**: Noise tinggi, detail terganggu  
- **Median**: Noise impuls berkurang  
- **Gaussian**: Noise lebih halus, sedikit blur  
- **Histogram Equalization**: Kontras meningkat, noise ikut naik  
- **Final Result**: Lebih tajam, namun noise masih terlihat  

---

## Analisis

### 1. Analisis Tiap Tahap

- **Median Filter**  
  Efektif mengurangi noise impuls, tetapi tidak sepenuhnya menghilangkan noise granular.

- **Gaussian Filter**  
  Memberikan smoothing tambahan, namun menyebabkan sedikit kehilangan detail halus.

- **Histogram Equalization**  
  Berhasil meningkatkan kontras secara signifikan, tetapi juga memperkuat noise karena bersifat global.

- **Unsharp Masking**  
  Meningkatkan ketajaman edge, tetapi ikut memperkuat noise yang sudah ada.

---

### 2. Evaluasi Pipeline

- Pipeline berhasil meningkatkan visibilitas detail
- Kontras citra meningkat secara signifikan
- Namun noise masih cukup dominan pada hasil akhir



## Cara Menjalankan Program

### 1. Install 
pip install opencv-python numpy matplotlib

