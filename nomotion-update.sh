# check docker flags!!
docker build -t amcl_auto_localization .
docker run --net=host --ipc host -e ROS_DOMAIN_ID=81 -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp amcl_auto_localization bash -c "source /opt/ros/\$ROS_DISTRO/setup.bash && \
source install/setup.bash && \
ros2 run amcl_auto_localization auto_localization_client"