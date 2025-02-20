#!/usr/bin/env python
import rclpy
from geometry_msgs.msg import Twist

class TeleopTwistWeb:
    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node(node_name='teleop_twist_web', namespace='cozmo')
        self.pub = self.node.create_publisher(Twist, 'cmd_vel', 1)
        self.movement_speed = 0.2
        self.head_speed = 2.0
        self.lift_speed = 2.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0

        # Mapping button names to movement directions
        self.moveBindings = {
            "f_fwd": (1.0, 0.0, 0.0, 0.0),   # Forward fast
            "s_fwd": (0.5, 0.0, 0.0, 0.0),   # Forward slow
            "f_bwd": (-1.0, 0.0, 0.0, 0.0),  # Backward fast
            "s_bwd": (-0.5, 0.0, 0.0, 0.0),  # Backward slow
            "f_lft": (0.0, 0.0, 0.0, 1.0),   # Turn left fast
            "s_lft": (0.0, 0.0, 0.0, 0.5),   # Turn left slow
            "f_rht": (0.0, 0.0, 0.0, -1.0),  # Turn right fast
            "s_rht": (0.0, 0.0, 0.0, -0.5),  # Turn right slow
            "stop": (0.0, 0.0, 0.0, 0.0)     # Stop
        }

    def send_command(self, command):
        # Check if command is in moveBindings
        if command in self.moveBindings:
            print(command, "in moveBindings")
            self.x, self.y, self.z, self.th = self.moveBindings[command]
        else:
            print(command, "not in moveBindings")
            self.x = self.y = self.z = self.th = 0.0
        
        twist = Twist()
        twist.linear.x = self.x * self.movement_speed
        twist.linear.y = self.y * self.head_speed
        twist.linear.z = self.z * self.lift_speed
        twist.angular.z = self.th * self.movement_speed

        self.pub.publish(twist)

    def shutdown(self):
        self.pub.publish(Twist())
        self.node.destroy_node()
        rclpy.shutdown()
