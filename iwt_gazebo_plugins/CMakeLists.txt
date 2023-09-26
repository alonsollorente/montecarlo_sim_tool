cmake_minimum_required(VERSION 3.0.2)
project(iwt_gazebo_plugins)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  gazebo_dev
  gazebo_msgs
  sensor_msgs 
  gazebo_ros
  tf
  roscpp
  roscpp
  rospy
)

find_package(gazebo REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GAZEBO_CXX_FLAGS}")

include_directories(include
  ${Boost_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
)

link_directories(
  ${catkin_LIBRARY_DIRS}
  ${GAZEBO_LIBRARY_DIRS}
)

catkin_package(
  INCLUDE_DIRS include ${GAZEBO_INCLUDE_DIRS}
  LIBRARIES gazebo_ros_ouster_laser gazebo_ros_ouster_gpu_laser
  CATKIN_DEPENDS
    gazebo_msgs
    sensor_msgs 
    gazebo_ros
    roscpp
    rospy
)

if (UNIX)
  ## Plugins
  add_library(iwt_gazebo_planar_move src/gazebo_ros_planar_move.cpp)
  target_link_libraries(iwt_gazebo_planar_move ${catkin_LIBRARIES} ${Boost_LIBRARIES})

  add_library(gazebo_ros_ouster_laser src/GazeboRosOusterLaser.cpp)
  target_link_libraries(gazebo_ros_ouster_laser
    ${catkin_LIBRARIES}
    ${GAZEBO_LIBRARIES}
    RayPlugin
  )

  add_library(gazebo_ros_ouster_gpu_laser src/GazeboRosOusterLaser.cpp)
  target_link_libraries(gazebo_ros_ouster_gpu_laser
    ${catkin_LIBRARIES}
    ${GAZEBO_LIBRARIES}
    GpuRayPlugin
  )
  target_compile_definitions(gazebo_ros_ouster_gpu_laser PRIVATE GAZEBO_GPU_RAY=1)
  
  # VLP-16
  add_library(gazebo_ros_velodyne_laser src/GazeboRosVelodyneLaser.cpp)
  target_link_libraries(gazebo_ros_velodyne_laser
    ${catkin_LIBRARIES}
    ${GAZEBO_LIBRARIES}
    RayPlugin
  )

  
  add_library(gazebo_ros_velodyne_gpu_laser src/GazeboRosVelodyneLaser.cpp)
  target_link_libraries(gazebo_ros_velodyne_gpu_laser
    ${catkin_LIBRARIES}
    ${GAZEBO_LIBRARIES}
    GpuRayPlugin
  )
  target_compile_definitions(gazebo_ros_velodyne_gpu_laser  PRIVATE GAZEBO_GPU_RAY=1)
  # End VLP-16

  # # VLP-32
  # # No GPU
  # add_library(gazebo_ros_velodyne32_laser src/GazeboRosVelodyne32Laser.cpp)
  # target_link_libraries(gazebo_ros_velodyne32_laser
  #   ${catkin_LIBRARIES}
  #   ${GAZEBO_LIBRARIES}
  #   RayPlugin
  # )

  # # GPU
  # add_library(gazebo_ros_velodyne32_gpu_laser src/GazeboRosVelodyne32Laser.cpp)
  # target_link_libraries(gazebo_ros_velodyne32_gpu_laser
  #   ${catkin_LIBRARIES}
  #   ${GAZEBO_LIBRARIES}
  #   GpuRayPlugin
  # )
  # target_compile_definitions(gazebo_ros_velodyne32_gpu_laser  PRIVATE GAZEBO_GPU_RAY=1)
  # # End VLP-32

  install(TARGETS gazebo_ros_ouster_laser gazebo_ros_ouster_gpu_laser gazebo_ros_velodyne_laser gazebo_ros_velodyne_gpu_laser
          LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  )

  install(DIRECTORY include/${PROJECT_NAME}/
          DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  )


    
endif (UNIX)