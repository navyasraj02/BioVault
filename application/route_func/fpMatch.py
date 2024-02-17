import cv2
import numpy as np
def fingerprint_segment(image1_path):
    kp1, kp2 = None, None

    # Load images
    img1 = cv2.imread(image1_path, 0)
    #img2 = cv2.imread(image2_path, 0)

    # Check image data type
    # print("Image 1 data type:", img1.dtype)
    #print("Image 2 data type:", img2.dtype)

    # Initialize SIFT detector
    sift = cv2.SIFT_create()
    
    # Detect keypoints and compute descriptors for the images
    kp1, desc1 = sift.detectAndCompute(img1, None)
    #kp2, desc2 = sift.detectAndCompute(img2, None)
    
    # print(type(kp1),type(desc1))
    num_segments=4
    kp_s1 = np.array_split(kp1, num_segments)
    desc_s = np.array_split(desc1, num_segments)
    #kp_s2 = np.array_split(kp2, num_segments)
    #desc_s2 = np.array_split(desc2, num_segments)

    # FLANN parameters
    '''FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=10)
    search_params = dict(checks=50)
    
    # FLANN matcher
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc_s[2], desc_s2[2], k=2)
    
    # Ratio test as per Lowe's paper
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
    
    # Calculate the similarity score
    score = len(good_matches) / max(len(kp_s1[2]), len(kp_s2[2])) * 100'''
    return kp_s1,desc1
