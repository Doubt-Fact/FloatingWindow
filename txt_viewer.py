from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QFont


class TxtViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        font = QFont("Microsoft YaHei", 10)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        self._text_edit.setFont(font)
        self._text_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self._text_edit.setStyleSheet("""
            QTextEdit {
                border: none; background: #fafafa; color: #333;
            }
        """)
        layout.addWidget(self._text_edit)

    def load_txt(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self._text_edit.setPlainText(f.read())
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="gbk") as f:
                self._text_edit.setPlainText(f.read())

    def scale_to_width(self, width: int):
        pass
