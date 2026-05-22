from pathlib import Path

from PySide6.QtGui import QFontDatabase, QFont, QPainter, QPixmap, QColor
from PySide6.QtCore import Qt, QRect


class IconHelper:
    _font_id: int = -1
    _font_family: str = ""

    ICON_CLOSE = ""
    ICON_PINNED = ""
    ICON_UNPINNED = ""
    ICON_ADD = ""
    ICON_PDF = ""
    ICON_EYE_OFF = ""

    @classmethod
    def load_icons(cls, font_path: str) -> bool:
        cls._font_id = QFontDatabase.addApplicationFont(font_path)
        if cls._font_id == -1:
            return False
        families = QFontDatabase.applicationFontFamilies(cls._font_id)
        if not families:
            return False
        cls._font_family = families[0]
        return True

    @classmethod
    def icon_pixmap(cls, codepoint: str, size: int = 20,
                    color: QColor = QColor(80, 80, 80)) -> QPixmap:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        font = QFont(cls._font_family)
        font.setPixelSize(int(size * 0.85))
        painter.setFont(font)
        painter.setPen(color)
        painter.drawText(QRect(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, codepoint)
        painter.end()
        return pixmap
