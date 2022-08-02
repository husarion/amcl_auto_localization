FROM husarion/navigation2:galactic

SHELL ["/bin/bash", "-c"]

WORKDIR /ros2_ws

RUN apt update && apt install -y \
    git \
    python3-colcon-common-extensions 

COPY ./amcl_auto_localization /ros2_ws/src/amcl_auto_localization

RUN source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build

