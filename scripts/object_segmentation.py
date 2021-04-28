import cv2
import numpy as np


img = cv2.imread('color_frame.jpeg')

# Displaying the image 
cv2.imshow("Image",img)

lower_blue = np.array([100,0,0])
upper_blue = np.array([150,10,10])
mask = cv2.inRange(img, lower_blue, upper_blue)

obj_seg = cv2.bitwise_and(img,img, mask=mask)

### Alternative way: Threshold the image after conerting to grayscale, 
### find contours, then find moments of the contours. 
### You need to make sure the object of interest is the largest contour

#obj_mono = cv2.cvtColor(obj_seg,cv2.COLOR_BGR2GRAY)
#ret, thresh = cv2.threshold(obj_mono, 10, 255, 0)
#contours= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#cnt = contours[0]

# M = cv2.moments(cnt)

# Find the moments of the image
M = cv2.moments(mask)
print M

if M['m00'] != 0:
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
else:
    cX, cY = 0, 0

print "Centroid, x: ", cX, "y: ", cY
print "Area: ", M['m00']

cv2.circle(obj_seg, (cX, cY), 5, (0, 0, 255), -1)

cv2.imshow("Result",obj_seg)

#waits for user to press any key 
cv2.waitKey(0) 

#closing all open windows 
cv2.destroyAllWindows()