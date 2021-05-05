#!/usr/bin/env python
#
# Helper function for lab7 to combine generated trajectory points from curves
# found in a csv file, with the move_group_interface components to reach poses
# and to plan a trajectory based on waypoints.
# 
###########################################################


import numpy as np
import pandas as pd
from pick_and_place import PickAndPlace
import copy
from pyquaternion import Quaternion

repo = pd.read_csv('data.csv',sep=',',header=0)
data = np.array((repo['x'].values, repo['y'].values, repo['z'].values))
print "Number of data points: ", data.shape[1]
# data has 3 rows (x,y,z) and num_of_points number of columns
qStart = Quaternion(array=np.array([0.499, 0.5, 0.5,0.501]))
qEnd = Quaternion(array=np.array([0.022, 0.193, 0.894,0.405]))
qList = []
# Quickest (not most effective) way to get the items from the intermediates method since 
# its output is a generator of objects and has no easy way to get elements from it
for q in Quaternion.intermediates(qStart, qEnd, data.shape[1]-2, include_endpoints=True):
    # the method q.elements returns floats but does not guarantee normalization
    # so there could be the chance of errors based on the quaternions produced
    qList.append(q.elements)
# Instance of the pick and place class
example = PickAndPlace()
waypoints = []
# Using this to have the correct structure for pose without adding extra import msgs
current_pose = example.get_cartesian_pose()

for points in range(data.shape[1]):
    current_pose.position.x = data[0,points]
    current_pose.position.y = data[1,points]
    current_pose.position.z = data[2,points]
    # Notice the Quaternion class has a specific order: w, x, y, z
    current_pose.orientation.w = qList[points][0]
    current_pose.orientation.x = qList[points][1]
    current_pose.orientation.y = qList[points][2]
    current_pose.orientation.z = qList[points][3]
    waypoints.append(copy.deepcopy(current_pose))

cartesian_plan, fraction = example.plan_cartesian_path(waypoints)
example.execute_plan(cartesian_plan)


