import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('input/lena.png')

if img is None:
    raise ValueError("Gambar tidak ditemukan!")

img = img.astype(np.float64)



def bgr_to_ycrcb(img):
    B = img[:,:,0]
    G = img[:,:,1]
    R = img[:,:,2]

    Y  = 0.299 * R + 0.587 * G + 0.114 * B
    Cr = (R - Y) * 0.713 + 128
    Cb = (B - Y) * 0.564 + 128

    return np.stack([Y, Cr, Cb], axis=2)


def ycrcb_to_bgr(img):
    Y  = img[:,:,0]
    Cr = img[:,:,1]
    Cb = img[:,:,2]

    R = Y + 1.403 * (Cr - 128)
    G = Y - 0.344 * (Cb - 128) - 0.714 * (Cr - 128)
    B = Y + 1.773 * (Cb - 128)

    return np.stack([
        np.clip(B, 0, 255),
        np.clip(G, 0, 255),
        np.clip(R, 0, 255)
    ], axis=2)



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




# manual split 
b = img[:,:,0]
g = img[:,:,1]
r = img[:,:,2]

# 1. Median
b_med = median_filter(b, 5)
g_med = median_filter(g, 5)
r_med = median_filter(r, 5)

denoise1 = np.stack([b_med, g_med, r_med], axis=2)

# 2. Gaussian
kernel = gaussian_kernel(5, 1.2)
b_g = convolve(b_med, kernel)
g_g = convolve(g_med, kernel)
r_g = convolve(r_med, kernel)

denoise2 = np.stack([b_g, g_g, r_g], axis=2)

# 3. YCrCb manual
ycrcb = bgr_to_ycrcb(denoise2)
Y  = ycrcb[:,:,0]
Cr = ycrcb[:,:,1]
Cb = ycrcb[:,:,2]

# 4. Histogram Equalization
Y_eq = histogram_equalization(Y)

contrast = np.stack([Y_eq, Cr, Cb], axis=2)
contrast = ycrcb_to_bgr(contrast).astype(np.uint8)

# 5. Sharpen
Y_sharp = unsharp_mask(Y_eq, sigma=1.0, k=1.2)

result = np.stack([Y_sharp, Cr, Cb], axis=2)
result = ycrcb_to_bgr(result).astype(np.uint8)


y_orig = bgr_to_ycrcb(img)[:,:,0]
y_med = bgr_to_ycrcb(denoise1)[:,:,0]
y_gauss = bgr_to_ycrcb(denoise2)[:,:,0]
y_eq = Y_eq
y_final = bgr_to_ycrcb(result.astype(np.float64))[:,:,0]

#Visualisasi
plt.figure(figsize=(18,10))

plt.subplot(3,5,1)
plt.title("Original")
plt.imshow(img[:,:,::-1].astype(np.uint8))
plt.axis('off')

plt.subplot(3,5,2)
plt.title("Median")
plt.imshow(denoise1[:,:,::-1].astype(np.uint8))
plt.axis('off')

plt.subplot(3,5,3)
plt.title("Gaussian")
plt.imshow(denoise2[:,:,::-1].astype(np.uint8))
plt.axis('off')

plt.subplot(3,5,4)
plt.title("Hist Eq")
plt.imshow(contrast[:,:,::-1])
plt.axis('off')

plt.subplot(3,5,5)
plt.title("Final")
plt.imshow(result[:,:,::-1])
plt.axis('off')

# HISTOGRAM
plt.subplot(3,5,6)
plot_histogram(y_orig, "Hist Original")

plt.subplot(3,5,7)
plot_histogram(y_med, "Hist Median")

plt.subplot(3,5,8)
plot_histogram(y_gauss, "Hist Gaussian")

plt.subplot(3,5,9)
plot_histogram(y_eq, "Hist Equalized")

plt.subplot(3,5,10)
plot_histogram(y_final, "Hist Final")

plt.tight_layout()
plt.show()


cv2.imwrite('output_ycbcr/hasil_restorasi_YCbCr.png', result)
