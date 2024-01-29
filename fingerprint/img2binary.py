import cv2

# Load the TIFF image
img = cv2.imread('D:\\Major Project\\DB1_B\\104_7.tif')         #specify file path accordingly

# Check if the image is loaded successfully
if img is None:
    print("Error: Could not read the image.")
else:
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)

    # Display the binary image
    cv2.imshow('Binary Image', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()