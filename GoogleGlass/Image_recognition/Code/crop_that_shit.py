import cv2
from matplotlib import pyplot as plt
import numpy as np
import operator

def crop_img_for_hist(img1, size_):


  h,w = img1.shape

  print("w: ", w)
  print("h: ", h)

  if(size_ == "l"):

  	r1 = int(h*(1/8))
  	r2 = int(w*(1/8))

  	crop = img1[r1:h-r1, r2:w-r2]

  # fig = plt.figure()
  # plt.subplot(2,1,1)
  # plt.imshow(img1)
  # plt.subplot(2,1,2)
  # plt.imshow(crop)
  # plt.show()

  return crop

def calc_best_hist(img1, img2, crop_img1, crop_img2):

	
	img1_hist = cv2.calcHist([img1],[0],None,[256],[0,256]) 
	img2_hist = cv2.calcHist([img2],[0],None,[256],[0,256]) 

	crop_img1_hist = cv2.calcHist([crop_img1],[0],None,[256],[0,256]) 
	crop_img2_hist = cv2.calcHist([crop_img2],[0],None,[256],[0,256])  

	correl_img1_img2 = cv2.compareHist(img1_hist,img2_hist,cv2.HISTCMP_CORREL)
	correl_cropimg1_img2 = cv2.compareHist(crop_img1_hist,img2_hist,cv2.HISTCMP_CORREL)
	correl_img1_cropimg2 = cv2.compareHist(img1_hist,crop_img2_hist,cv2.HISTCMP_CORREL)


	# print("correl_img1_img2", correl_img1_img2)
	# print("correl_cropimg1_img2", correl_cropimg1_img2)
	# print("correl_img1_cropimg2", correl_img1_cropimg2)

	all_correls = [correl_img1_img2, correl_cropimg1_img2, correl_img1_cropimg2]

	max_ = np.max(all_correls)

	index_ = 0
	for i in range(0,len(all_correls)):
		if all_correls[i] == max_:
			index_ = i

	combis_ = [[img1, img2],[crop_img1, img2],[img1, crop_img2]]

	return (combis_[index_], max_)

	#return np.max([correl_img1_img2, correl_cropimg1_img2, correl_img1_cropimg2])




# img1 = cv2.imread("../Test_Pics_B11/EG_Flur092/Object/0_1_h_EG_Flur092.jpg",0) 
# img2 = cv2.imread("../Test_Pics_B11/3OG_Flur394/Object/1_1_h_3OG_Flur394.jpg",0)
# #img2 = cv2.imread("../Test_Pics_B11/EG_Flur092/Object_Test/0_3_h_EG_Flur092.jpg",0)


# crop_img1 = crop_img_for_hist(img1, str("l"))
# crop_img2 = crop_img_for_hist(img2, str("l"))
# [img, max_] = calc_best_hist(img1, img2, crop_img1, crop_img2)

# img1 = img[0]
# img2 = img[1]

# hist1= cv2.calcHist([img1],[0],None,[256],[0,256]) 
# hist2 = cv2.calcHist([img2],[0],None,[256],[0,256]) 
# correl = cv2.compareHist(hist1,hist2,cv2.HISTCMP_CORREL)
# print("best correl: ", correl)
