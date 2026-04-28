import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('LATIHAN/lena.png')

if img is None:
    raise ValueError("Gambar tidak ditemukan!")

img = img.astype(np.float64)


def compute_histogram(img):
    hist = np.zeros(256)
    for pixel in img.flatten():
        hist[int(pixel)] += 1
    return hist

def plot_histogram(img, title):
    hist = compute_histogram(img)
    plt.plot(hist)
    plt.title(title)
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")


def median_filter(img, k=3):
    pad = k // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+k, j:j+k].flatten()
            output[i, j] = np.sort(window)[len(window)//2]

    return np.clip(output, 0, 255)


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

    return np.clip(output, 0, 255)


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

    return np.clip(output, 0, 255)


def unsharp_mask(img, sigma=1.0, k=1.2):
    kernel = gaussian_kernel(5, sigma)
    blurred = convolve(img, kernel)
    mask = img - blurred
    sharp = img + k * mask
    return np.clip(sharp, 0, 255)


b, g, r = cv2.split(img)

# 1. Median
b_med = median_filter(b, 5)
g_med = median_filter(g, 5)
r_med = median_filter(r, 5)
denoise1 = cv2.merge([b_med, g_med, r_med])

# 2. Gaussian
kernel = gaussian_kernel(5, 1.2)
b_g = convolve(b_med, kernel)
g_g = convolve(g_med, kernel)
r_g = convolve(r_med, kernel)
denoise2 = cv2.merge([b_g, g_g, r_g])

# 3. HISTOGRAM EQUALIZATION PER CHANNEL 
b_eq = histogram_equalization(b_g)
g_eq = histogram_equalization(g_g)
r_eq = histogram_equalization(r_g)

contrast = cv2.merge([
    b_eq.astype(np.uint8),
    g_eq.astype(np.uint8),
    r_eq.astype(np.uint8)
])

# 4. SHARPEN PER CHANNEL
b_sharp = unsharp_mask(b_eq)
g_sharp = unsharp_mask(g_eq)
r_sharp = unsharp_mask(r_eq)

result = cv2.merge([
    b_sharp.astype(np.uint8),
    g_sharp.astype(np.uint8),
    r_sharp.astype(np.uint8)
])



y_orig = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2YCrCb)[:,:,0]
y_med = cv2.cvtColor(denoise1.astype(np.uint8), cv2.COLOR_BGR2YCrCb)[:,:,0]
y_gauss = cv2.cvtColor(denoise2.astype(np.uint8), cv2.COLOR_BGR2YCrCb)[:,:,0]
y_eq = cv2.cvtColor(contrast, cv2.COLOR_BGR2YCrCb)[:,:,0]
y_final = cv2.cvtColor(result, cv2.COLOR_BGR2YCrCb)[:,:,0]



plt.figure(figsize=(18,10))

# IMAGE
plt.subplot(3,5,1)
plt.title("Original")
plt.imshow(cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(3,5,2)
plt.title("Median")
plt.imshow(cv2.cvtColor(denoise1.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(3,5,3)
plt.title("Gaussian")
plt.imshow(cv2.cvtColor(denoise2.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(3,5,4)
plt.title("HEQ BGR")
plt.imshow(cv2.cvtColor(contrast, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(3,5,5)
plt.title("Final")
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.axis('off')

# HISTOGRAM
plt.subplot(3,5,6)
plot_histogram(y_orig, "Hist Original")

plt.subplot(3,5,7)
plot_histogram(y_med, "Hist Median")

plt.subplot(3,5,8)
plot_histogram(y_gauss, "Hist Gaussian")

plt.subplot(3,5,9)
plot_histogram(y_eq, "Hist HEQ BGR")

plt.subplot(3,5,10)
plot_histogram(y_final, "Hist Final")

plt.tight_layout()
plt.show()


cv2.imwrite('TUGAS/hasil_restorasi_BGR.png', result)