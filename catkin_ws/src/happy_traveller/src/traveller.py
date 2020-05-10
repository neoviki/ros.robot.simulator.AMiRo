import ros

import rospy
from geometry_msgs.msg import Twist

#topic='cmd_vel'

topic='/amiro1/cmd_vel'

PI=float(3.1415926)

wheel_diameter=2

def deg2rad(degrees):
    return float(degrees*(PI/180))


robot_drive_topic="/amiro1/cmd_vel"

robot_proximity_sensor_topic="/amiro1/proximity_ring/values"

rfid_tag_list_topic="/amiro1/rfid_tag_list"

def stop_robot(robot):
    twist = Twist()
    if not rospy.is_shutdown():
        print "DRIVE [ STOP ]"
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        robot.publish(twist)
    else:
        print "ros publisher thread is dead"


def turn_robot_left(robot, degree, angular_turn_rate):
    twist = Twist()
    if not rospy.is_shutdown():
        print "DRIVE [ LEFT ]"
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        #angular rate, How much degrees to turn per second
        turn_rate = deg2rad(angular_turn_rate)
        #How much degree to turn [total]
        angle_to_turn = deg2rad(degree)

        current_angle = 0
        twist.angular.z = abs(turn_rate)
        #Need this time for to calculate the amount of turn
        t0 = rospy.Time.now().to_sec()
        while current_angle < angle_to_turn:
            robot.publish(twist)
            t1 = rospy.Time.now().to_sec()
            current_angle = (t1-t0) * turn_rate
        stop_robot(robot)
    else:
        print "ros publisher thread is dead"

def turn_robot_right(robot, degree, angular_turn_rate):
    twist = Twist()
    if not rospy.is_shutdown():
        print "DRIVE [ RIGHT ]"
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = -0.25

        #angular rate, How much degrees to turn per second
        turn_rate = deg2rad(angular_turn_rate)
        #How much degree to turn [total]
        angle_to_turn = deg2rad(degree)

        current_angle = 0
        twist.angular.z = -abs(turn_rate)
        #Need this time for to calculate the amount of turn
        t0 = rospy.Time.now().to_sec()
        while current_angle < angle_to_turn:
            robot.publish(twist)
            t1 = rospy.Time.now().to_sec()
            current_angle = (t1-t0) * turn_rate
        stop_robot(robot)
    else:
        print "ros publisher thread is dead"


def move_robot_forward(robot, distance, speed):
    twist = Twist()
    if not rospy.is_shutdown():
        print "DRIVE [ FORWARD ]"
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0

        #How much centimeters per sec to move
        twist.linear.x = speed
        #Counter = 10 for 25 cm displacement
        #Counter = 16 for 54 cm displacement
        #Counter = 12 for 34 cm displacement
        #Counter = 14 for 44 cm displacement
        counter = distance  #Counter = 10 for 25 cm displacement
        while counter > 0:
            robot.publish(twist)
            rospy.sleep(0.2)
            counter = counter - 1

        stop_robot(robot)
    else:
        print "ros publisher thread is dead"


def move_robot_backward(robot):
    twist = Twist()
    if not rospy.is_shutdown():
        print "DRIVE [ FORWARD ]"
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0

        #How much centimeters per sec to move
        twist.linear.x = -0.2
        #Counter = 10 for 25 cm displacement
        #Counter = 16 for 54 cm displacement
        #Counter = 12 for 34 cm displacement
        #Counter = 14 for 44 cm displacement
        counter = 4  #Counter = 10 for 25 cm displacement
        while counter > 0:
            robot.publish(twist)
            rospy.sleep(0.2)
            counter = counter - 1

        stop_robot(robot)
    else:
        print "ros publisher thread is dead"


def main():
    print "ROBOT DRIVER"
    rospy.init_node('robot_driver', anonymous=True)
    rate = rospy.Rate(1)
    robot = rospy.Publisher(topic, Twist, queue_size=10)
    speed = float(0.8)
    distance= float(10.0)
    degrees= int(90)
    twist_rate=int(10)
    arena_height = 20
    arena_width = 20
    amiro_diameter = 2
    print "MOVE FWD"
    for i in range(arena_width/amiro_diameter):
        #Assuming Amiro Starts at (0,0) - South West Corner
        move_robot_forward(robot, arena_height, 0.1)
        turn_robot_right(robot, degrees, twist_rate)
        move_robot_forward(robot, amiro_diameter, 0.1)
        turn_robot_right(robot, degrees, twist_rate)
        rospy.sleep(1)
    #move_robot_forward(robot)
    #turn_robot_left(robot, degrees, twist_rate)
    #move_robot_forward(robot, distance, speed)
    #move_robot_backward(robot, distance, speed)
    #stop_robot(robot)

main()

