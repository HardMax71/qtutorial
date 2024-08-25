import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                               QLineEdit, QVBoxLayout, QWidget, QHBoxLayout,
                               QCheckBox, QComboBox,
                               QRadioButton)

from qtutorial import load_stylesheet, QTutorialManager


# Example of a simple application with a tutorial
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Example with Tutorial")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(load_stylesheet('start_style.qss'))

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Left side layout
        left_vbox = QVBoxLayout()
        self.label1 = QLabel("Left Label")
        self.text_box1 = QLineEdit()
        self.text_box1.setPlaceholderText("Enter text for left label...")
        self.button1 = QPushButton("Update Left Label")
        self.button1.clicked.connect(self.update_left_label)
        self.checkbox1 = QCheckBox("Option 1")

        left_vbox.addWidget(self.label1)
        left_vbox.addWidget(self.text_box1)
        left_vbox.addWidget(self.button1)
        left_vbox.addWidget(self.checkbox1)
        left_vbox.addStretch()

        # Middle layout
        middle_vbox = QVBoxLayout()
        self.label3 = QLabel("Choose an option")
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option A", "Option B", "Option C"])
        self.radio_button1 = QRadioButton("Radio Button 1")
        self.radio_button2 = QRadioButton("Radio Button 2")
        self.middle_button = QPushButton("Middle Action")

        middle_vbox.addWidget(self.label3)
        middle_vbox.addWidget(self.combo_box)
        middle_vbox.addWidget(self.radio_button1)
        middle_vbox.addWidget(self.radio_button2)
        middle_vbox.addWidget(self.middle_button)
        middle_vbox.addStretch()

        # Right side layout
        right_vbox = QVBoxLayout()
        self.label2 = QLabel("Right Label")
        self.text_box2 = QLineEdit()
        self.text_box2.setPlaceholderText("Enter text for right label...")
        self.button2 = QPushButton("Update Right Label")
        self.button2.clicked.connect(self.update_right_label)
        self.checkbox2 = QCheckBox("Option 2")

        right_vbox.addWidget(self.label2)
        right_vbox.addWidget(self.text_box2)
        right_vbox.addWidget(self.button2)
        right_vbox.addWidget(self.checkbox2)
        right_vbox.addStretch()

        main_layout.addLayout(left_vbox)
        main_layout.addLayout(middle_vbox)
        main_layout.addLayout(right_vbox)

        self.setCentralWidget(central_widget)

        tutorial_steps = [
            (self.label1, "This is the left label that displays text."),
            (self.text_box1, "Enter text here to update the left label."),
            (self.button1, "Click this button to update the left label."),
            (self.checkbox1, "Toggle this checkbox for additional options."),
            (self.label3, "This label prompts you to choose an option."),
            (self.combo_box, "Select an option from this dropdown menu."),
            (self.radio_button1, "This is the first radio button."),
            (self.radio_button2, "This is the second radio button."),
            (self.middle_button, "Click this button to perform a middle action."),
            (self.label2, "This is the right label that displays text."),
            (self.text_box2, "Enter text here to update the right label."),
            (self.button2, "Click this button to update the right label."),
            (self.checkbox2, "Toggle this checkbox for options on the right.")
        ]

        self.tutorial_manager = QTutorialManager(self, tutorial_steps, show_step_number=True)
        self.tutorial_manager.start_tutorial()

    def update_left_label(self):
        self.label1.setText(f"Left: {self.text_box1.text()}")

    def update_right_label(self):
        self.label2.setText(f"Right: {self.text_box2.text()}")

    def moveEvent(self, event):
        super().moveEvent(event)
        self.tutorial_manager.update_hint_position()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.tutorial_manager.update_hint_position()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
