import fingerprint_feature_extractor
import cv2
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fing.jpeg')
img = cv2.imread(image_path, 0)				
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path2= os.path.join(script_dir, 'fing2.jpeg')
img2 = cv2.imread(image_path2, 0)	
FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage=False, showResult=False, saveResult=False)
#bf=cv2.BFMatcher()
#FeaturesTerminations2, FeaturesBifurcations2 = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage=False, showResult=False, saveResult=False)
#matches=bf.knnMatch(FeaturesTerminations,FeaturesTerminations2)

#goodmatch=[]
#for m,n in matches:
   # if m.distance<0.7 * n.distance:
 #       goodmatch.append(m)
#score = len(goodmatch) / max(len(FeaturesTerminations), len(FeaturesTerminations2)) * 100
#print(score)