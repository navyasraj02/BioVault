import cv2
import numpy as np
import os
from consistent import extract_consistent_region
'''def align_fingerprint(gray):
    # Convert image to grayscale
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Initialize ORB detector
    orb = cv2.SIFT_create()
    
    # Find keypoints and descriptors
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    
    # Select top keypoints based on response
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Filter good matches
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    # Calculate transformation matrix
    if len(good) > 4:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Align image
        aligned_image = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))

        # Adjust boundaries (if needed)
        # ...

        return aligned_image
    
    return aligned_image'''

def extract_consistent_region(gray):
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding to binarize the image
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 4)
    
    # Perform morphological operations to clean up the image
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)
    
    # Find contours in the image
    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    

    relevant_contours = []
    for contour in contours:
        # Compute contour area
        area = cv2.contourArea(contour)
        
        # Compute contour perimeter
        perimeter = cv2.arcLength(contour, True)
        
        # Compute compactness (ratio of perimeter^2 to area)
        compactness = (perimeter ** 2) / (4 * np.pi * area)
        
        # Compute bounding rectangle and aspect ratio
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        min_area_threshold=500
        max_compactness_threshold=15
        # Filter contours based on size, compactness, and aspect ratio
        if area > min_area_threshold and compactness < max_compactness_threshold and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
            relevant_contours.append(contour)
    # Select the largest contour as the consistent region
    

def extract_minutiae(consistent_region):
    # Implement minutiae extraction algorithm here
    minutiae_points = []  # Placeholder, replace with actual extraction code
    return minutiae_points

def select_horizontal_segment(consistent_region, minutiae_points):
    # Calculate horizontal projection of minutiae points
    projection = np.sum(consistent_region, axis=1)
    
    # Smooth the projection
    kernel_size = 15  # Adjust as needed
    smoothed_projection = cv2.GaussianBlur(projection.astype(np.float32), (kernel_size, kernel_size), 0)

    #smoothed_projection = cv2.GaussianBlur(projection, (kernel_size, kernel_size), 0)
    
    # Find peaks in the smoothed projection
    peaks = np.where((smoothed_projection[1:-1] > smoothed_projection[:-2]) & (smoothed_projection[1:-1] > smoothed_projection[2:]))[0] + 1
    
    # Select segment with the highest number of minutiae points
    segment_height = 100  # Adjust as needed
    max_segment = None
    max_minutiae_count = 0
    
    for peak in peaks:
        segment = consistent_region[peak-segment_height//2 : peak+segment_height//2, :]
        minutiae_count = len([pt for pt in minutiae_points if peak-segment_height//2 < pt[0] < peak+segment_height//2])
        if minutiae_count > max_minutiae_count:
            max_minutiae_count = minutiae_count
            max_segment = segment
    
    return max_segment

# Example usage
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fa1.BMP')
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image=cv2.resize(image,None,fx=2.5,fy=2.5)
#aligned_image = align_fingerprint(image)
consistent_region = extract_consistent_region(image)
#minutiae_points = extract_minutiae(consistent_region)
#horizontal_segment = select_horizontal_segment(consistent_region, minutiae_points)

# Display the results
#cv2.imshow('Aligned Fingerprint', aligned_image)
cv2.imshow('Consistent Region', consistent_region)
#cv2.imshow('Horizontal Segment', horizontal_segment)
cv2.waitKey(0)
cv2.destroyAllWindows()
