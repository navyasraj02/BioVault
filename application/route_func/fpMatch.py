import cv2

def fingerprint_similarity(image1_path, image2_path):
    # Load images
    img1 = cv2.imread(image1_path, 0)
    img2 = cv2.imread(image2_path, 0)
    
    # Initialize SIFT detector
    sift = cv2.SIFT_create()
    
    # Detect keypoints and compute descriptors for the images
    kp1, desc1 = sift.detectAndCompute(img1, None)
    kp2, desc2 = sift.detectAndCompute(img2, None)
    
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=10)
    search_params = dict(checks=50)
    
    # FLANN matcher
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc1, desc2, k=2)
    
    # Ratio test as per Lowe's paper
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
    
    # Calculate the similarity score
    score = len(good_matches) / max(len(kp1), len(kp2)) * 100
    
    return score

# Example usage:
# similarity_score = fingerprint_similarity('fa1.BMP', 'fa2.BMP')
# print("Similarity Score:", similarity_score)
