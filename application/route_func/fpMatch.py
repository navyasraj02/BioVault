import cv2
import numpy as np
import msgpack
def fingerprint_segment(image1_path):
    kp1, kp2 = None, None

    # Load images
    img1 = cv2.imread(image1_path, 0)
    #img2 = cv2.imread(image2_path, 0)

    # Check image data type
    # print("Image 1 data type:", img1.dtype)
    #print("Image 2 data type:", img2.dtype)

    # Initialize SIFT detector
    sift = cv2.SIFT_create()
    
    # Detect keypoints and compute descriptors for the images
    kp1, desc1 = sift.detectAndCompute(img1, None)
    #kp2, desc2 = sift.detectAndCompute(img2, None)
    
    # print(type(kp1),type(desc1))
    num_segments=4
    kp_s1 = np.array_split(kp1, num_segments)
    desc_s = np.array_split(desc1, num_segments)
    #kp_s2 = np.array_split(kp2, num_segments)
    #desc_s2 = np.array_split(desc2, num_segments)

    # FLANN parameters
    return kp_s1,desc_s
def serializef(keypoint):
    skeypoint_1 = [msgpack.dumps({
        'pt': (kp.pt[0], kp.pt[1]),
        'size': kp.size,
        'angle': kp.angle,
        'response': kp.response,
        'octave': kp.octave,
        'class_id': kp.class_id
        }) for kp in keypoint]
    return skeypoint_1
def server(i):
    server_urls = [
    # "https://biovault-server0.onrender.com",
    "https://biovault-server1-p9ds.onrender.com",#working
    "https://biovault-server2.onrender.com",
    "https://biovault-server3.onrender.com",
    "https://biovault-server4.onrender.com",
    "https://biovault-server5.onrender.com",
    "https://biovault-server6.onrender.com",
    #"https://biovault-server7.onrender.com",
    # "https://biovault-server1.onrender.com"
    ]
    return server_urls[i-1]
