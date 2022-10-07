import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

import mdm

#  def switch():


class mbmApp(QtWidgets.QMainWindow, mdm.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()


        self.setupUi(self)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = mbmApp()
    form.show()
    sys.exit(app.exec_())

