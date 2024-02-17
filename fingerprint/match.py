import os
import cv2
import numpy as np
#import fingerprint_enhancer
kp1, kp2, kp = None, None, None

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fa2.BMP')
img = cv2.imread(image_path, 0)
#e1=fingerprint_enhancer.enhance_Fingerprint(img)

# img_path2 = os.path.join(script_dir, 'fing2.jpeg')
img_path2 = os.path.join(script_dir, 'fa1.BMP')
img2 = cv2.imread(img_path2, 0)
#e2=fingerprint_enhancer.enhance_Fingerprint(img2)
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors for the images
kp1, desc1 = sift.detectAndCompute(img, None)
kp2, desc2 = sift.detectAndCompute(img2, None)
print(type(kp1),type(desc2))

num_segments=4
kp_s1 = np.array_split(kp1, num_segments)
desc_s = np.array_split(desc1, num_segments)
kp_s2 = np.array_split(kp2, num_segments)
desc_s2 = np.array_split(desc2, num_segments)
print(kp_s1[1])
# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=10)
search_params = dict(checks=50)

# FLANN matcher
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(desc_s[3], desc_s2[3], k=2)

# Ratio test as per Lowe's paper
good_matches = []
for m, n in matches:
    if m.distance < 0.85 * n.distance:
        good_matches.append(m)

# Calculate the similarity score
score = len(good_matches) / max(len(kp_s1[2]), len(kp_s2[2])) * 100
print(score)
