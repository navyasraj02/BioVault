import cv2
import os
import numpy as np
def thinning(image):
    # Apply Zhang-Suen thinning algorithm
    skeleton = np.zeros(image.shape, dtype=np.uint8)
    size = np.size(image)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    done = False

    while not done:
        eroded = cv2.erode(image, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(image, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        image = eroded.copy()

        zeros = size - cv2.countNonZero(image)
        if zeros == size:
            done = True

    return skeleton

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fing.jpeg')
sample=cv2.imread(image_path)
sample = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY) 
sample=thinning(sample)
if sample is None:
    print("image not selected")
else:
    print("loaded successfully")
    blocksize=8
    features=[]
    for x in range(0,sample.shape[1],blocksize):
        for y in range(0,sample.shape[0],blocksize):
            block = sample[y:y+blocksize, x:x+blocksize]
            mean = np.mean(block)  
            std_dev = np.std(block)
        
        # Histogram bins 
            hist, _ = np.histogram(block, bins=16)  
        
        # Append to vector
            block_vector = [mean, std_dev] + hist.tolist() 
            features.append(block_vector)
    features_array = np.array(features)
    ##print(features_array)
    sample=cv2.resize(sample,None,fx=.5,fy=.5)
    cv2.imshow("sample",sample)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
