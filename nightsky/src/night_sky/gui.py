import sys
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton

class MouseDrag(QMouseEvent):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("My Form")
        self.edit = QLineEdit("Write my name here..")
        self.button = QPushButton("Show Greetings")
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())