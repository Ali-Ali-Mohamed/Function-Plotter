import sys
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Plotter Application")
        self.setIcon()
        self.init_ui()
        self.pushButton()

    # This button is used by the user as a user manuel
    def pushButton(self):
        self.aboutButton = QPushButton("How to use the program", self)
        self.aboutButton.move(60, 345)
        font1 = QFont("Arial", 12)
        font1.setBold(True)
        self.aboutButton.setFont(font1)
        self.aboutButton.setFixedSize(200, 50)
        self.aboutButton.clicked.connect(self.aboutBox)

    # Show information about the program and how to use it to the user
    def aboutBox(self):
        QMessageBox.about(self.aboutButton, "How to use the program",
                          "First, enter the function you want to plot\nSecond, enter the minimum of the variable x\n"
                          "Third, enter the maximum of the variable x\nThen, click Plot button\n\nImportant Notes:\n"
                          "1-The function must has only one unknown variable (x)\n"
                          "2-The following operators are supported: + - / * ^\n"
                          "3-Minimum and Maximum must bs integers\n"
                          "4-Minimum must be smaller than Maximum\n"
                          "5-The function can't be in this format: 2x, instead let it be: 2*x\n"
                          "6-The function must contain at least one (x)")

    # Give the program an icon
    def setIcon(self):
        appIcon = QIcon("download.png")
        self.setWindowIcon(appIcon)

    # Implementing the user interface
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)

        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)

        # Take the function from the user
        self.label_string = QLabel("Enter The Function:")
        self.label_string.setFont(QFont("Arial", 16))
        self.text_input_string = QLineEdit()
        self.text_input_string.setFixedWidth(100)
        self.text_input_string.setFixedWidth(200)

        # Take the minimum value of x from the user
        self.label_int1 = QLabel("Enter The Minimum of x:")
        self.label_int1.setFont(QFont("Arial", 16))
        self.text_input_int1 = QLineEdit()
        self.text_input_int1.setFixedWidth(50)
        self.text_input_int1.setFixedWidth(100)

        # Take the maximum value of x from the user
        self.label_int2 = QLabel("Enter The Maximum of x:")
        self.label_int2.setFont(QFont("Arial", 16))
        self.text_input_int2 = QLineEdit()
        self.text_input_int2.setFixedWidth(50)
        self.text_input_int2.setFixedWidth(100)

        input_layout.addWidget(self.label_string)
        input_layout.addWidget(self.text_input_string)
        input_layout.addWidget(self.label_int1)
        input_layout.addWidget(self.text_input_int1)
        input_layout.addWidget(self.label_int2)
        input_layout.addWidget(self.text_input_int2)
        input_layout.addStretch()

        # Plot button
        button = QPushButton("Plot The Function")
        font = QFont("Arial", 12)
        font.setBold(True)
        button.setFont(font)
        button.setStyleSheet("color: red;")
        button.setFixedSize(200, 50)
        input_layout.addWidget(button)

        layout.addWidget(input_widget)

        self.setLayout(layout)
        button.clicked.connect(self.submit_input)
        self.resize(800, 400)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    # Handling if the user entered either X or x
    def replace_capital_x(self, s: str):
        new_string = ""
        for char in s:
            if char == 'X':
                new_string += 'x'
            else:
                new_string += char
        return new_string

    # Check the input fields before submit
    def submit_input(self):
        string_input = self.text_input_string.text()
        int1_input = self.text_input_int1.text()
        int2_input = self.text_input_int2.text()

        string_input = self.replace_capital_x(string_input)

        # Check that the user entered all required fields
        if string_input and int1_input and int2_input:
            try:
                int1 = int(int1_input)
                int2 = int(int2_input)
                # Check that the minimum is smaller than the maximum
                if not int2 > int1:
                    QMessageBox.warning(self, "Invalid Input",
                                        "Maximum of x must be greater than its minimum!")
            except ValueError:
                QMessageBox.warning(self, "Invalid Input",
                                    "Minimum and Maximum must be intergers!")
        else:
            QMessageBox.warning(self, "Incomplete Input",
                                "Please enter all fields!")

        # Check that the entered function is a valid function
        for i in string_input:
            if not i.isnumeric() and i != "x" and i != "+" and i != "-" and i != "/" and i != "*" and i != "^" and i != " ":
                QMessageBox.warning(self, "Invalid Input",
                                    "you can only use numbers, x, +, -, /, * and ^!\nerror was using '" + i + "' in the function input")
                break

        # Check that the entered function is a valid function
        for i in range(len(string_input) - 1):
            if string_input[i].isnumeric() and string_input[i+1] == 'x':
                QMessageBox.warning(self, "Invalid Input",
                                    "There must be and operation (+, -, /, *) between the number and x")
                break
            if string_input[i] == 'x' and string_input[i+1].isnumeric():
                QMessageBox.warning(self, "Invalid Input",
                                    "There must be and operation (+, -, /, *) between the number and x")
                break

        # Check that the entered function is a valid function
        if not string_input.__contains__('x'):
            QMessageBox.warning(self, "Invalid Input",
                                "There must be at least one x in the function input")

        # Replace any ^ in the user input by ** to give it to matplotlib
        string_input = string_input.replace("^", "**")

        x = np.linspace(int1, int2, 100)
        y = eval(string_input)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())