import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import tf

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "arm_with_torso"
move_group = moveit_commander.MoveGroupCommander(group_name)

# We can get the name of the reference frame for this robot:
planning_frame = move_group.get_planning_frame()
print "============ Planning frame: %s" % planning_frame

# We can also print the name of the end-effector link for this group:
eef_link = move_group.get_end_effector_link()
print "============ End effector link: %s" % eef_link

# # Set end effector
# move_group.set_end_effector_link('wrist_flex_link')

# We can also print the name of the end-effector link for this group:
eef_link = move_group.get_end_effector_link()
print "============ End effector link: %s" % eef_link

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print "============ Available Planning Groups:", robot.get_group_names()

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print "============ Printing robot state"
print robot.get_current_state()
print ""

pose_goal = geometry_msgs.msg.Pose()
target_q = tf.transformations.quaternion_from_euler(0.0, 3.14 / 2.0, 0.0)

print "target Quaternion = ", target_q[0], target_q[1], target_q[2], target_q[3]
pose_goal.orientation.x = target_q[0]
pose_goal.orientation.y = target_q[1]
pose_goal.orientation.z = target_q[2]
pose_goal.orientation.w = target_q[3]

# pose_goal.orientation.x = -0.30883
# pose_goal.orientation.y = 0.6097
# pose_goal.orientation.z = 0.32759
# pose_goal.orientation.w = 0.65236
pose_goal.position.x = 0.3
pose_goal.position.y = 0
pose_goal.position.z = 0.9

# mypose = move_group.get_current_pose().pose
# mypose.position.z += 1
move_group.set_pose_target(pose_goal)

# Maybe the robot planner didn't take it into account? Need to check move_group.launch
# Check https://github.com/ros-planning/moveit/pull/541 for detail problem due to 
# fetch_moveit_config/config/ompl_planner.yaml is modified
# Check if sampling in JointModelStateSpace is enforced for this group by user.
# This is done by setting 'enforce_joint_model_state_space' to 'true' for the desired group in ompl_planning.yaml.

# Some planning problems like orientation path constraints are represented in PoseModelStateSpace and sampled via IK.
# However consecutive IK solutions are not checked for proximity at the moment and sometimes happen to be flipped,
# leading to invalid trajectories. This workaround lets the user prevent this problem by forcing rejection sampling
# in JointModelStateSpace.

constraint = moveit_msgs.msg.Constraints()
constraint.name = "dewey grasp constraint"
orientation_constraint = moveit_msgs.msg.OrientationConstraint()
orientation_constraint.header.frame_id = "base_link"
orientation_constraint.link_name = "wrist_roll_link"
orientation_constraint.orientation = geometry_msgs.msg.Quaternion(target_q[0],target_q[1],target_q[2],target_q[3])
# It looks like it didn't took value < 0.1 into account need to investigate
# in to ompl source for more info
orientation_constraint.absolute_x_axis_tolerance = 0.1
orientation_constraint.absolute_y_axis_tolerance = 0.1
orientation_constraint.absolute_z_axis_tolerance = 0.1
orientation_constraint.weight = 1
constraint.orientation_constraints.append(orientation_constraint)
move_group.set_path_constraints(constraint)

move_group.set_start_state(move_group.get_current_state())

move_group.set_planning_time(15)
myplan = move_group.plan()

# myc = move_group.get_path_constraints()

move_group.execute(myplan)
# Calling `stop()` ensures that there is no residual movement
move_group.stop()
# It is always good to clear your targets after planning with poses.
# Note: there is no equivalent function for clear_joint_value_targets()
move_group.clear_pose_targets()