#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Imu
from rclpy.qos import QoSProfile,ReliabilityPolicy,HistoryPolicy
from transforms3d import euler

class controller(Node):
    def __init__(self):
        super().__init__("controller")
        self.get_logger().info("The controller is now running...")
        self.velocity_publisher = self.create_publisher(Float64MultiArray,'/velocity_controller/commands',10)
        self.position_publisher = self.create_publisher(Float64MultiArray,'/position_controller/commands',10)
        self.qos_profile = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,history=HistoryPolicy.KEEP_LAST,depth =10)
        self.imu_data_show = self.create_subscription(Imu,"imu_plugin/out",self.imu_callback,self.qos_profile)
        self.start_time = 0.0
        self.stop_time = 3200.0
        self.kp = 1.35
        
    def move_forward(self,pose:Imu):
        vel = Float64MultiArray()
        vel1 = Float64MultiArray()
        steering_input = Float64MultiArray()
        steering_input.data = [pose.angular_velocity.z,pose.angular_velocity.z,0.0,0.0]
        vel.data = [2.0,2.0,-2.0,-2.0]
        vel1.data = [0.0,0.0,0.0,0.0]
        if self.start_time < self.stop_time:
            self.velocity_publisher.publish(vel)
            self.position_publisher.publish(steering_input)
            self.get_logger().info(f"The steering angle is: {pose.angular_velocity.z}")
            self.start_time += 0.5
        else: 
            self.velocity_publisher.publish(vel1)       

    def control(self,values_for_error:Imu):
        current_values = values_for_error
        expected_values = Imu()
        error = Imu()
        no_steering_value = Imu()
        euler_convention = euler.quat2euler([current_values.orientation.x,current_values.orientation.y,current_values.orientation.z,current_values.orientation.w])
        self.get_logger().info(f"The yaw angle is:{euler_convention[0]}")
        expected_values.angular_velocity.z = -0.025
        no_steering_value.angular_velocity.z = 0.0
        error.angular_velocity.z = (expected_values.angular_velocity.z - current_values.angular_velocity.z)
        current_values.angular_velocity.z = (self.kp*error.angular_velocity.z)+0.02
        if current_values.orientation.x > -0.8238787 and current_values.orientation.x<-1.0238787:
            return no_steering_value
        else:
            return current_values



    def imu_callback(self,values:Imu):
        corrected_values = self.control(values)
        self.move_forward(corrected_values)

def main(args =None):
    rclpy.init(args=args)
    node = controller()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
