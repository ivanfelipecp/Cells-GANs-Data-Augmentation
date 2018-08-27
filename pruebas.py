import cv2
import numpy as np

a= np.eye(3)
print(a.shape)
b = a.reshape(1,3,3)
print (b.shape)


print(a)
print(b)