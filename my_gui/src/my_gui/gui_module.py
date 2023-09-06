import os
import rospy
import rospkg

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget 
from std_msgs.msg import String


class MyPlugin(Plugin):

    def __init__(self, context):
        super(MyPlugin, self).__init__(context)

        self.setObjectName('MyPlugin')

        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())

        if not args.quiet:
            pass

        self._widget = QWidget()
        ui_file = os.path.join(rospkg.RosPack().get_path('my_gui'), 'resource', 'MyPlugin.ui')
        loadUi(ui_file, self._widget)
        self._widget.setObjectName('MyPluginUi')
        self._widget.publishButton.clicked.connect(self.publishButtonCB)
        self._widget.rvizButton.clicked.connect(self.rvizButtonCB)
        self.pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.Subscriber("label", String, self.callback)

        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

    def publishButtonCB(self):
        rospy.loginfo("=====================================")
        rospy.loginfo("           Pubilshing data           ")
        rospy.loginfo("=====================================")
        msg = String()
        msg.data = "hello world"
        self.pub.publish(msg)

    def rvizButtonCB(self):
        os.system("gnome-terminal -e 'rviz'")
    
    def callback(self, data):
        self._widget.subLabel.setText(data.data)

