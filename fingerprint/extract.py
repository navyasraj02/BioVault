import fingerprint_feature_extractor
import cv2
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fing.jpeg')
img = cv2.imread(image_path, 0)				# read the input image --> You can enhance the fingerprint image using the "fingerprint_enhancer" library
FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage=False, showResult=True, saveResult=True)
print(type(FeaturesBifurcations))