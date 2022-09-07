# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ast import Constant
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Twist
INF = 1000.0


class CollisionAvoidance(Node):
    min_dist = INF
    trig_dist = 1.0

    def __init__(self):
        super().__init__('ariadna_collision_avoidance')
        self.subscription = self.create_subscription(
            LaserScan, 'scan', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.colav)

    def listener_callback(self,msg):
        meas_min_dist = INF
        for range in msg.ranges:
            if range < meas_min_dist:
                meas_min_dist = range
            if meas_min_dist < self.min_dist:
                self.min_dist = meas_min_dist

        self.get_logger().info('I heard: "%.5f"' % meas_min_dist)\
    

    def set_vel_zero(self):
        linear=Vector3()
        linear.x=float(0)
        linear.y=float(0)
        linear.z=float(0)
        angular=Vector3()
        angular.x=float(0)
        angular.y=float(0)
        angular.z=float(0)
        msg = Twist()
        msg.linear=linear
        msg.angular=angular
        self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)

    def colav(self):
        if self.min_dist < self.trig_dist:
            self.set_vel_zero()
            self.get_logger().info('I started vel_zero()!')
            self.min_dist=INF


def main(args=None):
    rclpy.init(args=None)

    collision_avoidance = CollisionAvoidance()

    rclpy.spin(collision_avoidance)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    collision_avoidance.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

# To wysyłac na /cmd_vel
# linear:
#   x: 0.0
#   y: 0.0
#   z: 0.0
# angular:
#   x: 0.0
#   y: 0.0
#   z: 0.0
# ---
