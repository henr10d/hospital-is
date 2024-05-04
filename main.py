import sys
from PyQt5.QtWidgets import (QApplication)

from HospitalApp import HospitalApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HospitalApp()
    ex.show()
    # ex.showFullScreen()
    sys.exit(app.exec_())
