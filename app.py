import os
import sys
from multiprocessing import Process
import cv2

# Fingerprint Recognition
from fingerprint_simpletest_rpi import num_id, enroll_finger, get_fingerprint, save_fingerprint_image
import serial
import adafruit_fingerprint
from finger_match import match as f_match

# Face Recognition
from face_match import *

# Initializations
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

database_directory = './database'
if not os.path.exists(database_directory):
  os.makedirs(database_directory)

temp_dir = './temp'
if not os.path.exists(temp_dir):
  os.makedirs(temp_dir)


# Our list of known face encodings and a matching list of metadata about each face.
# known_face_encodings = []
# known_face_metadata = []
load_known_faces()
  


##################################################
def enroll_user():
  user_id = int(input("Enter ID # from 0-{}: ".format(num_id())))

  # create user directory
  user_dir = os.path.join(database_directory, str(user_id))
  if not os.path.exists(user_dir):
    os.makedirs(user_dir)

  enroll_finger(user_id)

  # get finger image
  while finger.get_image():
    pass

  # save finger image in parallel
  user_finger_img_addr = os.path.join(user_dir, 'finger.png')
  p_save_img = Process(target=save_fingerprint_image, args=(user_finger_img_addr,))
  p_save_img.start()

  # get user image
  handle_new_faces(str(user_id))


  p_save_img.join()

  # fimg = cv2.imread(user_finger_img_addr)
  # cv2.imshow('finger', fimg)
  # cv2.waitKey()
  # cv2.destroyAllWindows()

def handle_new_faces(user_id):
  # Grab a single frame of video
  video_capture = cv2.VideoCapture(get_jetson_gstreamer_source(), cv2.CAP_GSTREAMER)
  
  face_found = False
  count = 0
  while not face_found:
    ret, frame = video_capture.read()

    cv2.imshow('capture', frame)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the face locations and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    count += len(face_locations)
    print(count)
    if count > 3: face_found = True

  face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
  
  for face_location, face_encoding in zip(face_locations, face_encodings):
    # Grab the image of the the face from the current frame of video
    top, right, bottom, left = face_location
    face_image = small_frame[top:bottom, left:right]
    face_image = cv2.resize(face_image, (150, 150))

    user_dir = os.path.join(database_directory, user_id, 'face.png')
    cv2.imwrite(user_dir, face_image)

    # Add the new face to our known face data
    register_new_face(face_encoding, face_image, user_id)
  
  save_known_faces()

  video_capture.release()
  cv2.destroyAllWindows()

def find_user():
  # # get finger image
  # while finger.get_image():
  #   pass

  r, _id, _confidence = get_fingerprint()

  while not r:
    print('finger dont match! try again. \n')
    r, _id, _confidence = get_fingerprint()


  # # save finger image in parallel
  # temp_finger_img_addr = os.path.join(temp_dir, 'finger.png')
  # p_save_img = Process(target=save_fingerprint_image, args=(temp_finger_img_addr,))
  # p_save_img.start()


  found_user_id = find_face()
  # print('found_user_id: ', found_user_id)

  # f_result = match_fingers(found_user_id)
  # if f_result: print('fingers match')
  # else: print('fingers don\'t match')


  print(f'finger {r} | \t user_id: {_id} confidence: {_confidence}')
  print(f'face | \t user_id: {found_user_id}')
  

  
  # p_save_img.join()

def find_face():
  # Grab a single frame of video
  video_capture = cv2.VideoCapture(get_jetson_gstreamer_source(), cv2.CAP_GSTREAMER)
  
  face_found = False
  count = 0
  while not face_found:
    ret, frame = video_capture.read()

    cv2.imshow('capture', frame)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the face locations and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    count += len(face_locations)
    print(count)
    if count > 3: face_found = True
  
  face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

  found_user_id = None
  for face_location, face_encoding in zip(face_locations, face_encodings):
    # See if this face is in our list of known faces.
    metadata = lookup_known_face(face_encoding)

    # If we found the face, label the face with some useful information.
    if metadata is not None:
      found_user_id = metadata['user_id']
  

  return found_user_id


def match_fingers(found_user_id):
  img1_path = os.path.join(database_directory, found_user_id, 'finger.png')
  img2_path = os.path.join(temp_dir, 'finger.png')

  img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
  img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

  result = f_match(img1, img2)
  return result


  
##################################################
if __name__ == "__main__":
  while True:
    print("------%------")
    # print("Size of template library: ", finger.library_size)
    print("e) enroll user \t f) find user \t q) quit")
    print("\n")
    c = input("> ")

    if c == 'e':
      enroll_user()
    if c == 'f':
      find_user()
    if c == 'q':
      print("Exiting...")
      raise SystemExit
