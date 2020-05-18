# initializing list
from os.path import isfile, join
from os import listdir
test_list = ['I', 'L', 'O', 'V', 'E', 'G', 'F', 'G']

# printing original list
print("The original list is : " + str(test_list))

# using join() + list slicing
# merging list elements
test_list[5: 8] = [''.join(test_list[5: 8])]

# printing result
print("The list after merging elements : " + str(test_list))


data_folder = "./data/download"

# listof_pdf_files_in_download_folder = [f for f in listdir(
#     data_folder) if isfile(join(data_folder, f))]

# listof_pdf_files_in_download_folder = ["./data/download/" + f for f in listdir(
#     data_folder) if isfile(join(data_folder, f))]

# print(listof_pdf_files_in_download_folder)

import glob
print(glob.glob("./data/download/*.pdf"))
