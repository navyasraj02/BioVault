import cv2
import numpy as np

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
    min_area_threshold = 500
    max_compactness_threshold = 15
    min_aspect_ratio = 0.5
    max_aspect_ratio = 2.0
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
        
        # Filter contours based on size, compactness, and aspect ratio
        if area > min_area_threshold and compactness < max_compactness_threshold and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
            relevant_contours.append(contour)
    # Select the largest contour as the consistent region
    max_contour = max(contours, key=cv2.contourArea)
    
    # Create a mask for the consistent region
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [max_contour], -1, 255, -1)
    
    # Apply the mask to extract the consistent region
    consistent_region = cv2.bitwise_and(gray, mask)
    consistent_region = cv2.normalize(consistent_region, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    return consistent_region