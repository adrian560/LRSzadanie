#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <mavros_msgs/msg/state.hpp>
#include <mavros_msgs/srv/command_bool.hpp>
#include <mavros_msgs/srv/set_mode.hpp>
#include <mavros_msgs/srv/command_tol.hpp>
#include <stdio.h>

using namespace std::chrono_literals;

class TemplateDroneControl : public rclcpp::Node
{
public:
    TemplateDroneControl() : Node("template_drone_control_node")
    {
        // Set up ROS publishers, subscribers and service clients
        state_sub_ = this->create_subscription<mavros_msgs::msg::State>(
            "mavros/state", 10, std::bind(&TemplateDroneControl::state_cb, this, std::placeholders::_1));
        local_pos_pub_ = this->create_publisher<geometry_msgs::msg::PoseStamped>("mavros/setpoint_position/local", 10);
        arming_client_ = this->create_client<mavros_msgs::srv::CommandBool>("mavros/cmd/arming");
        set_mode_client_ = this->create_client<mavros_msgs::srv::SetMode>("mavros/set_mode");
        takeoff_client_ = this->create_client<mavros_msgs::srv::CommandTOL>("mavros/cmd/takeoff");


/////////////////
        rmw_qos_profile_t custom_qos = rmw_qos_profile_default;
        custom_qos.depth = 1;
        custom_qos.reliability = RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT;
        auto qos = rclcpp::QoS(rclcpp::QoSInitialization(custom_qos.history, 1), custom_qos);
        local_pos_sub_ = this->create_subscription<geometry_msgs::msg::PoseStamped>(
                "/mavros/local_position/pose", qos, std::bind(&TemplateDroneControl::local_pos_cb, this, std::placeholders::_1));

        //geometry_msgs::msg::PoseStamped setpoint_to_send;
        //setpoint_to_send.pose.position.x = 1;
        //local_pos_pub_.publish(current_local_pos_);

//////////////////


        // Wait for MAVROS SITL connection
        while (rclcpp::ok() && !current_state_.connected)
        {
            rclcpp::spin_some(this->get_node_base_interface());
            std::this_thread::sleep_for(100ms);
        }
        mavros_msgs::srv::SetMode::Request guided_set_mode_req;
        guided_set_mode_req.custom_mode = "GUIDED";


        // mavros_msg::srv:CommandBool mavrosArmingMode;
        // mavrosArmingMode.mode = True;
 
        while (!set_mode_client_->wait_for_service(1s))
        {
            if (!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(), "Interrupted while waiting for the set_mode service. Exiting.");
                return;
            }
            RCLCPP_INFO(this->get_logger(), "Waiting for set_mode service...");
        }
        auto result = set_mode_client_->async_send_request(std::make_shared<mavros_msgs::srv::SetMode::Request>(guided_set_mode_req));

        // TODO: Test if drone state really changed to GUIDED
        
        if (current_state_.mode == "GUIDED")
        {
            RCLCPP_INFO(this->get_logger(), "funguje");;
        }       
        
        // TODO: Arm and Take Off\
        // Arm the drone
        mavros_msgs::srv::CommandBool::Request arm_request;
        arm_request.value = true;
        RCLCPP_INFO(this->get_logger(), "Drone armed successfully");

        // Take off
        mavros_msgs::srv::CommandTOL::Request takeoff_request;
        takeoff_request.altitude = 3.0; // Adjust the altitude as needed
        RCLCPP_INFO(this->get_logger(), "Drone took off successfully");

////////

        
        RCLCPP_INFO(this->get_logger(), "Sending position command");
        // tuna budes pisat arming 
        // auto resultArming = arming_-> async_send_request(std:make_thread<mavros_msg::srv::)

        // TODO: Implement position controller and mission commands here
    }

private:

    void publish(const geometry_msgs::msg::PoseStamped setpoint_to_send)
    {

        //setpoint_to_send.pose.position.x = 1;
        //RCLCPP_INFO(this->get_logger(), "Current State: %s", current_state_.mode.c_str());
    }

    void state_cb(const mavros_msgs::msg::State::SharedPtr msg)
    {
        current_state_ = *msg;
        RCLCPP_INFO(this->get_logger(), "Current State: %s", current_state_.mode.c_str());
    }


    void local_pos_cb(const geometry_msgs::msg::PoseStamped::SharedPtr msg)
    {
        geometry_msgs::msg::PoseStamped current_local_pos_ = *msg;

        // To obtain the position of the drone use this data fields withing the message, please note, that this is the local position of the drone in the NED frame so it is different to the map frame
        current_local_pos_.pose.position.x;
        current_local_pos_.pose.position.y;
        current_local_pos_.pose.position.z;
        // you can do the same for orientation, but you will not need it for this seminar


        RCLCPP_INFO(this->get_logger(), "Current Local Position: %f, %f, %f", current_local_pos_.pose.position.x, current_local_pos_.pose.position.y, current_local_pos_.pose.position.z);
    }


    rclcpp::Subscription<mavros_msgs::msg::State>::SharedPtr state_sub_;
    rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr local_pos_pub_;
    rclcpp::Client<mavros_msgs::srv::CommandBool>::SharedPtr arming_client_;
    rclcpp::Client<mavros_msgs::srv::SetMode>::SharedPtr set_mode_client_;
    rclcpp::Client<mavros_msgs::srv::CommandTOL>::SharedPtr takeoff_client_;

    rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr local_pos_sub_;

    mavros_msgs::msg::State current_state_;
};

/*
void nacitatMapu()
{
    FILE *pArq;
    pArq = fopen("/home/lrs-ubuntu/LRS/ros2_ws_group10/src/template_drone_control/maps/FEI_LRS_2D.pgm", "r");

    char line1[2], line2[100], line3[10];

    int cont = 1;
    while(1){
        if(cont ==1){ //version
            fscanf(pArq, "%s", &line1);
            if(feof(pArq)) break;

            printf("%s", line1);
        }

        if(cont ==2){ //comment
            fscanf(pArq, "%s", &line2);
            if(feof(pArq)) break;

            printf("%s", line2);
        }

        if(cont ==3){ //width, height
            fscanf(pArq, "%s", &line3);
            if(feof(pArq)) break;

            printf("%s", line3);
        }

        cont++;
    }
    fclose(pArq);
}
*/
int main(int argc, char **argv)
{
    //nacitatMapu();
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<TemplateDroneControl>());
    rclcpp::shutdown();
    return 0;
}
