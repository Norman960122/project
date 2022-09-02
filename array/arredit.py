import numpy as np
import cv2

img_col = 5
img_row = 4
out_file_name = input("enter file name to write:")        
# file_name1 = input("enter file name1 to read:")        
# file_name2 = input("enter file name2 to read:")
# file_name3 = input("enter file name3 to read:")
# file_name4 = input("enter file name4 to read:")
# file_name5 = input("enter file name5 to read:")
# file_name6 = input("enter file name6 to read:")
# file_name7 = input("enter file name7 to read:")
new_data1 = np.loadtxt('x_train_short2.txt')   #------------------讀取檔案
new_data2 = np.loadtxt('left-sig-leftshort.txt')  
new_data3 = np.loadtxt('no-sig-leftshort.txt')  
# new_data4 = np.loadtxt('left-sig-stoptestshort.txt')  
# new_data5 = np.loadtxt('no-sig-lefttestshort.txt')  
# new_data6 = np.loadtxt('no-sig-righttestshort.txt')  
# new_data7 = np.loadtxt('right-sig-lefttestshort.txt')  
# new_data8 = np.loadtxt('right-sig-righttestshort.txt') 
# new_data9 = np.loadtxt('right-sig-stoptestshort.txt') 
# new_data10 = np.loadtxt('normaltestshort.txt') 
key = input("t for traing data, l for label data : ")

if key == 't':
    # datasum = np.concatenate((new_data1, new_data2, new_data3, new_data4, new_data5, new_data6, new_data7), axis = 0)#合併檔案
    datasum = np.concatenate((new_data1, new_data2, new_data3), axis = 0)#合併檔案
    print(datasum.shape)
    with open(out_file_name, 'w') as outfile:
        np.savetxt(outfile, datasum, delimiter=' ', newline='\n')#另存檔案
    reshaped_data = datasum.reshape(-1, img_col, img_row)
    print(reshaped_data.shape)

elif key == 'l':
    # datasum = np.concatenate((new_data1, new_data2, new_data3, new_data4, new_data5, new_data6, new_data7), axis = 0)
    datasum = np.concatenate((new_data1, new_data2, new_data3), axis = 0)#合併檔案
    print(datasum.shape)
    with open(out_file_name, 'w') as outfile:
        np.savetxt(outfile, datasum, delimiter=' ', newline='\n')








# vector, remain = np.split(new_data1,[1],axis = 1)
# print ('vector shape',vector.shape, '  remian shape', remain.shape)
# print(vector.max())
# vector = vector/vector.max()
# np.concatenate((vector, remain), axis = 1)
# print(vector.shape, vector.max())




# img = np.ones((100, 100, 3), dtype="uint8")#
# window_name = 'hello'
# cv2.imshow(window_name, img)
# key = cv2.waitKey(0) 