import cv2
import os
from glob import glob

for image in glob('./*.png'):
  img = cv2.imread(image)
  img = img[:176, :176]
  name, ext = os.path.splitext(image)
  cv2.imwrite(''.join([name, '-trim', ext]), img)


  # cv2.imshow('finger', img)
  # cv2.waitKey()
  # cv2.destroyAllWindows()