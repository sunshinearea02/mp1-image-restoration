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

Pada bagian ini ditampilkan perbandingan antara citra awal yang rusak dengan hasil restorasi menggunakan dua metode histogram equalization.
| Citra Noisy (Input) | Restored (HEQ BGR) | Restored (HEQ YCbCr) | Citra Original |
|--------------------|-------------------|----------------------|----------------|
| ![](input/lena_noise.png) | ![](output/hasil_restorasi_BGR.png) | ![](output-YCbCr/hasil_restorasi.png) | ![](input/lena_original.png) |


