# Mini Project 1 — Image Restoration

**Mata Kuliah:** Pengolahan Citra dan Video  
**Nama:** Athaya Khairani Adi  
**NRP:** 5024241007  

---
##  1. Detail Masalah

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

##  2. Pipeline Restorasi

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
| ![](input/lena.png) | ![](output/hasil_restorasi_BGR.png) | ![](output/hasil_restorasi_YCbCr.png) |

## 3.2 Perbandingan Tahap Pipeline

## 3.2.1 Pipeline dengan HEQ YCbCr
![](output/hasil_V1.png)

# Analisis

- Pada tahap **citra awal (original)**, gambar mengandung noise (Gaussian dan salt-and-pepper), blur, serta kontras rendah sehingga detail kurang terlihat.  
  Histogram sempit dan terpusat di intensitas tengah → menandakan distribusi intensitas belum merata (low contrast).

- Setelah **median filter**, salt-and-pepper noise berkurang signifikan tanpa merusak struktur objek. Noise ekstrem (piksel 0 dan 255) mulai hilang.  
  Histogram menjadi lebih halus dan spike di nilai ekstrem berkurang → distribusi lebih stabil.

- Pada tahap **Gaussian filter**, noise halus semakin berkurang dan citra terlihat lebih bersih, meskipun sedikit lebih blur.  
  Histogram semakin smooth, menunjukkan variasi kecil (noise) berkurang → kualitas distribusi meningkat.

- Pada tahap **histogram equalization (YCbCr - channel Y)**, kontras meningkat signifikan karena distribusi intensitas melebar ke seluruh rentang 0–255. Warna tetap natural karena hanya luminance yang diproses.  
  Histogram menjadi lebih merata → peningkatan kontras global yang seimbang.

- Pada tahap **sharpening**, detail dan tepi objek kembali tajam tanpa merusak warna.  
  Histogram menunjukkan peningkatan pada area gelap dan terang secara seimbang → peningkatan kontras lokal tanpa membuat distribusi ekstrem.

Secara keseluruhan, pipeline YCbCr meningkatkan kualitas citra secara bertahap: dari distribusi sempit → stabil → merata → tajam, dengan hasil yang tetap natural.

---

## 3.2.2 Pipeline dengan HEQ BGR
![](output/hasil_V2.png)

# Analisis

- Pada tahap **citra awal (original)**, citra memiliki noise tinggi, blur, dan kontras rendah sehingga detail sulit dikenali.  
  Histogram sempit dan terpusat di tengah → menunjukkan kontras rendah.

- Setelah **median filter**, salt-and-pepper noise berkurang dan citra lebih bersih tanpa merusak bentuk objek.  
  Histogram menjadi lebih halus, spike ekstrem berkurang → distribusi mulai stabil.

- Pada tahap **Gaussian filter**, noise halus berkurang dan citra menjadi lebih smooth, meskipun sedikit blur.  
  Histogram semakin smooth → noise berkurang, tetapi kontras belum meningkat.

- Pada tahap **histogram equalization (BGR)**, kontras meningkat lebih agresif karena tiap channel diproses terpisah. Detail menjadi lebih menonjol, tetapi warna mulai berubah.  
  Histogram tiap channel melebar secara tidak seimbang → menyebabkan distorsi warna.

- Pada tahap **sharpening**, citra menjadi sangat tajam dan kontras tinggi. Namun, peningkatan ini cenderung berlebihan dan dapat memperkuat noise yang tersisa.  
  Histogram menunjukkan spike kuat di 0 dan 255 → distribusi menjadi lebih ekstrem.

Secara keseluruhan, pipeline BGR meningkatkan kontras dan ketajaman secara lebih kuat, tetapi distribusi histogram menjadi kurang stabil sehingga warna terlihat kurang natural.

## Kesimpulan Analisis Pipeline

Dari kedua pipeline tersebut, dapat disimpulkan bahwa:

- Pipeline **YCbCr** menghasilkan citra yang lebih natural dan seimbang, karena hanya memperbaiki luminance tanpa mengganggu warna.
- Pipeline **BGR** menghasilkan citra yang lebih kontras dan tajam, tetapi berisiko menimbulkan distorsi warna dan peningkatan yang berlebihan pada kontras dan detail.
- Pemilihan metode tergantung kebutuhan:
  - Untuk hasil realistis → YCbCr lebih baik  
  - Untuk visual yang lebih “menonjol” → BGR bisa digunakan

