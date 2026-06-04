import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():
    # Declare the launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('husky_description'))
    xacro_file = os.path.join(pkg_path,'urdf','husky.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file).toxml()
    # robot_description_config = Command(['xacro ', xacro_file])
    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Launch!
    # Note: joint_state_publisher is intentionally omitted here.
    # In Gazebo simulation, libgazebo_ros_joint_state_publisher (in gazebo.control.xacro)
    # publishes real joint positions and velocities from physics — joint_state_publisher
    # would override those with zeros, breaking wheel odometry and TF.

    # # Create a joint_state_publisher node for the wheels
    # node_joint_state_publisher = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     output='screen',
    #     parameters=[params]
    # )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        node_robot_state_publisher,
    ])