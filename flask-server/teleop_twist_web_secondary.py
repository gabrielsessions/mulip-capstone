#!/usr/bin/env python
import rclpy
from geometry_msgs.msg import Twist

# Define movement bindings based on button names instead of keyboard keys
moveBindings = {
    "f_fwd": (1.0, 0.0, 0.0, 0.0),
    "f_fwd": (1.0, 0.0, 0.0, 0.0),
    "f_bwd": (-1.0, 0.0, 0.0, 0.0),
    "s_bwd": (-0.5, 0.0, 0.0, 0.0),
    "f_rht": (1.0, 0.0, 0.0, -1.0),
    "s_rht": (0.0, 0.0, 0.0, -1.0),
    "f_lft": (1.0, 0.0, 0.0, 1.0),
    "s_lft": (0.0, 0.0, 0.0, 1.0),    
    "stop": (0.0, 0.0, 0.0, 0.0),
    "o": (0.0, 0.0, 1.0, 0.0),   # Lift up
    "p": (0.0, 0.0, -1.0, 0.0),  # Lift down
    "l": (0.0, 1.0, 0.0, 0.0),   # Head up
    ";": (0.0, -1.0, 0.0, 0.0)   # Head down
}

# Speed adjustment bindings
speedBindings = {
    "t": (1.1, 1.0, 1.0),  # Increase movement speed
    "y": (0.9, 1.0, 1.0),  # Decrease movement speed
    "g": (1.0, 1.1, 1.0),  # Increase lift speed
    "h": (1.0, 0.9, 1.0),  # Decrease lift speed
    "b": (1.0, 1.0, 1.1),  # Increase head speed
    "n": (1.0, 1.0, 0.9)   # Decrease head speed
}

class RobotController:
    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node('teleop_twist_web')
        self.pub = self.node.create_publisher(Twist, 'cmd_vel', 1)
        self.movement_speed = 0.2
        self.head_speed = 2.0
        self.lift_speed = 2.0

    def send_command(self, command):
        x, y, z, th = moveBindings.get(command, (0.0, 0.0, 0.0, 0.0))

        # Adjust speeds for twist message
        twist = Twist()
        twist.linear.x = x * self.movement_speed
        twist.linear.y = y * self.head_speed
        twist.linear.z = z * self.lift_speed
        twist.angular.z = th * self.movement_speed
        self.pub.publish(twist)

    def adjust_speed(self, command):
        if command in speedBindings:
            self.movement_speed *= speedBindings[command][0]
            self.head_speed *= speedBindings[command][1]
            self.lift_speed *= speedBindings[command][2]

    def stop_robot(self):
        self.pub.publish(Twist())  # Publish zero velocities to stop

    def close(self):
        rclpy.shutdown()

# Usage with web-based commands
controller = RobotController()

def handle_web_command(command):
    # If the command adjusts speed
    if command in speedBindings:
        controller.adjust_speed(command)
    else:
        controller.send_command(command)
    if command == "stop":
        controller.stop_robot()

try:
    # Replace with an appropriate loop or web callback to receive commands
    # For example, in a real web application, handle_web_command would be
    # connected to web socket messages or HTTP POST requests with command strings.
    pass  # Replace this pass with the actual communication mechanism
finally:
    controller.close()
