import rospy
import serial
from control.msg import Control
import json
 
# Publishes the control message from the radio serial output
def radio_publisher():
    rospy.init_node("nrf24l01_node", anonymous=True)
    rospy.loginfo("Starting nrf24l01")
    pub = rospy.Publisher('control', Control, queue_size=10)

    with serial.Serial('/dev/ttyACM0', 57600, timeout=1) as ser:
        while(not rospy.is_shutdown()):
            line: bytes = ser.readline()
            if line:
                try:
                    string: str = line.decode()
                    data: dict = json.loads(string)
                    control: Control = Control()
                    control.keys = list(map(int, data.keys()))
                    control.values = data.values()
                    pub.publish(control)
                except Exception as e:
                    rospy.logwarn("Unable to decode data radio data: " + str(e))

if __name__ == '__main__':
    try:
        radio_publisher()
    except rospy.ROSInterruptException:
        pass