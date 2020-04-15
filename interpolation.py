# -*- coding: utf-8 -*-
"""Linear_Interpolation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17_Sc8-HN-0PKX2McaCMO8G84Iy0CZoHx
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from skimage.metrics import structural_similarity, peak_signal_noise_ratio
import os

def interpolate_image(path, print_pics = False):
  orig_img = plt.imread(path) #('/content/0004x2.png')
  print('Original Dimensions : ', orig_img.shape)
  orig_dim = (orig_img.shape[1], orig_img.shape[0]) # (width, height)

  scale_percent = 20 # percent of original size
  width = int(orig_img.shape[1] * scale_percent / 100)
  height = int(orig_img.shape[0] * scale_percent / 100)
  dim = (width, height)
  downsampled_img = cv2.resize(orig_img, dim, interpolation = cv2.INTER_AREA)

  print('Downsampled Dimensions : ', downsampled_img.shape)

  # Upscale image
  resized_NN = cv2.resize(downsampled_img, orig_dim, interpolation = cv2.INTER_NEAREST)
  resized_BL = cv2.resize(downsampled_img, orig_dim, interpolation = cv2.INTER_LINEAR)
  resized_BC = cv2.resize(downsampled_img, orig_dim, interpolation = cv2.INTER_CUBIC)
  # print(np.max(resized_BC))
  # print(np.min(resized_BC))
  # resized_BC = np.clip(resized_BC, 0, 1)

  print('Resized Dimensions : ', resized_NN.shape)
  if print_pics:
    plt.figure(figsize=(16,10))

    plt.subplot(2,3,1)
    plt.imshow(orig_img)
    # plt.imsave('orig.jpg', orig_img)
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(2,3,2)
    plt.imshow(downsampled_img)
    plt.title('Downsampled Image')
    plt.axis('off')

    plt.subplot(2,3,4)
    plt.imshow(resized_NN)
    # plt.imsave('NN.jpg', resized_NN)
    plt.title('Upsampled Image - Nearest Neighbour')
    plt.axis('off')

    plt.subplot(2,3,5)
    plt.imshow(resized_BL)
    # plt.imsave('BL.jpg', resized_BL)
    plt.title('Upsampled Image - Bilinear')
    plt.axis('off')

    plt.subplot(2,3,6)
    plt.imshow(resized_BC)
    # plt.imsave('BC.jpg', resized_BC)
    plt.title('Upsampled Image - Bicubic')
    plt.axis('off')

    plt.tight_layout()
    plt.savefig('interpolated_' + path[-10:-4])
    plt.show()

  NN_ssim = structural_similarity(orig_img, resized_NN, multichannel=False)
  NN_psnr = peak_signal_noise_ratio(orig_img, resized_NN)

  BL_ssim = structural_similarity(orig_img, resized_BL, multichannel=False)
  BL_psnr = peak_signal_noise_ratio(orig_img, resized_BL)

  BC_ssim = structural_similarity(orig_img, resized_BC, multichannel=False)
  BC_psnr = peak_signal_noise_ratio(orig_img, resized_BC)

  # print('Nearest Neighbour Interpolation:')
  # print('\tSSIM: {:.2f}'.format(NN_ssim))
  # print('\tPSNR: {:.2f}'.format(NN_psnr))

  # print('Bilinear Interpolation:')
  # print('\tSSIM: {:.2f}'.format(BL_ssim))
  # print('\tPSNR: {:.2f}'.format(BL_psnr))

  # print('Bicubic Interpolation:')
  # print('\tSSIM: {:.2f}'.format(BC_ssim))
  # print('\tPSNR: {:.2f}'.format(BC_psnr))

  return NN_ssim, NN_psnr, BL_ssim, BL_psnr, BC_ssim, BC_psnr

NN_ssim, NN_psnr = list(), list()
BL_ssim, BL_psnr = list(), list()
BC_ssim, BC_psnr = list(), list()


directory = '/content/drive/My Drive/Cancer Images'
for filename in os.listdir(directory):
  if filename.endswith('.jpg'):
    path = os.path.join(directory, filename)
    a, b, c, d, e, f = interpolate_image(path, print_pics=True)
    NN_ssim.append(a)
    NN_psnr.append(b)
    BL_ssim.append(c)
    BL_psnr.append(d)
    BC_ssim.append(e)
    BC_psnr.append(f)
  else:
    continue

print('Nearest Neighbour Interpolation:')
print('\tSSIM: {:.2f}'.format(np.mean(NN_ssim)))
print('\tPSNR: {:.2f}'.format(np.mean(NN_psnr)))

print('Bilinear Interpolation:')
print('\tSSIM: {:.2f}'.format(np.mean(BL_ssim)))
print('\tPSNR: {:.2f}'.format(np.mean(BL_psnr)))

print('Bicubic Interpolation:')
print('\tSSIM: {:.2f}'.format(np.mean(BC_ssim)))
print('\tPSNR: {:.2f}'.format(np.mean(BC_psnr)))



# Compute errors scores
# from skimage.measure import compare_ssim, compare_psnr
from skimage.metrics import structural_similarity, peak_signal_noise_ratio

NN_ssim = structural_similarity(orig_img, resized_NN, multichannel=True)
NN_psnr = peak_signal_noise_ratio(orig_img, resized_NN)

BL_ssim = structural_similarity(orig_img, resized_BL, multichannel=True)
BL_psnr = peak_signal_noise_ratio(orig_img, resized_BL)

BC_ssim = structural_similarity(orig_img, resized_BC, multichannel=True)
BC_psnr = peak_signal_noise_ratio(orig_img, resized_BC)

print('Nearest Neighbour Interpolation:')
print('\tSSIM: {:.2f}'.format(NN_ssim))
print('\tPSNR: {:.2f}'.format(NN_psnr))

print('Bilinear Interpolation:')
print('\tSSIM: {:.2f}'.format(BL_ssim))
print('\tPSNR: {:.2f}'.format(BL_psnr))

print('Bicubic Interpolation:')
print('\tSSIM: {:.2f}'.format(BC_ssim))
print('\tPSNR: {:.2f}'.format(BC_psnr))

def crop_image(img, left_factor, right_factor, top_factor, bot_factor):
  h, w, _ = img.shape

  left = int(left_factor * w)
  right = int((1-right_factor) * w)
  top = int(top_factor * h)
  bottom = int((1-bot_factor) * h)

  return img[top:-bottom, left:-right]


left, right, top, bottom = 1/2, 2/3, 1/3, 2/3

plt.figure(figsize=(10,6))

plt.subplot(2,2,1)
plt.imshow(crop_image(img, left, right, top, bottom))
plt.title('Original Image')
plt.axis('off')

plt.subplot(2,2,2)
plt.imshow(crop_image(resized_NN, left, right, top, bottom))
plt.title('Upsampled Image - Nearest Neighbour')
plt.axis('off')

plt.subplot(2,2,3)
plt.imshow(crop_image(resized_BL, left, right, top, bottom))
plt.title('Upsampled Image - Bilinear')
plt.axis('off')

plt.subplot(2,2,4)
plt.imshow(crop_image(resized_BC, left, right, top, bottom))
plt.title('Upsampled Image - Bicubic')
plt.axis('off')

plt.show()
