import time

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from lifecycle_msgs.srv import GetState

from rclpy.qos import QoSDurabilityPolicy, QoSReliabilityPolicy, QoSHistoryPolicy
from rclpy.qos import QoSProfile


class AutoLocalizationClient(Node):
    def __init__(self):
        super().__init__("auto_localiztion_client")

        amcl_pose_qos = QoSProfile(
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.localization_pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            "amcl_pose",
            self._amclPoseCallback,
            amcl_pose_qos,
        )

        self.vel_publisher = self.create_publisher(Twist, "/cmd_vel", 10)

        self.reinitialize_global_localization_cli = self.create_client(
            Empty, "reinitialize_global_localization"
        )
        self.request_nomotion_update_cli = self.create_client(
            Empty, "request_nomotion_update"
        )

        self.req = Empty.Request()
        self.twist = Twist()
        self.twist.angular.z = 0.3

    def _amclPoseCallback(self, msg):
        self.get_logger().info(f"Received amcl pose \n{msg}")
        self.initial_pose_received = True
        return

    def send_reinitialize_request(self):
        self.future = self.reinitialize_global_localization_cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    def send_no_motion_update_request(self):
        self.future = self.request_nomotion_update_cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    def spin_robot(self):
        self.vel_publisher.publish(self.twist)
        rclpy.spin_once(self)
        return

    def waitUntilNav2Active(self):
        self._waitForNodeToActivate("amcl")

        while not self.reinitialize_global_localization_cli.wait_for_service(
            timeout_sec=1.0
        ):
            self.get_logger().info("service not available, waiting...")

        while not self.request_nomotion_update_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting...")

        self.get_logger().info("Nav2 is ready for use!")
        return

    def _waitForNodeToActivate(self, node_name):
        self.get_logger().warning("Waiting for " + node_name + " to become active..")

        node_service = node_name + "/get_state"
        state_client = self.create_client(GetState, node_service)

        while not state_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning(
                node_service + " service not available, waiting..."
            )

        req = GetState.Request()
        state = "unknown"
        while state != "active":
            future = state_client.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            if future.result() is not None:
                state = future.result().current_state.label
                self.get_logger().info("Result of get_state: %s" % state)
            time.sleep(2)
        return


def main(args=None):
    rclpy.init(args=args)

    no_motion_client = AutoLocalizationClient()

    no_motion_client.waitUntilNav2Active()
    no_motion_client.send_reinitialize_request()
    no_motion_client.spin_robot()

    for i in range(50):
        no_motion_client.send_no_motion_update_request()
        time.sleep(0.4)

    no_motion_client.get_logger().info(f"Done!")

    no_motion_client.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
