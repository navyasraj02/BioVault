import cv2
import os
import fingerprint_enhancer
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fing2.jpeg')

# Load the TIFF image
img = cv2.imread(image_path)         #specify file path accordingly
sample=fingerprint_enhancer.enhance_Fingerprint(img)
# Check if the image is loaded successfully
if sample is None:
    print("Error: Could not read the image.")
else:
    
    

    # Apply a binary threshold
    ret, thresh = cv2.threshold(sample, 70, 255, cv2.THRESH_BINARY)

    # Display the binary image
    cv2.imshow('Binary Image', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()