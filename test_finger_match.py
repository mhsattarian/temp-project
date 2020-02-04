import os, sys, glob
from finger_match import match as f_match
import cv2

images = sorted(glob.glob('./samples/finger-*-trim.png'))

for image in images:
  img = cv2.imread(image, 0)
  images_to_compare = sorted([i for i in images if i is not image])
  image_number = image.split('-')[1]
  for image_to_compare in images_to_compare:
    img_to_compare = cv2.imread(image_to_compare, 0)
    r, s = f_match(img, img_to_compare)
    image_to_compare_number = image_to_compare.split('-')[1]
    print(f'finger {image_number} - {image_to_compare_number} : {r} - score({s})')


