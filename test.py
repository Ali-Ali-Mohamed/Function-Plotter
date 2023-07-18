import pytest
from PyQt5.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMessageBox, QPushButton, QLineEdit
from matplotlib.backends.backend_template import FigureCanvas
from FunctionPlotter import InputWindow


@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    window = InputWindow()
    window.show()
    qtbot.addWidget(window)
    yield test_app
    test_app.quit()


@pytest.fixture
def window(app, qtbot):
    return app.activeWindow()


def test_invalid_input_message(window, qtbot):
    button = window.findChild(QPushButton, "submit_button")
    qtbot.mouseClick(button, Qt.LeftButton)
    msg_box = QMessageBox.warning
    assert msg_box.isVisible()
    assert msg_box.windowTitle() == "Incomplete Input"
    input_string = window.findChild(QLineEdit, "text_input_string")
    input_string.setText("2x")
    qtbot.mouseClick(button, Qt.LeftButton)
    assert msg_box.isVisible()
    assert msg_box.windowTitle() == "Invalid Input"


def test_plot_function(window, qtbot):
    input_string = window.findChild(QLineEdit, "text_input_string")
    input_int1 = window.findChild(QLineEdit, "text_input_int1")
    input_int2 = window.findChild(QLineEdit, "text_input_int2")
    button = window.findChild(QPushButton, "submit_button")
    input_string.setText("x**2")
    input_int1.setText("0")
    input_int2.setText("10")
    qtbot.mouseClick(button, Qt.LeftButton)

    canvas = window.findChild(FigureCanvas)
    assert canvas is not None
    assert canvas.isVisible()


if __name__ == "__main__":
    pytest.main()