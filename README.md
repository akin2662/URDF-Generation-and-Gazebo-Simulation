# URDF-Generation-and-Gazebo-Simulation
**Note:** This project was a requirement for the course ENPM 662- Introduction to Robot Modeling at University of Maryland, College Park

## Project Description
The project involves designing a toy car in SolidWorks, exporting it as a URDF, and integrating it into ROS2 and Gazebo. The model includes LiDAR and IMU sensors, a teleoperation system, and a proportional controller to autonomously move the car from (0,0) to (10,10). Challenges like wheel misalignment, controller tuning, and sensor integration were addressed.

## Dependencies
* Python 3.11 (any version above 3 should work)
* Python running IDE (I've used VSCode)

## Libraries used
* The complete lists of the libraries used can be found in rally_car > packages.xml

## Instructions
1. Download the zip file and extract it
2. The assembly.zip contains the different parts of the the rally car
3. To run, you will first need to create a ROS2 workspace and build it.
   
   `mkdir -p ~/your_workspace/src`
   
   `cd ~/your_workspace/src`
   
5. Before building the workspace, you need to resolve package dependencies.

   `rosdep install -i --from-path src --rosdistro galactic -y
   
   **Note:** Make sure you are not in the src directory
7. Then run the following command (make sure you are still in your workspace)
   
   `colcon build`
   
10. After successfully building the workspace, you will see 4 directories: build install log src
11. Then go to the src folder and paste the 'rally_car' package, extracted from the zip file you downloaded
12. Then go back to a folder in your workspace and again build it:
    
      `colcon build`
   
14. Then run the following commands:
    
      `ros2 run rally_car proportional_controller.py`

      to run the controller

      `ros2 run rally_car error_values.py`

      to print the values of error in terminal

15. You can also control your car using teleop in a racing competition arena, to do this, use the commands given below:

      `ros2 launch package_name competition.launch.py`

       This would launch the arena

       `ros2 run rally_car rally_car_telop.py`

       This would run the teleop script and you would be able to control the car through the terminal
   
**Note**: a custom message Errorval and Controlval is used to get the error values and control values of the yaw angle in order to plot them. This is because, rqt_plot takes single values and not data of type arrays. The msg Errorval and Control val is published to /error/val and /control/val topics. Another node 'Error_values' is subscribed to these topics and prints the values (error only) to the terminal.

**Note**: It is assumed that you have ros2 already installed on your PC. I have done this project on  ROS2 Galactic Geoechelone


## How it works
* The program consists of a move forward method, a control method and an imu_callback
* The robots position is acquired through the imu call back through which the control and move forward methods are called.



