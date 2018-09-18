from operator import itemgetter
import operator
import fnmatch
import numpy as np
from GoogleGlass.Image_recognition.Code.help_funcs import replace_str_index, reverse_numeric, find_listcomp, find_second_last, find_second, find_nth
from GoogleGlass.Image_recognition.Code.help_funcs import get_folder_from_path, same_folder, same_folder_list, get_image_id, check_id, check_id_rank
from GoogleGlass.Image_recognition.Code.result_paths import results_files_path

# from help_funcs import replace_str_index, reverse_numeric, find_listcomp, find_second_last, find_second, find_nth
# from help_funcs import get_folder_from_path, same_folder, same_folder_list, get_image_id, check_id, check_id_rank
# from result_paths import results_files_path



def sort_matches(all_chosen_files, test_path):

  ranked_ssim =[]
  ranked_correl =[]
  ranked_dist = []
  combined_ranks = []
  best_matches_rank = []
  best_match_ssim = ""
  best_match_correl = ""
  best_match_dist = ""
  

  # sort by ssim
  sorted_ssim = sorted(all_chosen_files, key=operator.itemgetter(1), reverse=True)
  if sorted_ssim:
    best_match_ssim = sorted_ssim[0][0]

  # sort by distance
  sorted_dists = sorted(all_chosen_files, key=operator.itemgetter(2))
  if sorted_dists:
    best_match_dist = sorted_dists[0][0]

  #sort by correl
  sorted_correl = sorted(all_chosen_files, key=operator.itemgetter(3), reverse=True)
  if sorted_correl:
    best_match_correl = sorted_correl[0][0]

  # add ranking
  count = 0
 
  for i in sorted_ssim:
    ranked_ssim.append((sorted_ssim[count][0],count+1))
    ranked_correl.append((sorted_correl[count][0],count+1))
    ranked_dist.append((sorted_dists[count][0],count+1))
    count = count+1

  count2 = 0
  for i in ranked_ssim:

    combined_rank = np.median([find_listcomp(ranked_ssim, ranked_ssim[count2][0]),
                             find_listcomp(ranked_dist, ranked_ssim[count2][0]), 
                             find_listcomp(ranked_correl, ranked_ssim[count2][0])])
    #combined_rank = (find_listcomp(ranked_ssim, ranked_ssim[count2][0]))+(find_listcomp(ranked_dist, ranked_ssim[count2][0]))+(find_listcomp(ranked_correl, ranked_ssim[count2][0]))
    combined_ranks.append((ranked_ssim[count2][0],combined_rank))
    count2 = count2 +1

  sorted_ranks = sorted(combined_ranks, key = operator.itemgetter(1))

  if sorted_ranks:
    best_matches_rank.append(sorted_ranks[0][0])

    for i in range(1,len(sorted_ranks)):
      if sorted_ranks[0][1] == sorted_ranks[i][1]:
        best_matches_rank.append(sorted_ranks[i][0])

  print("\nSorted by ssim: ", sorted_ssim, '\n')
  print("\nSorted by correl: ", sorted_correl, '\n')
  print("Sorted by SURF distance: ", sorted_dists, '\n')
  print("Sorted by ranks: ", sorted_ranks, '\n')

  cut = find_second_last(test_path, '/')
  resultFile = results_files_path+test_path[cut:-4]+'.txt'
  print("resultFile: ",resultFile)
  script_ = open(resultFile, 'w')
  script_.write("Test image: "+test_path + '\n\n')
  script_.write("Best matches by rank: " +str(best_matches_rank)+ '\n\n')
  script_.write("Best matches by SURF distance: "+str(best_match_dist)+ '\n\n')
  script_.write("Best matches ssim: "+str(best_match_ssim)+ '\n\n')
  script_.write("Best matches correl: "+str(best_match_correl)+ '\n\n')
  script_.write("Sorted by ssim: "+str(sorted_ssim)+'\n\n')
  script_.write("Sorted by correl: "+str(sorted_correl)+'\n\n')
  script_.write("Sorted by SURF distance: "+str(sorted_dists)+ '\n\n')
  script_.write("Sorted by ranks: "+str(sorted_ranks)+ '\n')
  script_.write("------------------------------------------------------------------------\n\n")
  script_.close()
  
  testpath_pos = find_testpath_position(test_path, sorted_ssim, sorted_correl, sorted_dists ,sorted_ranks)
  
  return([best_matches_rank, best_match_dist, best_match_ssim, best_match_correl], testpath_pos)


def get_most_freq_matches(best_matches):

  most_freq_folders = []
  counter_folders = []
  counter_list = []
  same_counts = []
  paths_counter = []

  if(best_matches):

    best_matches_rank = best_matches[0]
    best_match_dist = best_matches[1]
    best_match_ssim = best_matches[2]
    best_match_correl = best_matches[3]

    

    for i in best_matches_rank:
      most_freq_folders.append((i, get_image_id(i),get_folder_from_path(i)))
    most_freq_folders.append((best_match_dist,get_image_id(best_match_dist), get_folder_from_path(best_match_dist)))
    most_freq_folders.append((best_match_ssim,get_image_id(best_match_ssim),get_folder_from_path(best_match_ssim)))
    most_freq_folders.append((best_match_correl,get_image_id(best_match_correl),get_folder_from_path(best_match_correl)))

    
    if(most_freq_folders):
      counter_folders.append((most_freq_folders[0][0], most_freq_folders[0][1], most_freq_folders[0][2]))
      counter_list.append(1)

    
    i = 1

    for p in most_freq_folders[1:]:

      check = 0

      for j in range(0,len(counter_folders)):

        # if id and room/floor the same
        if most_freq_folders[i][2] == counter_folders[j][2] and most_freq_folders[i][1] == counter_folders[j][1]:
          counter_list[j]= counter_list[j]+1
          check = 1

      if(check == 0):
        counter_folders.append((most_freq_folders[i][0], most_freq_folders[i][1], most_freq_folders[i][2]))
        counter_list.append(1)
      i = i+1

   
    same_counts.append(counter_list[0])

    for j in range(1, len(counter_list)):
      if j == same_counts[0]:
        same_counts.append(j)

    for i in range(0,len(same_counts)):
      paths_counter.append(counter_folders[i][0])

  return paths_counter




def count_matches(test_folder, test_path, best_matches, paths_counter, script_overview, time_):

  best_matches_counter = paths_counter
  best_matches_rank = best_matches[0]
  best_match_dist = best_matches[1]
  best_match_ssim = best_matches[2]
  best_match_correl = best_matches[3]
  id_ssim = ""
  id_correl = ""
  id_surf =""
  id_rank = []
  id_counter = []

  match_rank = []
  match_counter = []

  rank_folders = []
  counter_folders = []

  # is the result image from the same room as the test image?

  cut1 = test_folder.find('/')
  ssim_folder = get_folder_from_path(best_match_ssim)
  surf_folder = get_folder_from_path(best_match_dist)
  correl_folder = get_folder_from_path(best_match_correl)


  #matched_folders = [ssim_folder, surf_folder, correl_folder]

  match_ssim = same_folder(ssim_folder, test_folder[:cut1])
  match_surf = same_folder(surf_folder,test_folder[:cut1])
  match_correl = same_folder(correl_folder,test_folder[:cut1])


  for i in best_matches_rank:
    rank_folder = get_folder_from_path(i)
    rank_folders.append(rank_folder)
  
  match_rank = same_folder_list(rank_folders, test_folder[:cut1])


  for i in best_matches_counter:
    counter_folder = get_folder_from_path(i)
    counter_folders.append(counter_folder)
  
  match_counter = same_folder_list(counter_folders, test_folder[:cut1])


  # if yes, is the same object in the result image as in the test image?
  #'./Test_Pics_B11/3OG_R308/Object/1_2_3OG_R308.jpg'
  if match_ssim == 1: 
    id_ssim= get_image_id(best_match_ssim)

  if match_correl == 1: 
    id_correl= get_image_id(best_match_correl)

  if match_surf ==1:
    id_surf = get_image_id(best_match_dist)

  for k in range(0,len(match_rank)):
    if match_rank[k] ==1:
      id_rank.append(get_image_id(best_matches_rank[k]))

  for k in range(0,len(match_counter)):
    if match_counter[k] ==1:
      id_counter.append(get_image_id(best_matches_counter[k]))


  id_testpath = get_image_id(test_path)

   # check if the room is the same and then the id
  id_match_ssim = check_id(id_ssim,id_testpath)
  id_match_correl = check_id(id_correl,id_testpath)
  id_match_surf = check_id(id_surf,id_testpath)
  id_match_rank = check_id_rank(id_rank, id_testpath)
  id_match_counter = check_id_rank(id_counter, id_testpath)


  script_overview.write(test_path+"\t\t\t\t\t\t"+ str(match_ssim)+"/"+str(id_match_ssim)
                                  +"\t\t\t"+  str(match_correl) +"/"+str(id_match_correl)
                                  +"\t\t\t"+  str(match_surf) +"/"+str(id_match_surf)
                                  +"\t\t\t"+ str(match_rank)+"/"+str(id_match_rank)
                                  +"\t\t\t"+ str(match_counter)+"/"+str(id_match_counter)
                                  +"\t\t"+ str(time_)+"\n\n")
  
  return([match_rank, match_surf, match_ssim, match_correl, match_counter], [id_match_rank, id_match_surf, id_match_ssim, id_match_correl, id_match_counter])



def find_testpath_position(test_path, sorted_ssim, sorted_correl, sorted_dists ,sorted_ranks):

  # find position of correct match in sorted lists
  # testpath: Test_Pics_B11/1OG_Flur194/Entrance_Test/1_3_1OG_Flur194.jpg
  # search for it in sorted_ssim ...
  # 
  # 
  cut = test_path.rfind('/')
  testpath_wild = test_path[cut+1:]
  cut1 = testpath_wild.find('_')

  testpath_wild = replace_str_index(testpath_wild, cut1+1,'*')

  paths_dist = []
  for paths in sorted_dists:

    cut = paths[0].rfind('/')
    paths_dist.append(paths[0][cut+1:])

  paths_ssim = []
  for paths in sorted_ssim:

    cut = paths[0].rfind('/')
    paths_ssim.append(paths[0][cut+1:])

  paths_correl = []
  for paths in sorted_correl:

    cut = paths[0].rfind('/')
    paths_correl.append(paths[0][cut+1:])


  paths_rank = []
  for paths in sorted_ranks:

    cut = paths[0].rfind('/')
    paths_rank.append(paths[0][cut+1:])

  testpath_pos_dist = []
  count = 1
  for i in paths_dist:
    if fnmatch.fnmatch(i, testpath_wild):
      testpath_pos_dist.append(count)
    count = count +1

  testpath_pos_ssim = []
  count = 1
  for i in paths_ssim:
    if fnmatch.fnmatch(i, testpath_wild):
      testpath_pos_ssim.append(count)
    count = count +1

  testpath_pos_correl = []
  count = 1
  for i in paths_correl:
    if fnmatch.fnmatch(i, testpath_wild):
      testpath_pos_correl.append(count)
    count = count +1

  testpath_pos_rank = []
  count = 1
  for i in paths_rank:
    if fnmatch.fnmatch(i, testpath_wild):
      testpath_pos_rank.append(count)
    count = count +1


  return([testpath_pos_dist, testpath_pos_ssim, testpath_pos_correl, testpath_pos_rank])