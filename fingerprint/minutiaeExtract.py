#path not given
import os
import cv2
import numpy as np
def extract_minutiae(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform image enhancement, ridge segmentation, and minutiae extraction (replace with your actual code)
    enhanced_image = cv2.equalizeHist(gray)
    _, binary_image = cv2.threshold(enhanced_image, 128, 255, cv2.THRESH_BINARY)
    
    # Assuming minutiae coordinates are stored in a variable named minutiae_points
    minutiae_points = [(x, y) for y in range(binary_image.shape[0]) for x in range(binary_image.shape[1]) if binary_image[y, x] == 255]

    return minutiae_points
def extract_minutiae_segments(image_path, num_segments=4):
    # Load fingerprint image
    fingerprint = cv2.imread(image_path)

    minu_points = extract_minutiae(fingerprint)
    
    minutiae_img = np.zeros(fingerprint.shape, np.uint8)

    # Draw each extracted (x, y) point
    for x, y in minu_points:
        cv2.circle(minutiae_img, (x, y), 1, 255, -1)

    # Display binary minutiae image
    cv2.imshow('Minutiae Points', minutiae_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Split into segments
    segments = np.array_split(minu_points, num_segments)

    # Return array of segments
    return list(map(list, segments))

# Example usage
image_path = 'fing.jpeg'
result_segments = extract_minutiae_segments(image_path)
print(result_segments)

