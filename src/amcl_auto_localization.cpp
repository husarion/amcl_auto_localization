#include "amcl_auto_localization.h"


unsigned int ROSbotAutoLocalizer::waitForNodeToActivate(std::string lifecycle_node, std::chrono::seconds time_out)
{   
    std::string node_get_state_topic = lifecycle_node + "/get_state";
    
    this->client_get_state_ = this->create_client<lifecycle_msgs::srv::GetState>(
            node_get_state_topic);
            
    while(true){  
        auto request = std::make_shared<lifecycle_msgs::srv::GetState::Request>();

        if (!this->client_get_state_->wait_for_service(time_out)) {
        RCLCPP_ERROR(
            get_logger(),
            "Service %s is not available.",
            this->client_get_state_->get_service_name());
        return lifecycle_msgs::msg::State::PRIMARY_STATE_UNKNOWN;
        }

        auto future_result = client_get_state_->async_send_request(request);

        auto future_status = wait_for_result(future_result, time_out);

        if (future_status != std::future_status::ready) {
        RCLCPP_ERROR(
            get_logger(), "Server time out while getting current state for node %s", lifecycle_node.c_str());
        }

        if (future_result.get()) {
        RCLCPP_INFO(
            get_logger(), "Node %s has current state %s.",
            lifecycle_node.c_str(), future_result.get()->current_state.label.c_str());
            
            if(future_result.get()->current_state.id == 3){
                return future_result.get()->current_state.id;
            }
        } else {
        RCLCPP_ERROR(
            get_logger(), "Failed to get current state for node %s", lifecycle_node.c_str());
        return lifecycle_msgs::msg::State::PRIMARY_STATE_UNKNOWN;
        }

        rclcpp::sleep_for(2s);
    }
}


void ROSbotAutoLocalizer::emptyServiceHandle(std::string service_name, std::chrono::seconds time_out)
{
    rclcpp::Client<std_srvs::srv::Empty>::SharedPtr client =
    this->create_client<std_srvs::srv::Empty>(service_name);

    auto request = std::make_shared<std_srvs::srv::Empty::Request>();


    while (!client->wait_for_service(time_out)) {
        if (!rclcpp::ok()) {
            RCLCPP_ERROR(
                get_logger(), "Interrupted while waiting for the service. Exiting.");
            return;
        }
        RCLCPP_INFO(
            get_logger(), "service not available, waiting again....");
    }

    auto result = client->async_send_request(request);
}