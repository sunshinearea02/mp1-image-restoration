import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('input/lena.png')

if img is None:
    raise ValueError("Gambar tidak ditemukan!")

img = img.astype(np.float64)


def median_filter(img, k=3):
    pad = k // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+k, j:j+k].flatten()
            sorted_vals = np.sort(window)
            output[i, j] = sorted_vals[len(sorted_vals)//2]

    return output

def gaussian_kernel(size, sigma):
    half = size // 2
    kernel = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            x, y = j - half, i - half
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))

    return kernel / kernel.sum()

def convolve(img, kernel):
    k = kernel.shape[0]
    pad = k // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+k, j:j+k]
            output[i, j] = np.sum(region * kernel)

    return output


def histogram_equalization(img):
    L = 256
    hist = np.zeros(L)

    for pixel in img.flatten():
        hist[int(pixel)] += 1

    pdf = hist / img.size
    cdf = np.cumsum(pdf)

    s = (L - 1) * cdf

    output = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            output[i, j] = s[int(img[i, j])]

    return output


def unsharp_mask(img, sigma=1.0, k=1.2):
    kernel = gaussian_kernel(5, sigma)
    blurred = convolve(img, kernel)
    mask = img - blurred
    sharp = img + k * mask
    return np.clip(sharp, 0, 255)


# --- SPLIT ---
b, g, r = cv2.split(img)


b_med = median_filter(b, 5)
g_med = median_filter(g, 5)
r_med = median_filter(r, 5)

denoise1 = cv2.merge([b_med, g_med, r_med])  


kernel = gaussian_kernel(5, 1.2)

b_g = convolve(b_med, kernel)
g_g = convolve(g_med, kernel)
r_g = convolve(r_med, kernel)

denoise2 = cv2.merge([b_g, g_g, r_g])  

# --- HISTOGRAM (Y only) ---
ycrcb = cv2.cvtColor(denoise2.astype(np.uint8), cv2.COLOR_BGR2YCrCb)
Y, Cr, Cb = cv2.split(ycrcb)

Y_eq = histogram_equalization(Y.astype(np.float64))

contrast = cv2.merge([Y_eq.astype(np.uint8), Cr, Cb])
contrast = cv2.cvtColor(contrast, cv2.COLOR_YCrCb2BGR)  

# --- SHARPEN ---
Y_sharp = unsharp_mask(Y_eq, sigma=1.0, k=1.2)

result = cv2.merge([
    Y_sharp.astype(np.uint8),
    Cr,
    Cb
])

result = cv2.cvtColor(result, cv2.COLOR_YCrCb2BGR)


plt.figure(figsize=(15,8))

plt.subplot(2,3,1)
plt.title("Original")
plt.imshow(cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(2,3,2)
plt.title("Median")
plt.imshow(cv2.cvtColor(denoise1.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(2,3,3)
plt.title("Gaussian")
plt.imshow(cv2.cvtColor(denoise2.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(2,3,4)
plt.title("Histogram Equalization")
plt.imshow(cv2.cvtColor(contrast.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(2,3,5)
plt.title("Final Result")
plt.imshow(cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.tight_layout()
plt.show()


cv2.imwrite('output/hasil_restorasi.png', result.astype(np.uint8))
