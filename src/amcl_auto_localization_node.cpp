#include "amcl_auto_localization.h"

void auto_localization_script(std::shared_ptr<ROSbotAutoLocalizer> service_client)
{   
    service_client->waitForNodeToActivate("amcl", 1s);
    service_client->waitForNodeToActivate("bt_navigator", 1s);

    service_client->emptyServiceHandle("reinitialize_global_localization", 5s);

    for(unsigned int i = 0; i < 50; i++){
        service_client->emptyServiceHandle("request_nomotion_update", 5s);
        rclcpp::sleep_for(330ms);
    }

    while(1){
        service_client->emptyServiceHandle("request_nomotion_update", 1s);
        rclcpp::sleep_for(1s);
    }
}


int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<ROSbotAutoLocalizer>();

    rclcpp::executors::SingleThreadedExecutor exe;
    exe.add_node(node);

    std::shared_future<void> script = std::async(
        std::launch::async,
        std::bind(auto_localization_script, node));
    exe.spin_until_future_complete(script);

    rclcpp::shutdown();
    return 0;
}