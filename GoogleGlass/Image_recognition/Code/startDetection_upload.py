# used source:
# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html

import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import pickle
import os
import glob
import operator
import math
import sys
from operator import itemgetter
from PIL import Image
import time
import fnmatch
import itertools
from skimage.measure import compare_ssim as ssim
from GoogleGlass.Image_recognition.Code.sort_count_funcs import sort_matches, count_matches, find_testpath_position, get_most_freq_matches
from GoogleGlass.Image_recognition.Code.plot_funcs import plot_best_matches, plot_diagram_matches, plot_diagram_match_position
from GoogleGlass.Image_recognition.Code.result_paths import resultOverview_path, result_multiple_rounds_sift
from GoogleGlass.Image_recognition.Code.help_funcs import get_image_object_id, get_sums_rank, cut_image_at_sift_keypoints
from GoogleGlass.Image_recognition.Code.pickle_funcs import unpickle_keypoints
from GoogleGlass.Image_recognition.Code.color_balance import simplest_cb
from GoogleGlass.Image_recognition.Code.crop_that_shit import crop_img_for_hist, calc_best_hist
from GoogleGlass.Image_recognition.Code.testfiles1 import folders_object, folders_object_test
from GoogleGlass.Image_recognition.Code.testfiles1 import sift_keypoints_file_obj, surf_keypoints_file_obj_600, surf128_keypoints_file_obj_600, hist_file_obj, hist_file_obj_blur

# from sort_count_funcs import sort_matches, count_matches, find_testpath_position, get_most_freq_matches
# from plot_funcs import plot_best_matches, plot_diagram_matches, plot_diagram_match_position
# from result_paths import resultOverview_path, result_multiple_rounds_sift
# from help_funcs import get_image_object_id, get_sums_rank, cut_image_at_sift_keypoints
# from pickle_funcs import unpickle_keypoints
# from color_balance import simplest_cb
# from crop_that_shit import crop_img_for_hist, calc_best_hist


img_path = '/Test_Pics_B11/'
MIN_MATCH_COUNT_matches = 20
MIN_MATCH_COUNT_inliers = 10
matplotlib.rcParams.update({'font.size':5}) # text size for images plotting
# Initiate SIFT/SURF detector
#surf = cv2.xfeatures2d.SURF_create(400)
#sift = cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create(hessianThreshold = 600)



def find_best_match(test_img_path, keypoints_file, hist_file, folders, predicted_obj):

  all_chosen_files = [] # includes all images with their ssim and distance to the test image
  # imread rgb image for histogram
  # imread grey scale image for computing SURF keypoints
  #test_img_path = "r^"+test_img_path
  img1 = cv2.imread(test_img_path,0) 
  print("\n---------------------------")
  print("Test image: ",test_img_path)
  kp2, des2 = surf.detectAndCompute(img1,None)
  blur1 = cv2.blur(img1,(5,5))
  hist1 = cv2.calcHist([blur1],[0],None,[256],[0,256])  
  #kp2, des2 = sift.detectAndCompute(test_img1,None)
  #test_img_hists = hist_tiles(test_img1)

  for path in folders:

    for infile in glob.glob( os.path.join(path, '*.jpg') ):

      if get_image_object_id(infile) == predicted_obj or get_image_object_id(infile) == "hf":

        print(infile)
         # imread grey scale image
        img2 = cv2.imread(infile,0)
       
        # get stored keypoints
        infile_repl = infile.replace("/", "+")
        keypoints_file1 = keypoints_file+infile_repl[63:-4]+".p"
        print("keypoints_file1:", keypoints_file1)
        

        if os.path.isfile(keypoints_file1):
          keypoints_database = pickle.load( open(keypoints_file1, "rb" ) )
          kp1, des1 = unpickle_keypoints(keypoints_database)
        else: 
          kp1, des1 = surf.detectAndCompute(img2,None)
          #kp1, des1 = sift.detectAndCompute(img2,None)
          print("No stored KeyPoints available. Calculating keypoints...")


        # kpTest, desTest = surf.detectAndCompute(img2,None)
        # http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   # higher values gives better precision, but also take more time
        flann = cv2.FlannBasedMatcher(index_params,search_params)


        matches = flann.knnMatch(des1,des2,k=2)



        #################
        ################
        
        # store all the good matches as per Lowe's ratio test.
        good = []
        #print("matches: ", len(matches))
        for m,n in matches:
          if m.distance < 0.7*n.distance:
            good.append(m)
            #print("m: ", m)
            #print("n: ", n)


        if len(good)>MIN_MATCH_COUNT_matches:

            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            inliers = []
            for i in range(0, len(good)):
              if matchesMask[i] == 1:
                inliers.append(good[i])
            
         

            if len(inliers) >= MIN_MATCH_COUNT_inliers:

              inlier_distances = []
              for i in inliers:
                inlier_distances.append(i.distance)

              sorted_distSum = sorted(inlier_distances)
              sum_sorted_distSum = sum(sorted_distSum[:10])

              print("sum_sorted_distSum: ", sum_sorted_distSum)




              h,w = img2.shape
              #pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
              #dst = cv2.perspectiveTransform(pts,M)

              #img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

              if img2.shape != img1.shape:
                img1=cv2.resize(img1,(img2.shape[1],img2.shape[0]))

              # apply ssim
              ssim_const = ssim(img1, img2, data_range = img2.max() - img2.min())
              
              #####TRY CROP IMAGE VERSION ###
              
              # crop1 = cut_image_at_sift_keypoints(img1, dst_pts)
              # crop2 = cut_image_at_sift_keypoints(img2, dst_pts)
              # hist1 = cv2.calcHist([crop1],[0],None,[256],[0,256])
              # hist2 = cv2.calcHist([crop2],[0],None,[256],[0,256])
              # correl_ = cv2.compareHist(hist1,hist2,cv2.HISTCMP_CORREL)

              #####
              
              ### try different ratios
              # crop_img1 = crop_img_for_hist(img1, str("l"))
              # crop_img2 = crop_img_for_hist(img2, str("l"))

              # [imgs, correl_] = calc_best_hist(img1, img2, crop_img1, crop_img2)

              # img1 = imgs[0]
              # img2 = imgs[1]

              # fig = plt.figure()
              # plt.subplot(2,1,1)
              # plt.imshow(img1)
              # plt.subplot(2,1,2)
              # plt.imshow(img2)
              # plt.show()
              ####

              hist_file1 = hist_file+infile_repl[3:-4]+".p"

              if os.path.isfile(hist_file1):
                hist2 = pickle.load( open(hist_file1, "rb" ) )
              else: 
                hist2 = cv2.calcHist([img2],[0],None,[256],[0,256])
              
              correl_ = cv2.compareHist(hist1,hist2,cv2.HISTCMP_CORREL)
              print("correl_: ", correl_)

              all_chosen_files.append((infile, ssim_const, sum_sorted_distSum, correl_))


            else:
              print("Not enough matches are found - %d/%d" % (len(inliers),MIN_MATCH_COUNT_inliers))
              matchesMask = None

        else:
              print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT_matches))
              matchesMask = None

        ################
        ###############        
  
  return all_chosen_files


def run_script(test_path, predicted_obj, folder, keypoints_file, hist_file):

  exe_time = 0
  # sum_ssim = 0
  # sum_correl = 0
  # sum_surf = 0
  # sum_rank = []
  # sum_counter = []
  # sum_id_ssim = []
  # sum_id_correl = []
  # sum_id_surf = []
  # sum_id_rank = []
  # sum_id_counter = []

  len_testpath = 0
  count_testpaths = 0
  testpaths = []
  testpath_pos_dist = []
  testpath_pos_ssim = []
  testpath_pos_correl = []
  testpath_pos_rank = [] 
  testpath_pos_counter = []
  sum_results_str = str("")

  # script_overview = open(resultOverview_path, 'w')
  # script_overview.write("Test image \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tSSIM\t\tCORREL\t\tSURF\t\tRANK\t\tCOUNTER\t\t\tTIME\n\n")
  # script_overview.write("Match \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tRoom/Image\t\tRoom/Image\t\tRoom/Image\t\tRoom/Image\tRoom/Image\n\n")


  print("test_path: ", test_path)
  start_time2 = time.time()

  #predicted_obj = get_image_object_id(test_path)
  len_testpath = len(test_path)

  if(os.path.exists(test_path)):

    start_time = time.time()
    count_testpaths = count_testpaths + 1
    test_img = cv2.imread(test_path)      

    all_files = find_best_match(test_path, keypoints_file, hist_file, folder, predicted_obj) 
    [best_matches, testpath_pos]  = sort_matches(all_files, test_path)
    paths_counter = get_most_freq_matches(best_matches)
    path_time = time.time() - start_time
    # [sum_matches, sum_id_matches] = count_matches(j, test_path, best_matches, paths_counter, script_overview, path_time)
    # sum_correl = sum_correl + sum_matches[3]
    # sum_ssim = sum_ssim + sum_matches[2]
    # sum_surf = sum_surf + sum_matches[1]
    # sum_rank.append(sum_matches[0])
    # sum_counter.append(sum_matches[4])

    # sum_id_correl.append(sum_id_matches[3])
    # sum_id_ssim.append(sum_id_matches[2])
    # sum_id_surf.append(sum_id_matches[1])
    # sum_id_rank.append(sum_id_matches[0])
    # sum_id_counter.append(sum_id_matches[4])

    testpath_pos_dist.append(testpath_pos[0])
    testpath_pos_ssim.append(testpath_pos[1])
    testpath_pos_correl.append(testpath_pos[2])
    testpath_pos_rank.append(testpath_pos[3])

    sum_results_str = sum_results_str + plot_best_matches(best_matches, test_path)
    testpaths.append(test_path)

    exe_time = exe_time +path_time
  else:
    print(str(test_path)+" does not exist.")

  #[sum_rank2, sum_id_rank2, sum_id_rank3] = get_sums_rank(sum_rank, sum_id_rank)
  #[sum_counter2, sum_id_counter2, sum_id_counter3] = get_sums_rank(sum_counter, sum_id_counter)

  print("execution time: ", exe_time)
  # sum_results = str("Sum: \t\t"+str(count_testpaths)+((len_testpath-5)*" ")+"\t\t\t\t"
  #               + str(sum_ssim)+"/"+str(np.sum(sum_id_ssim))+"\t\t"+  str(sum_correl)+"/"
  #               +str(np.sum(sum_id_correl))+"\t\t"+  str(sum_surf)+"/"+str(np.sum(sum_id_surf))+"\t\t\t"
  #               + str(sum_rank2)+"/"+str(sum_id_rank2)+"\t\t\t"
  #               + str(sum_counter2)+"/"+str(sum_id_counter2)+"\t\t\t"
  #               +str(exe_time) +"\n\n")
  # script_overview.write(sum_results)
  # script_overview.close()

  #plot_diagram_matches(testpaths, sum_id_rank3, sum_id_ssim, sum_id_correl, sum_id_surf)
  #plot_diagram_match_position(testpaths, testpath_pos_dist, testpath_pos_ssim, testpath_pos_correl, testpath_pos_rank)

  return sum_results_str

  

def main(test_file, predicted_obj):

    #from testfiles5 import folders_entrance, folders_entrance_test
    #from testfiles1 import folders_object, folders_object_test
    #from testfile5 import sift_keypoints_file_entrance, surf_keypoints_file_entrance_600
    #from testfiles1 import sift_keypoints_file_obj, surf_keypoints_file_obj_600, surf128_keypoints_file_obj_600, hist_file_obj, hist_file_obj_blur
    sum_ =run_script(test_file, predicted_obj, folders_object, surf_keypoints_file_obj_600, hist_file_obj_blur)
    return(sum_)

   
    #sift = cv2.xfeatures2d.SIFT_create()
    #surf = cv2.xfeatures2d.SURF_create(600)
    #surf.setExtended(True)
    #sum_ =run_script(folders_entrance_test, folders_entrance, sift_keypoints_file_entrance, surf_keypoints_file_entrance_600)
    ##sum_ =run_script(folders_object_test, folders_object, surf_keypoints_file_obj_600, hist_file_obj_blur)
