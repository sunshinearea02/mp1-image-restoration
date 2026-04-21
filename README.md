# Mini Project 1 — Image Restoration

**Mata Kuliah:** Pengolahan Citra dan Video  
**Nama:** Athaya Khairani Adi  
**NRP:** 5024241007  

---

## Penjelasan Pipeline Restorasi

Untuk menghasilkan citra yang lebih bersih dan tetap terlihat natural, digunakan pipeline restorasi bertahap yang terdiri dari proses denoising, smoothing, enhancement, dan sharpening.

### Penjelasan Pipeline Restorasi

| Urutan | Teknik | Penjelasan Teknis (Sederhana) | Tujuan & Alasan |
|--------|--------|--------------------------------|----------------|
| 1 | Split Channel (BGR) | Gambar dipisah menjadi 3 channel warna (biru, hijau, merah) untuk diproses terpisah | Distribusi noise berbeda tiap channel, sehingga hasil filtering lebih optimal |
| 2 | Median Filter (5x5) | Setiap pixel diganti dengan nilai tengah dari pixel di sekitarnya | Menghilangkan noise bintik-bintik tanpa merusak tepi objek |
| 3 | Gaussian Filter | Gambar dihaluskan dengan memberi bobot lebih besar ke pixel tengah | Mengurangi noise yang tersisa dan membuat hasil lebih halus |
| 4 | Konversi ke YCrCb | Gambar diubah ke format yang memisahkan kecerahan dan warna | Supaya peningkatan kontras tidak merusak warna |
| 5 | Histogram Equalization | Kecerahan gambar diatur ulang agar lebih merata | Meningkatkan kontras dan membuat detail lebih terlihat |
| 6 | Unsharp Masking | Detail yang hilang karena blur ditambahkan kembali | Menajamkan tepi dan memperjelas objek |
| 7 | Merge & Convert | Semua channel digabung kembali menjadi gambar berwarna | Menghasilkan citra akhir yang sudah diperbaiki |



---

## Perbandingan Visual

Berikut hasil perbandingan sebelum dan sesudah restorasi:

![Perbandingan](asset/hasil%20tugas1.png)

### Observasi

- **Original**: Noise tinggi, detail terganggu  
- **Median**: Noise berupa titik-titik acak berkurang  
- **Gaussian**: Noise lebih halus, sedikit blur  
- **Histogram Equalization**: Kontras meningkat, noise ikut naik  
- **Final Result**: Lebih tajam, namun noise masih terlihat  

---

## Analisis

### 1. Analisis Tiap Tahap

- **Median Filter**  
  Mengurangi noise berupa bintik-bintik acak, tetapi belum sepenuhnya menghilangkan noise halus yang menyebar di seluruh gambar.

- **Gaussian Filter**  
  Memberikan smoothing tambahan, namun menyebabkan sedikit kehilangan detail halus.

- **Histogram Equalization**  
  Berhasil meningkatkan kontras secara signifikan, tetapi juga memperkuat noise karena bersifat global.

- **Unsharp Masking**  
  Meningkatkan ketajaman edge, tetapi ikut memperkuat noise yang sudah ada.

---

### 2. Evaluasi Pipeline

- Objek pada citra menjadi lebih jelas terlihat
- Kontras citra meningkat secara signifikan
- Namun noise masih cukup dominan pada hasil akhir



## Cara Menjalankan Program

### 1. Install 
pip install opencv-python numpy matplotlib

