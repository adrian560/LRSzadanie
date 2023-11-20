# LRSzadanie
# LRSzadanie



    Open terminator with LRS layout.
    In 1st terminal launch gazebo: gazebo <path_to_world>/fei_lrs_gazebo.world
    In 2nd terminal launch ArduPilot SITL:

    cd ardupilot/ArduCopter
    sim_vehicle.py -f gazebo-iris --console -l 48.15084570555732,17.072729745416016,150,0

    Launch mavros ros2 run mavros mavros_node --ros-args -p fcu_url:=udp://127.0.0.1:14551@14555


    Source your worskpace using source install/setup.bash
    Now you can run packages with the command ros2 run <package_1> <name_of_the_executable> in our case it can be ros2 run template_drone_control template_drone_control_node
   
    dokumentacia python sa nachadza v main branchy
