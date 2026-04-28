# Mini Project 1 — Image Restoration

**Mata Kuliah:** Pengolahan Citra dan Video  
**Nama:** Athaya Khairani Adi  
**NRP:** 5024241007  

---
##  1. Detail Masalah

| Jenis Degradasi | Penjelasan | Dampak pada Citra |
|----------------|----------|------------------|
| Low Contrast | Rentang intensitas piksel sempit (tidak menyebar dari 0–255) | Gambar terlihat pucat, detail sulit dibedakan |
| Gaussian Noise | Noise acak dengan distribusi normal | Muncul butiran halus (grain), mengganggu detail kecil |
| Salt-and-Pepper Noise | Piksel acak bernilai 0 (hitam) dan 255 (putih) | Titik-titik ekstrem yang sangat mengganggu visual |
| Blur | Kehilangan ketajaman akibat proses smoothing atau akuisisi | Tepi objek kabur, detail hilang |

---

##  2. Pipeline Restorasi

| Tahap | Teknik | Apa yang Dilakukan | Alasan Dipilih | Dampak |
|------|--------|------------------|---------------|--------|
| 1 | Median Filter | Mengambil nilai median dari tetangga piksel | Efektif menghilangkan salt-and-pepper noise tanpa merusak edge | Noise impuls hilang, bentuk objek tetap |
| 2 | Gaussian Filter | Melakukan smoothing dengan kernel Gaussian | Mengurangi Gaussian noise (noise halus) | Citra lebih halus, noise berkurang |
| 3A | HEQ (YCbCr) | Equalization pada channel Y (luminance) saja | Memperbaiki kontras tanpa mengubah warna | Kontras naik, warna tetap natural |
| 3B | HEQ (BGR) | Equalization pada tiap channel warna (B, G, R) | Meningkatkan kontras secara langsung | Kontras tinggi, tapi warna bisa berubah |
| 4 | Unsharp Masking | Menambahkan detail (img - blur) ke citra | Mengembalikan ketajaman setelah blur | Detail dan edge menjadi lebih tajam |

---

###  Urutan Pipeline
Input → Median → Gaussian → Histogram Equalization → Sharpening → Output

