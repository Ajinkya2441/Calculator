from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QGridLayout, QPushButton, QVBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
import sys
import math

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Scientific Calculator")
        self.setGeometry(100, 100, 380, 500)
        self.equation = ""
        self.last_answer = ""

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 28px;
                padding: 10px;
                border: 2px solid #555;
                border-radius: 10px;
                background-color: #222;
                color: #eee;
            }
        """)
        self.layout.addWidget(self.display)

        # Buttons grid
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(10)

        buttons = [
            ('7', '8', '9', '/', 'C'),
            ('4', '5', '6', '*', '⌫'),
            ('1', '2', '3', '-', '('),
            ('0', '.', '=', '+', ')'),
            ('sin', 'cos', 'tan', 'log', 'ln'),
            ('√', '^', 'pi', 'e', 'Ans')
        ]

        self.buttons = {}

        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                button = QPushButton(btn_text)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setMinimumSize(60, 50)
                button.setStyleSheet(self.button_style())
                button.clicked.connect(self.on_button_clicked)
                buttons_layout.addWidget(button, row_idx, col_idx)
                self.buttons[btn_text] = button

        self.layout.addLayout(buttons_layout)
        self.setLayout(self.layout)

        # Set main window style
        self.setStyleSheet("background-color: #121212;")

    def button_style(self):
        return """
            QPushButton {
                font-size: 18px;
                color: #eee;
                background-color: #333;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #777;
            }
        """

    def on_button_clicked(self):
        sender = self.sender()
        text = sender.text()

        if text == 'C':
            self.equation = ""
            self.display.clear()
        elif text == '⌫':
            self.equation = self.equation[:-1]
            self.display.setText(self.equation)
        elif text == '=':
            self.calculate_result()
        elif text in ['sin', 'cos', 'tan', 'log', 'ln', '√', '^', 'pi', 'e', 'Ans']:
            self.handle_scientific(text)
        else:
            self.equation += text
            self.display.setText(self.equation)

    def calculate_result(self):
        try:
            expression = self.equation.replace('^', '**')
            expression = expression.replace('pi', str(math.pi))
            expression = expression.replace('e', str(math.e))
            expression = expression.replace('Ans', self.last_answer)
            # Safely evaluate with math functions allowed
            result = eval(expression, {"__builtins__": None}, math.__dict__)
            self.display.setText(str(result))
            self.equation = str(result)
            self.last_answer = str(result)
        except Exception:
            self.display.setText("Error")
            self.equation = ""

    def handle_scientific(self, func):
        try:
            if func == 'pi':
                self.equation += 'pi'
                self.display.setText(self.equation)
                return
            if func == 'e':
                self.equation += 'e'
                self.display.setText(self.equation)
                return
            if func == 'Ans':
                self.equation += self.last_answer
                self.display.setText(self.equation)
                return

            value = float(self.equation) if self.equation else 0

            if func == 'sin':
                res = math.sin(math.radians(value))
            elif func == 'cos':
                res = math.cos(math.radians(value))
            elif func == 'tan':
                res = math.tan(math.radians(value))
            elif func == 'log':
                res = math.log10(value)
            elif func == 'ln':
                res = math.log(value)
            elif func == '√':
                res = math.sqrt(value)
            elif func == '^':
                self.equation += '^'
                self.display.setText(self.equation)
                return
            else:
                res = "Unknown"

            self.display.setText(str(res))
            self.equation = str(res)
            self.last_answer = str(res)

        except Exception:
            self.display.setText("Error")
            self.equation = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
