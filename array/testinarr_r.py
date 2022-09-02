import numpy as np
file_name= input("enter file name to read:")
data_type= input("(test_data / lable_data)  (t/l):")
if data_type == 't':
    arr_hight = 10
    arr_width = 4
    new_data = np.loadtxt(file_name)
    print (new_data.shape)
    new_data = new_data.reshape((-1,arr_hight,arr_width))
    print (new_data.shape)

    # for i in range(0,new_data.shape[0]):
    #     print(new_data[i])
    #     print('\n')
elif data_type == 'l':
    new_data = np.loadtxt(file_name)
    print (new_data.shape)
 