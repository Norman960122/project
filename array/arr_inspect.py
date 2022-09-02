import numpy as np
import cv2
import collections
new_data1 = np.loadtxt('y_train_short2.txt')  
print(new_data1.shape)
print(collections.Counter(new_data1))