# amcl_auto_localization

ROS Galactic demo showing how to use the `nomotion_update` service that is part of the `AMCL` algorithm implemented in `Navigation2` stack.

## How to use?

1. Run `localization` example from this [tutorial](https://github.com/husarion/rosbot-docker/tree/ros1/demo),
2. Update docker flags in `nomotion-upadte.sh` to match those in your [.env](https://github.com/husarion/rosbot-docker/tree/ros1/demo/.env.template) file, from `rosbot-docker/demo.env.template`,
3. Run `nomotion-upadte.sh` script:
    ```bash
    ./nomotion-upadte.sh
    ```

## Result:
The robot will begin to rotate `(!TODO add continuous rotation)` and, in successive iterations, should determine its position more and more accurately until the covariance is acceptably small `(!TODO add this condition - currently is a fixed number of iterations)`. 