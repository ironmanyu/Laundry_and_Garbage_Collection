#! /usr/bin/python

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for processing and saving an image
import cv2
# Numpy to normalize depth image
import numpy as np
# Messages to save the pose estimation of the object


# Instantiate CvBridge
bridge = CvBridge()

def color_image_callback(msg):
    print("Received a color image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_color_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        # Save your OpenCV2 image as a jpeg 
        cv2.imwrite('color_frame.jpeg', cv2_color_img)

def depth_image_callback(msg):
    print("Received a depth image!")
    try:
        # The depth image is a single-channel float32 image
        # the values is the distance in m in z axis
        cv2_depth_img = bridge.imgmsg_to_cv2(msg, "32FC1")
    except CvBridgeError, e:
        print(e)
    else:
        depth_array = np.array(cv2_depth_img, dtype=np.float32)
        # Normalize the depth image to fall between 0 (black) and 1 (white)
        cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
        # At this point you can display the result properly:
        # cv2.imshow('Depth Image', depth_display_image)
        # If you write it as it si, the result will be a image with only 0 to 1 values.
        # To actually store in a this a image like the one we are showing its needed
        # to reescale the otuput to 255 gray scale.
        cv2.imwrite('depth_frame.jpeg',depth_array*255)

def main():
    rospy.init_node('frame_grabber')
    # Define your image topics
    color_topic = "/head_camera/rgb/image_raw"
    depth_topic = "/head_camera/depth_registered/image_raw"
    # Set up your color subscriber and define its callback
    rospy.Subscriber(color_topic, Image, color_image_callback)
    # Set up your depth subscriber and define its callback
    rospy.Subscriber(depth_topic, Image, depth_image_callback)
    # Spin until ctrl + c. You can also choose to spin once
    rospy.spin()

if __name__ == '__main__':
    main()