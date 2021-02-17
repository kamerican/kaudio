import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
        # self.setGeometry(100, 100, 200, 150)
        self.setWindowTitle('Window Example')
        self.resize(800, 600)
        
        btn_quit = QtWidgets.QPushButton('Force Quit', self)
        btn_quit.clicked.connect(QtWidgets.QApplication.instance().quit)
        btn_quit.resize(btn_quit.sizeHint())
        btn_quit.move(90, 100)
        
        
        self.show()
    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
    def closeEvent(self, event: QtGui.QCloseEvent):
        reply = QtWidgets.QMessageBox.question(
            self, 
            'Message', 
            'Are you sure you want to quit?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No,
        )

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()

    sys.exit(app.exec_())












import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

    # Greets the user
    def greetings(self):
        print(f"Hello {self.edit.text()}")

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())