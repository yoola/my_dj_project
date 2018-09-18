import numpy as np
import cv2
from matplotlib import pyplot as plt
import pickle
import os
import glob
from GoogleGlass.Image_recognition.Code.pickle_funcs import pickle_keypoints, unpickle_keypoints


img_path = '../Test_Pics_B11/'

folders = ["1OG_Flur192/Object","1OG_Flur193/Object", "1OG_Flur194/Object" ,"2OG_Flur292/Object",
              "2OG_Flur295/Object", "2OG_Flur296/Object", "2OG_Flur297/Object", "3OG_Flur392/Object", 
              "3OG_Flur394/Object", "3OG_R307/Object", "3OG_R308/Object","3OG_R310/Object", 
              "EG_Flur092/Object","EG_Flur094/Object","EG_Flur095/Object"]

# folders = ["1OG_Flur192","1OG_Flur193", "1OG_Flur194" ,"2OG_Flur292",
#               "2OG_Flur295", "2OG_Flur296", "2OG_Flur297", "3OG_Flur392", 
#               "3OG_Flur394", "3OG_R307", "3OG_R308","3OG_R310", 
#               "EG_Flur092","EG_Flur094","EG_Flur095"]

def hist_tiles(img):

  tile1 = int(img.shape[0]/3)
  tile2 = int(img.shape[1]/3)

  tile1_ = tile1
  tile2_ = tile2

  start1 = 0
  start2 = 0

  all_hists = [] 
  
  for j in range(0,3):

    for i in range(0,3):

      img_new=img[start1:tile1, start2:tile2]

      hist = cv2.calcHist([img],[0],None,[256],[0,256])
      all_hists.append(hist)

      tile1 = tile1 + tile1_
      start1 = start1+ tile1_

    tile2 = tile2 + tile2_
    start2 = start2+ tile2_

    start1 = 0
    tile1 = tile1_  

  return all_hists


def save_SIFT(img_path, folders):

	# Initiate SIFT detector
	sift = cv2.xfeatures2d.SIFT_create()

	for j in folders:

		path = img_path+j

		for infile in glob.glob( os.path.join(path, '*.jpg') ):

			img1 = cv2.imread(infile,0) 

			print(infile)

			# find the keypoints and descriptors with SIFT
			kp1, des1 = sift.detectAndCompute(img1,None)

			#Store and Retrieve keypoint features
			temp = pickle_keypoints(kp1, des1)
			infile = infile.replace("/", "+")
			pickle.dump(temp, open("../KeyPoints/SIFT_entrance/keypoints_"+infile[3:-4]+".p", "wb"))


def save_SURF(img_path, folders, numb_features):

	# Create SURF object. You can specify params here or later.
	# Here I set Hessian Threshold to 400
	surf = cv2.xfeatures2d.SURF_create(numb_features)
	surf.setExtended(True)

	for j in folders:

		path = img_path+j

		for infile in glob.glob( os.path.join(path, '*.jpg') ):

			img1 = cv2.imread(infile,0) 

			print(infile)

			# find the keypoints and descriptors with SIFT
			kp1, des1 = surf.detectAndCompute(img1,None)

			#Store and Retrieve keypoint features
			temp = pickle_keypoints(kp1, des1)
			infile = infile.replace("/", "+")
			pickle.dump(temp, open("../KeyPoints128/SURF_object_"+str(numb_features)+"/keypoints_"+infile[3:-4]+".p", "wb"))



def save_hists(img_path, folders):

	for j in folders:

		path = img_path+j

		for infile in glob.glob( os.path.join(path, '*.jpg') ):

			img1 = cv2.imread(infile,0) 

			print(infile)

			#hist = hist_tiles(img1)
			blur = cv2.blur(img1,(5,5))
			hist = cv2.calcHist([blur],[0],None,[256],[0,256])

			#Store and Retrieve keypoint features
			infile = infile.replace("/", "+")

			pickle.dump(hist, open("../Hists/Object_blur/hists_"+infile[3:-4]+".p", "wb"))



# save_SIFT(img_path, folders)
# save_SIFT(img_path, folders, 400)
# save_SIFT(img_path, folders, 500)
# save_SIFT(img_path, folders, 600)

# save_SURF(img_path, folders, 300)
# save_SURF(img_path, folders, 400)
# save_SURF(img_path, folders, 500)
#save_SURF(img_path, folders, 600)

save_hists(img_path, folders)


