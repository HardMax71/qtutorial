from PySide6.QtCore import Qt, QRect, QPoint, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout,
                               QFrame, QGraphicsOpacityEffect)

from .utils import load_stylesheet


class QTutorialHint(QFrame):
    def __init__(self, text, current_step, total_steps, show_step_number=True, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(load_stylesheet('styles:tutorial_hint.qss'))
        self.setFocusPolicy(Qt.StrongFocus)

        layout = QVBoxLayout(self)

        if show_step_number:
            self.progress_label = QLabel(f"Step {current_step + 1} of {total_steps}")
            self.progress_label.setAlignment(Qt.AlignCenter)
            self.progress_label.setObjectName("progress_label")
            layout.addWidget(self.progress_label)

        hint_text = QLabel(text)
        hint_text.setWordWrap(True)
        layout.addWidget(hint_text)

        button_layout = QHBoxLayout()
        self.next_button = QPushButton("Next")
        self.next_button.setFocusPolicy(Qt.NoFocus)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFocusPolicy(Qt.NoFocus)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        self.target_element = None

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(300)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(224, 224, 224))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def set_target_element(self, element):
        self.target_element = element
        self.update_position()

    def update_position(self):
        if self.target_element and self.parent():
            element_rect = self.target_element.geometry()
            element_global_rect = QRect(self.parent().mapToGlobal(element_rect.topLeft()), element_rect.size())

            screen_rect = QApplication.primaryScreen().availableGeometry()
            space_right = screen_rect.right() - element_global_rect.right()
            space_left = element_global_rect.left() - screen_rect.left()
            space_bottom = screen_rect.bottom() - element_global_rect.bottom()
            space_top = element_global_rect.top() - screen_rect.top()

            if space_right >= self.width() and space_bottom >= self.height():
                hint_pos = element_global_rect.topRight() + QPoint(10, 10)
            elif space_left >= self.width() and space_bottom >= self.height():
                hint_pos = element_global_rect.topLeft() + QPoint(-self.width() - 10, 10)
            elif space_right >= self.width() and space_top >= self.height():
                hint_pos = element_global_rect.bottomRight() + QPoint(10, -self.height() - 10)
            else:
                hint_pos = element_global_rect.bottomLeft() + QPoint(-self.width() - 10, -self.height() - 10)

            self.move(hint_pos)

    def show(self):
        super().show()
        self.opacity_animation.start()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right or event.key() == Qt.Key_Enter:
            self.next_button.click()
        elif event.key() == Qt.Key_Escape:
            self.stop_button.click()
