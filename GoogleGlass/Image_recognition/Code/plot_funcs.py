from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import numpy as np
import math
from GoogleGlass.Image_recognition.Code.help_funcs import find_second_last
from GoogleGlass.Image_recognition.Code.result_paths import image_plots_path, scatter_plt_matches_path, scatter_plt_matches_pos_path
#from help_funcs import find_second_last
#from result_paths import image_plots_path, scatter_plt_matches_path, scatter_plt_matches_pos_path

def plot_best_matches(best_matches, test_img_path):

  print('best_matches:',best_matches)
  print('\n')

  sum_results_str = str("")

  if not len(best_matches[0])==0:
    best_matches.append(test_img_path)
    titles = ["best ranked img", "best SURF img", "best ssim img", "best correl img", "test img"]
    number_of_plots = len(best_matches[0])+4

    #fig = plt.figure()
    #fig.tight_layout() 
    

    for i in range(0,len(best_matches)):

      if i ==0:

        for j in range(0,len(best_matches[0])):

          #a=fig.add_subplot(math.ceil(number_of_plots/2),2,j+1)
          #img=mpimg.imread(best_matches[0][j])
          #cut = find_second_last(best_matches[0][j], '/')
          #a.set_title(titles[i]+str(j)+': '+str(best_matches[0][j][cut:]))
          matches1 = str(titles[i])+str(j)+ "Path: "+ str(best_matches[0][j]+"\n")
          print(matches1)
          sum_results_str = sum_results_str + matches1
          #plt.axis('off')
          #plt.imshow(img)
      else:
        #a=fig.add_subplot(math.ceil(number_of_plots/2),2,i+j+1)
        #img=mpimg.imread(best_matches[i])
        #cut = find_second_last(best_matches[i][:], '/')
        #a.set_title(titles[i]+': '+str(best_matches[i][cut:]))
        matches2 = str(titles[i])+ "Path: " + str(best_matches[i]+"\n")
        print(matches2)
        sum_results_str = sum_results_str + matches2

        #plt.axis('off')
        #plt.imshow(img)


    #cut = find_second_last(test_img_path, '/')
    #plt.savefig(image_plots_path+test_img_path[cut:])

    #plt.clf()
    #plt.show()
    return sum_results_str


def plot_diagram_matches(testpaths, sum_id_rank, sum_id_ssim, sum_id_correl, sum_id_surf):

  # testpaths = ['Test_Pics_B11/1OG_Flur192/Entrance_Test/0_3_1OG_Flur192.jpg', 'Test_Pics_B11/1OG_Flur194/Entrance_Test/0_3_1OG_Flur194.jpg'
  #             , 'Test_Pics_B11/3OG_Flur194/Entrance_Test/0_3_3OG_Flur308.jpg', 'Test_Pics_B11/2OG_Flur192/Entrance_Test/1_2_2OG_Flur292.jpg', 
  #             'Test_Pics_B11/EG_Flur194/Entrance_Test/1_2_EG_Flur095.jpg', 'Test_Pics_B11/EG_Flur194/Entrance_Test/1_1_EG_Flur092.jpg']

  # sum_id_rank = [0,0,1,1,0,1]
  # sum_id_ssim  = [1,1,0,1,1,1]
  # sum_id_correl = [1,0,0,1,0,1]
  # sum_id_surf = [0,0,1,1,1,1]
  # 
  # print("sum_id_rank: ", sum_id_rank)
  # print("sum_id_ssim: ", sum_id_ssim)
  # print("sum_id_correl: ", sum_id_correl)
  # print("sum_id_surf: ", sum_id_surf)


  testpaths2 = []
  for i in testpaths:
    cut = i.rfind("/")
    testpaths2.append(i[cut+1:])

  y1 = sum_id_surf
  y2 = sum_id_ssim
  y3 = sum_id_correl
  y4 = sum_id_rank

  x = range(0,len(testpaths2))
  x1 = np.arange(0.1, len(testpaths2)+0.1, 1)
  x2 = np.arange(0.2, len(testpaths2)+0.2, 1)
  x3 = np.arange(0.3, len(testpaths2)+0.3, 1)

  plt_dist = plt.scatter(x,y1, marker='^', c = 'r')
  plt_ssim = plt.scatter(x1, y2, marker='*', c= 'g')
  plt_correl = plt.scatter(x2, y3, marker='o', c = 'b')
  plt_rank = plt.scatter(x3, y4, marker='+', c = 'y')
 

  plt.legend((plt_dist, plt_ssim, plt_correl, plt_rank),('SURF', 'ssim', 'correlation', 'rank'),scatterpoints=1,loc='center right',ncol=2,fontsize=8)
  plt.xticks(x)
  plt.yticks([0,1])
  plt.axes().set_xticklabels(testpaths2, rotation=90)
  plt.axes().set_yticklabels(["not detected", "detected"])
  plt.xlabel('test images')
  plt.ylabel('detection')
  plt.title('Test image recognition ')
  plt.tight_layout()
  #plt.show()
  plt.savefig(scatter_plt_matches_path)
  plt.clf()



def plot_diagram_match_position(testpaths, testpath_pos_dist, testpath_pos_ssim, testpath_pos_correl, testpath_pos_rank):

 
  # testpaths = ['Test_Pics_B11/1OG_Flur192/Entrance_Test/0_3_1OG_Flur192.jpg', 'Test_Pics_B11/1OG_Flur194/Entrance_Test/0_3_1OG_Flur194.jpg'
  #              , 'Test_Pics_B11/3OG_Flur194/Entrance_Test/0_3_3OG_Flur308.jpg']

  # testpath_pos_dist = [[1, 6, 7], [1, 5, 13], [1, 2, 6]]
  # testpath_pos_ssim = [[1, 6, 7], [11, 12, 15], [10, 13, 14]]
  # testpath_pos_correl = [[1, 2, 17], [1, 12, 19], [1, 8, 25]]
  # testpath_pos_rank = [[1, 3, 4], [3, 13, 15], [1, 4, 14]]


  testpaths2 = []
  for i in testpaths:
    cut = i.rfind("/")
    testpaths2.append(i[cut+1:])

  y1 = testpath_pos_dist
  y2 = testpath_pos_ssim
  y3 = testpath_pos_correl
  y4 = testpath_pos_rank

  x = range(0,len(testpaths2))
  x1 = np.arange(0.1, len(testpaths2)+0.1, 1)
  x2 = np.arange(0.2, len(testpaths2)+0.2, 1)
  x3 = np.arange(0.3, len(testpaths2)+0.3, 1)

  for xe, ye in zip(x, y1):
      plt_dist = plt.scatter([xe] * len(ye), ye, marker='^', c = 'r')
  for xe, ye in zip(x1, y2):
      plt_ssim = plt.scatter([xe] * len(ye), ye, marker='*', c= 'g')
  for xe, ye in zip(x2, y3):
      plt_correl = plt.scatter([xe] * len(ye), ye, marker='o', c = 'b')
  for xe, ye in zip(x3, y4):
      plt_rank = plt.scatter([xe] * len(ye), ye, marker='+', c = 'y')


  plt.legend((plt_dist, plt_ssim, plt_correl, plt_rank),('SURF', 'ssim', 'correlation', 'rank'),scatterpoints=1,loc='upper left',ncol=2,fontsize=8)
  plt.xticks(x)
  plt.axes().set_xticklabels(testpaths2, rotation=90)
  plt.xlabel('test images')
  plt.ylabel('position of correct matches')
  plt.title('Position of correct matches in algorithm rankings')
  plt.tight_layout()
  #plt.show()
  plt.savefig(scatter_plt_matches_pos_path)
  plt.clf()

