from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import sys
from PyQt5.QtGui import QPixmap
from main import *
import numpy as np

(Ui_MainWindow, QMainWindow) = uic.loadUiType('main.ui')


class MainWindow(QMainWindow):
    """MainWindow inherits QMainWindow"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        stylesheet = "::section{Background-color:rgb(102, 153, 255);}"
        self.ui.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        self.ui.tableWidget.verticalHeader().setStyleSheet(stylesheet)
        stylesheet = "::section{Background-color:rgb(102, 204, 204);}"
        self.ui.tableWidget_2.verticalHeader().setStyleSheet(stylesheet)
        self.ui.tableWidget_2.horizontalHeader().setStyleSheet(stylesheet)
        self.ui.tableWidget.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem('Начало ребра'))
        self.ui.tableWidget.setVerticalHeaderItem(1, QtWidgets.QTableWidgetItem('Конец ребра'))
        self.ui.tableWidget.setVerticalHeaderItem(2, QtWidgets.QTableWidgetItem('Пропускная способность'))
        self.ui.radioButton.clicked.connect(self.right_button_slot)
        self.ui.radioButton_2.clicked.connect(self.left_button_slot)
        self.ui.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_2.hide()

    def __del__(self):
        self.ui = None

    def right_button_slot(self):
        self.ui.pushButton.resize(631, self.ui.pushButton.height())
        self.ui.tableWidget_2.hide()
        self.ui.label_4.clear()
        self.ui.lineEdit.clear()

    def left_button_slot(self):
        self.ui.pushButton.resize(1042, self.ui.pushButton.height())
        self.ui.tableWidget_2.clear()
        self.ui.tableWidget_2.show()

    def slot1(self):
        if self.ui.radioButton.isChecked() or self.ui.radioButton_2.isChecked():
            graph_list = []
            for i in range(self.ui.tableWidget.columnCount()):
                if self.ui.tableWidget.item(0, i) is not None and \
                                self.ui.tableWidget.item(1, i) is not None and \
                                self.ui.tableWidget.item(2, i) is not None and \
                                self.ui.tableWidget.item(0, i).text() != '':
                    graph_list.append((self.ui.tableWidget.item(0, i).text(),
                                       self.ui.tableWidget.item(1, i).text(),
                                       self.ui.tableWidget.item(2, i).text()))
            if self.ui.radioButton.isChecked():
                self.ui.lineEdit.setText(str(max_flow(graph_list)))
                pixmap = QPixmap('graph.png')
                self.ui.label_4.setPixmap(pixmap)
            if self.ui.radioButton_2.isChecked():
                matr = floyd_alg(graph_list)
                for i in range(matr.shape[0]):
                    for j in range(matr.shape[1]):
                        if matr[i, j] != np.inf:
                            cell = QtWidgets.QTableWidgetItem()
                            cell.setText(str(int(matr[i, j])))
                            self.ui.tableWidget_2.setItem(i, j, cell)
            pixmap = QPixmap('start_graph.png')
            self.ui.label.setPixmap(pixmap)
            self.activateWindow()
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "Ошибка", "Выберите алгоритм", QMessageBox.NoButton, self)
            msg_box.addButton("&Continue", QMessageBox.RejectRole)
            msg_box.show()


# -----------------------------------------------------#
if __name__ == '__main__':
    # create application
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('max_flow')

    # create widget
    w = MainWindow()
    w.setWindowTitle('Максимальная пропускная способность')
    w.show()

    # execute application
    sys.exit(app.exec_())
