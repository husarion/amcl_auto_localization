cmake_minimum_required(VERSION 3.5)
project(amcl_auto_localization)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(navigation2 REQUIRED)
find_package(std_srvs REQUIRED)
find_package(lifecycle_msgs REQUIRED)


include_directories(
  include
)

#################
## Executables ##
#################

set(dependencies
  rclcpp
  navigation2
  std_srvs
  lifecycle_msgs
)

add_executable(rosbot_auto_localizator src/amcl_auto_localization_node.cpp src/amcl_auto_localization.cpp)
target_link_libraries(rosbot_auto_localizator ${Boost_LIBRARIES})
ament_target_dependencies(rosbot_auto_localizator rclcpp navigation2 std_srvs lifecycle_msgs)


#############
## Install ##
#############

install(DIRECTORY include
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS rosbot_auto_localizator
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()