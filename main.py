# coding: utf-8
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QTextCursor

from ui.ui_beidou import Ui_MainWindow
from at_cmd import AT_Command


class Stream(QtCore.QObject):
    """Redirects console output to text widget."""
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

    def flush(self):
        pass
    #  def flush(self):
    #      sys.stdout.flush()


class MainWindows(QtWidgets.QMainWindow):

    """Qt MainWindows Class"""

    def __init__(self, parent=None):
        super(MainWindows, self).__init__(parent=parent)

        # setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Redirect print to logarea
        sys.stdout = Stream(newText=self.normalOutputWritten)

        print("[INFO] Initializing RDSS")
        self.at_command = AT_Command()
        if (not self.at_command.is_serial_ok()):
            QtWidgets.QMessageBox.warning(self, "警告", "RDSS模块错误!")
            sys.exit(-1)
        # hide auto update check box
        self.ui.auto_update_loc_checkBox.setVisible(False)
        # count down
        self.time_count = 60
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        # set LCD style
        self.ui.ic_wait.setStyleSheet("color: red;")

        # set connects
        self.init_events()
        # ---------- get all info of RDSS -------------
        self.at_command.send_cmd(self.at_command.CMD['at_mode'])
        self.at_command.send_cmd(self.at_command.CMD['get_id'])
        self.at_command.send_cmd(self.at_command.CMD['get_csq'])
        self.at_command.send_cmd(self.at_command.CMD['get_dst_addr'])

    def init_events(self):
        # buttons method
        self.ui.set_dst_btn.clicked.connect(self.set_dst_addr)
        self.ui.update_signal_btn.clicked.connect(self.update_csq)
        self.ui.update_loc_btn.clicked.connect(self.update_loc)
        self.ui.send_btn.clicked.connect(self.send_msg)
        # timer method
        self.timer.timeout.connect(self.timer_countdown)

    def timer_countdown(self):
        self.ui.ic_wait.display(self.time_count)
        if self.time_count != 0:
            self.time_count -= 1
        else:
            self.time_count = 60
            self.timer.stop()
            self.ui.send_btn.setEnabled(True)

    def set_dst_addr(self):
        dst = self.ui.dst_line.text()
        self.at_command.send_cmd(self.at_command.CMD['set_dst_addr']+dst.encode('utf-8')+b'\r\n')

    def update_csq(self):
        self.at_command.send_cmd(self.at_command.CMD['get_csq'])

    def update_loc(self):
        self.at_command.send_cmd(self.at_command.CMD['get_loc'])

    def send_msg(self):
        dst = self.ui.dst_line.text()
        msg = self.ui.send_message_line.text()
        self.at_command.send_cmd('AT+SEND={},"{}"\r\n'.format(dst, msg).encode("utf-8"))
        # CD 1 min
        self.ui.send_btn.setEnabled(False)
        self.timer.start()

    def get_info(self, text):
        """
        this function will get the received message from serial.
        And analyze the message by key word.
        """
        # get Local Addr
        if '$ZTXX' in text:
            text = text[text.find('$'):]
            loc = text.split(',')
            self.ui.date_line.setText(loc[2])
            self.ui.time_line.setText(loc[3])
            self.ui.longitude_line.setText(loc[4]+loc[5])
            self.ui.latitude_line.setText(loc[6]+loc[7])
            alt = loc[8][:loc[8].find('m')+1]
            self.ui.altitude_line.setText(alt)

        elif 'SRCAD:' in text:
            id = text[text.find(':')+1:]
            self.ui.addr_line.setText(id)
        elif 'CSQ:' in text:
            csq = text[text.find(':')+1:]
            self.ui.signal_line.setText(csq)
        elif 'DSTAD:' in text:
            msg = text[text.find(':')+1:-1]
            self.ui.dst_line.setText(msg)

    def normalOutputWritten(self, text):
        """Write console output to text widget."""
        cursor = self.ui.message_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        # process received message
        self.get_info(text)
        self.ui.message_area.setTextCursor(cursor)
        self.ui.message_area.ensureCursorVisible()

    #  def check_return_is_OK(self, message):
    #      if (len(message) == 0):
    #          print("[ERROR]: receive data len is 0")
    #      elif "ERROR" in message[0]:
    #          print("[ERROR]: serial error")
    #          print(self.at_command.err)
    #      else:
    #          return True
    #      QtWidgets.QMessageBox.warning(self, "警告", "[ERROR]: send cmd failure")
    #      sys.exit(-1)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindows()
    myapp.show()
    sys.exit(app.exec_())
