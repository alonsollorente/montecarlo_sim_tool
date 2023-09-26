cmake_minimum_required(VERSION 3.5)
project(hector_gazebo_plugins VERSION 0.5.3)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp std_msgs std_srvs geographic_msgs geometry_msgs nav_msgs tf dynamic_reconfigure message_generation)
include_directories(include ${catkin_INCLUDE_DIRS})

## Find gazebo
if(POLICY CMP0054)
  cmake_policy(SET CMP0054 NEW)
endif()
find_package(gazebo REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GAZEBO_CXX_FLAGS}")
include_directories(${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})

## Find Boost
find_package(Boost REQUIRED COMPONENTS thread)
include_directories(${Boost_INCLUDE_DIRS})

#######################################
## Declare ROS messages and services ##
#######################################

## Generate messages in the 'msg' folder
# add_message_files(
#   FILES
# )

## Generate services in the 'srv' folder
add_service_files(DIRECTORY srv
  FILES
    SetBias.srv
    SetReferenceGeoPose.srv
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES geographic_msgs geometry_msgs
)

#add dynamic reconfigure api
generate_dynamic_reconfigure_options(
  cfg/SensorModel.cfg
  cfg/GNSS.cfg
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
    CATKIN_DEPENDS roscpp std_msgs geographic_msgs geometry_msgs nav_msgs tf message_runtime
    INCLUDE_DIRS include
    LIBRARIES
)

###########
## Build ##
###########


add_library(hector_gazebo_ros_imu_bis SHARED src/gazebo_ros_imu.cpp)
target_link_libraries(hector_gazebo_ros_imu_bis ${Boost_LIBRARIES} ${GAZEBO_LIBRARIES} ${catkin_LIBRARIES})
add_dependencies(hector_gazebo_ros_imu_bis ${PROJECT_NAME}_generate_messages_cpp ${PROJECT_NAME}_gencfg)

add_library(hector_gazebo_ros_gps_bis SHARED src/gazebo_ros_gps.cpp)
target_link_libraries(hector_gazebo_ros_gps_bis ${GAZEBO_LIBRARIES} ${catkin_LIBRARIES})
add_dependencies(hector_gazebo_ros_gps_bis ${PROJECT_NAME}_generate_messages_cpp ${PROJECT_NAME}_gencfg)


#############
## Install ##
#############

# all install targets should use catkin DESTINATION variables
# See http://ros.org/doc/api/catkin/html/adv_user_guide/variables.html

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  FILES_MATCHING PATTERN "*.h"
  PATTERN ".svn" EXCLUDE
)

install(TARGETS
  hector_gazebo_ros_imu_bis
  hector_gazebo_ros_gps_bis
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
)
