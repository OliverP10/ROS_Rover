import rospy
import serial
from control.msg import Control
import json
from socketio import Client
 
# Publishes the control message from the wifi socket
def socket_publisher():

    rospy.init_node("scoket_io_node", anonymous=True)
    rospy.loginfo("Starting scoket io")
    pub = rospy.Publisher('control', Control, queue_size=10)

    sio: Client = Client()
    load_callbacks(pub, sio)

    try:
        sio.connect('http://192.168.0.12:3000')
    except Exception as e:
        rospy.logerr("Unbale to connect to server: " + str(e))
    
# Loads the callbacks for the socket io
def load_callbacks(pub: rospy.Publisher, sio: Client):

    @sio.on('control-frame')
    def control_frame(data: json) -> None:
        try:
            control: Control = Control()
            control.keys = list(map(int, data.keys()))
            control.values = data.values()
            pub.publish(control)
        except Exception as e:
            rospy.logwarn("Unable to decode data scoket io data: " + str(e))

    @sio.event
    def connect() -> None:
        rospy.loginfo("WiFi connected")
        sio.emit("setType", "vehicle")

    @sio.event
    def disconnect() -> None:
        rospy.loginfo("WiFi disconnected")

if __name__ == '__main__':
    try:
        socket_publisher()
    except rospy.ROSInterruptException:
        pass