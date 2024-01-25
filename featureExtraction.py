import cv2
import numpy as np

# Load fingerprint image 
img = cv2.imread('fingerprint.jpg')

# Detect minutiae points using CV algorithm
minutiae = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
minutiae = cv2.adaptiveThreshold(minutiae,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,2)
minutiae = cv2.dilate(minutiae, None)
minutiae = cv2.erode(minutiae, None)
minutiae = cv2.findContours(minutiae, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Convert each minutiae point to binary  
binary_stream = []
for point in minutiae:
    x,y,w,h = point.reshape(4)
    theta = 0 # dummy orientation
    
    # Convert to binary
    x_bin = '{0:08b}'.format(x) 
    y_bin = '{0:08b}'.format(y)
    t_bin = '{0:08b}'.format(theta)
    
    # Append to stream  
    bin_str = x_bin + y_bin + t_bin
    binary_stream.append(bin_str)
    
# Concatenate final stream
minutiae_binary_stream = ''.join(binary_stream)