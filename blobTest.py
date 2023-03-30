# Standard imports
import cv2
import numpy as np;
 
# Read image
cap = cv2.VideoCapture(0)
params = cv2.SimpleBlobDetector_Params()
 
# Filter by Area.
params.filterByArea = True
params.minArea = 200
 
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.3
 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87
 
# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01

detector = cv2.SimpleBlobDetector_create(params)
while(True):
    frame = cap.read()
    im = cv2.cvtColor(frame[1], cv2.COLOR_BGR2GRAY)
    # im = frame[1]
    #im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)
    
    # Set up the detector with default parameters.
    if(cv2.waitKey(1)):
        
        # Detect blobs.
        keypoints = detector.detect(im)
        
        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow("era eu bro", im)
    if(cv2.waitKey(1)==27):
        break
cap.release()
cv2.destroyAllWindows()