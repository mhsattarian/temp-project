import os, sys, glob
from finger_match import match as f_match
import cv2

images = sorted(glob.glob('./samples/finger-*-trim.png'))

for image in images:
  img = cv2.imread(image, 0)
  finger_name = image.split("-")
  finger_number = finger_name[1]
  other_finger_number = (int(finger_number) + 5) % 10
  if other_finger_number == 0: other_finger_number = 10
  finger_name[1] = str(other_finger_number)
  other_finger_name = '-'.join(finger_name)
  
  # images_to_compare = sorted([i for i in images if i is not image])

  # for image_to_compare in images_to_compare:
  img_to_compare = cv2.imread(other_finger_name, 0)
  r, s = f_match(img, img_to_compare)
  print(f'match {image.split("-")[1]} and {other_finger_number} was {r}')

