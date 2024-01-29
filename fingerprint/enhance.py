import fingerprint_enhancer		
import fingerprint_feature_extractor						# Load the library
import cv2
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fing.jpeg')
img = cv2.imread(image_path, 0)		
sample = cv2.resize(img, None,fx=.5,fy=.5) 	
#cv2.imshow('sample',sample)
#cv2.waitKey(0)			# read input image
out = fingerprint_enhancer.enhance_Fingerprint(img)		# enhance the fingerprint image
cv2.imshow('enhanced_image', out);						# display the result
cv2.waitKey(0)											# hold the display window
FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(out, spuriousMinutiaeThresh=10, invertImage=False, showResult=True, saveResult=True)
print(type(FeaturesBifurcations))