# coding: utf-8
import sys
from PyQt5 import QtWidgets

from ui.ui_beidou import Ui_MainWindow


class MainWindows(QtWidgets.QMainWindow):

    """Qt MainWindows Class"""
    ##
    def __init__(self, parent=None):
        super(MainWindows, self).__init__(parent=parent)

        # setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindows()
    myapp.show()
    sys.exit(app.exec_())
