cmake_minimum_required(VERSION 3.7.2)
<<<<<<< HEAD
project(robotics_labs)

find_package(catkin REQUIRED 
  COMPONENTS 
  roscpp 
  rospy 
  std_msgs 
  geometry_msgs
  shape_msgs
  visualization_msgs
  genmsg 
  simple_grasping
  pcl_conversions 
  pcl_ros
  interactive_markers
  moveit_core
  moveit_ros_planning
  moveit_ros_planning_interface
  moveit_ros_perception
  rviz_visual_tools
  moveit_visual_tools
  pluginlib
  geometric_shapes
  rosbag
  tf2_ros
  tf2_eigen
  tf2_geometry_msgs
  message_generation)

find_package(Eigen3 REQUIRED)
find_package(Boost REQUIRED system filesystem date_time thread)

# set(ApproxMVBB_DIR "/home/dewey/ApproxMVBB/Build/lib/cmake")
# find_package(ApproxMVBB REQUIRED )

include_directories(include ${catkin_INCLUDE_DIRS})

add_message_files(
  DIRECTORY
  msg
  FILES
  BoxTarget.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  visualization_msgs
)

# catkin_package()
catkin_package(CATKIN_DEPENDS message_runtime)

add_executable(segmentation src/segmentation.cpp)
target_link_libraries(segmentation ${catkin_LIBRARIES})
add_dependencies(segmentation ${catkin_EXPORTED_TARGETS})

add_executable(segment_door src/segment_door.cpp)
target_link_libraries(segment_door ${catkin_LIBRARIES})
add_dependencies(segment_door ${catkin_EXPORTED_TARGETS})

add_executable(segment_object src/segment_object.cpp)
target_link_libraries(segment_object ${catkin_LIBRARIES})
add_dependencies(segment_object ${catkin_EXPORTED_TARGETS})

add_executable(moveit_test src/moveit_test.cpp)
target_link_libraries(moveit_test ${catkin_LIBRARIES})
add_dependencies(moveit_test ${catkin_EXPORTED_TARGETS})

add_executable(motionplan src/motionplan.cpp)
target_link_libraries(motionplan ${catkin_LIBRARIES} ${Boost_LIBRARIES})
=======
project(Laundry_and_Garbage_Collection)

find_package(catkin)
catkin_package()
>>>>>>> e221825f4fec1f832483110c8063ca9898a185bb

install(
  PROGRAMS
    scripts/demo.py
<<<<<<< HEAD
=======
    scripts/pick_place_demo.py
    scripts/tests_arm_movements.py
>>>>>>> e221825f4fec1f832483110c8063ca9898a185bb
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(
<<<<<<< HEAD
  DIRECTORY launch maps config msg srv
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
=======
  DIRECTORY launch maps config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
>>>>>>> e221825f4fec1f832483110c8063ca9898a185bb
