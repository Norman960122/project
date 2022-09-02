import numpy as np
file_name = input("enter file name to write:")
time_to_save = input("enter how many times to save 20 labels")#印出20個label的次數
timeinterval = 0.3
arr_saved = 20
array_hight = 10
first_end = timeinterval*array_hight 
for j in range(0, int(time_to_save)):
    for i in range(0, arr_saved):
        start = 0 + timeinterval * i
        end = first_end + timeinterval * i
        with open(file_name , 'a') as outfile:
            outfile.write('     #')
            outfile.write(str(round(start,1)))
            outfile.write('~')
            outfile.write(str(round(end,1)))
            
            outfile.write(' / matrix')
            outfile.write(str( i + 1))
            outfile.write('\n')

        