
def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def reverse_numeric(x, y):
  return y - x

# find a given value in a list
def find_listcomp(list_, value):
    z = [elem for elem in list_ if elem[0] == value]
    return z[0][1]

def find_second_last(text, pattern):
  return text.rfind(pattern, 0, text.rfind(pattern))

def find_second(text, pattern):
  return text.find(pattern, 0, text.find(pattern))

def find_nth(text, pattern, n):
    start = text.find(pattern)
    while start >= 0 and n > 1:
        start = text.find(pattern, start+len(pattern))
        n -= 1
    return start

# attention if paths have changed!
def get_folder_from_path(path):

  cut2 = find_nth(path, '/', 3) #2
  cut3 = find_nth(path, '/', 4) #3
  
  return path[cut2+1:cut3]


def same_folder(folder_path1, folder_path2):

  if folder_path1 == folder_path2:
    return 1
  else:
    return 0

def same_folder_list(folder_list_rank, folder_path2):

  matches = []
  for i in folder_list_rank:

    if i == folder_path2:
      matches.append(1)
    else:
      matches.append(0)

  return matches

def get_image_id(path_):

  cut1 = path_.rfind('/')
  cut2 = path_[cut1:].find('_')
  id_ = path_[cut1+1:cut1+cut2]

  return id_

def get_image_object_id(path_):
  cut1 = path_.rfind('/')
  cut2 = find_nth(path_[cut1:], '_',2)
  cut3 = path_[cut1+cut2+1:].find('_')
  object_id = path_[cut1+cut2+1:cut1+cut2+cut3+1]
  return object_id


def check_id(id_, id_test):
  if(id_== id_test):
    return 1
  else:
    return 0

def check_id_rank(id_rank, id_test):
  id_check = []
  if id_rank:
    for i in id_rank:
      if i == id_test:
        id_check.append(1)
      else:
        id_check.append(0)
  else:
    id_check.append(0)

  return id_check

def get_sums_rank(sum_rank, sum_id_rank):
  sum_rank2 = 0
  sum_id_rank2 = 0
  sum_id_rank3 = []

  check1 = 0
  for i in sum_rank:
    for j in i:
      if j == 1:
        check1 =1
    if(check1 ==1):
      sum_rank2 = sum_rank2 + 1
    check1 = 0


  check1 = 0
  for i in sum_id_rank:
    for j in i:
      if j == 1:
        check1 =1
    if(check1 ==1):
      sum_id_rank2 = sum_id_rank2 + 1
      sum_id_rank3.append(1)
    else:
      sum_id_rank3.append(0)
    check1 = 0

  return(sum_rank2, sum_id_rank2, sum_id_rank3)

def cut_image_at_sift_keypoints(img1, pts):

  xx = []
  yy = []

  for i in pts:
    for x,y in i:
      xx.append(x)
      yy.append(y)
            
  # xx, yy = zip(itertools.repeat(*kp_points))
  min_x = min(xx); min_y = min(yy); max_x = max(xx); max_y = max(yy)

  w1,h1 = img1.shape

  h1 = max_y - min_y
  w1 = max_x - min_x

  a1 = int(round(min_y))
  a2 = int(round(min_y+h1))
  b1 = int(round(min_x))
  b2 = int(round(min_x+w1))

  crop = img1[a1:a2, b1:b2]

  return crop

def hist_tiles(img):

  tile1 = int(img.shape[0]/3)
  tile2 = int(img.shape[1]/3)

  tile1_ = tile1
  tile2_ = tile2

  start1 = 0
  start2 = 0

  all_hists = [] 

  #color = ('b','g','r')
  
  for j in range(0,3):

    for i in range(0,3):

      img_new=img[start1:tile1, start2:tile2]

      hist = cv2.calcHist([img],[0],None,[256],[0,256])
      # for i,col in enumerate(color):

      #   hist = cv2.calcHist([img_new],[i],None,[256],[0,256])

      all_hists.append(hist)

      tile1 = tile1 + tile1_
      start1 = start1+ tile1_

    tile2 = tile2 + tile2_
    start2 = start2+ tile2_

    start1 = 0
    tile1 = tile1_  

  return all_hists


def hist_correlation(test_hists, hists):

  correl = []

  for i in range(0,len(test_hists)):

    correl.append(cv2.compareHist(test_hists[i],hists[i],cv2.HISTCMP_CORREL))

  return np.sum(correl)
