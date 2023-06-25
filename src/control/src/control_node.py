import rospy
from control.msg import Control
 
# Callds decode on all the items in the control message
def decode_control_msgs(control):
    rospy.loginfo(control)
    for i in range(len(control.keys)):
        decode_control_msg(control.keys[i], control.values[i])

# Decodes the the key to perform and action
def decode_control_msg(key:int, value: float):

    if(key == 0):
        connection_status(value)
    elif(key == 1):
        pass
    elif(key == 2):
        pass
    else:
        rospy.logwarn("No matching command for key: %s", key)
    
def connection_status(connected: int):
    if connected == 1:
        rospy.loginfo("Radio connected")
    else:
        rospy.logwarn("Radio disconnected")

if __name__ == '__main__':
    try:
        rospy.init_node("control_node", anonymous=True)
        rospy.loginfo("Started control node")
        rospy.Subscriber("control", Control, decode_control_msgs)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass