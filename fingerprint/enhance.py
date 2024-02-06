import fingerprint_enhancer		
import fingerprint_feature_extractor
from sklearn.metrics import jaccard_score						
import cv2
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fing.jpeg')
img = cv2.imread(image_path, 0)		
img_path2=os.path.join(script_dir,'fing2.jpeg')
img2=cv2.imread(img_path2,0)
#sample = cv2.resize(img, None,fx=.5,fy=.5) 	
#cv2.imshow('sample',sample)
#cv2.waitKey(0)			# read input image
out = fingerprint_enhancer.enhance_Fingerprint(img)	
out2=fingerprint_enhancer.enhance_Fingerprint(img2)	
#cv2.imshow('enhanced_image', out);						
#cv2.waitKey(0)											
FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(out, spuriousMinutiaeThresh=10, invertImage=False, showResult=False, saveResult=False)
#print(FeaturesBifurcations)

FeaturesTerminations2, FeaturesBifurcations2 = fingerprint_feature_extractor.extract_minutiae_features(out2, spuriousMinutiaeThresh=10, invertImage=False, showResult=False, saveResult=False)

