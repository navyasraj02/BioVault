import os
import cv2
kp,kp1,kp2=None,None,None
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fing.jpeg')
img = cv2.imread(image_path, 0)		
img_path2=os.path.join(script_dir,'fing2.jpeg')
img2=cv2.imread(img_path2,0)
sift=cv2.SIFT_create()

kp1,desc=sift.detectAndCompute(img,None)
kp2,desc2=sift.detectAndCompute(img2,None)
matches=cv2.FlannBasedSegment({'algorithm':1,'trees':10},{}).knnMatch(desc,desc2,k=2)
matchpoints=[]

for p,q in matches:
    if p.distance <0.1 * q.distance:
        matchpoints.append(p)

kp=0

if len(kp1) < len(kp2):
    kp=len(kp1)
else:
    kp=len(kp2)

score=len(matchpoints)/kp *100
print(score)