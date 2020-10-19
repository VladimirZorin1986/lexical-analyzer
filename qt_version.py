from PyQt5 import QtWidgets
from design import Ui_MainWindow
import sys
from app import lex_analysis


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.download_btn.clicked.connect(self.download)
        self.ui.get_lex.clicked.connect(self.analysis)

    def download(self):
        path = self.ui.pathfile.text()
        with open(path) as file:
            data = file.readlines()
        self.ui.listWidget.addItems(data)

    def analysis(self):
        lex_list = []
        for index in range(self.ui.listWidget.count()):
            for item_pair in lex_analysis(self.ui.listWidget.item(index).text()):
                lex_list.append(item_pair)
        self.ui.tableWidget.setRowCount(len(lex_list))
        row = 1
        for lexem, lexem_type in lex_list:
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(lexem))
            self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(lexem_type))
            row += 1


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()

sys.exit(app.exec())