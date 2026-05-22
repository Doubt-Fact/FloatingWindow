import pymupdf
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class PdfViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._doc = None
        self._original_pixmaps: list[QPixmap] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: #e8e8e8; }
        """)

        self._container = QWidget()
        self._page_layout = QVBoxLayout(self._container)
        self._page_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._page_layout.setSpacing(6)
        self._page_layout.setContentsMargins(6, 6, 6, 6)

        self._scroll_area.setWidget(self._container)
        layout.addWidget(self._scroll_area)

    def load_pdf(self, file_path: str) -> bool:
        try:
            self._doc = pymupdf.open(file_path)
        except Exception:
            return False

        self._original_pixmaps.clear()
        self._clear_pages()

        for i in range(len(self._doc)):
            page = self._doc[i]
            pix = page.get_pixmap(dpi=150, alpha=False)
            fmt = QImage.Format.Format_RGB888
            bpl = pix.width * 3
            qimg = QImage(bytes(pix.samples), pix.width, pix.height, bpl, fmt)
            qpixmap = QPixmap.fromImage(qimg.copy())
            self._original_pixmaps.append(qpixmap)

            label = QLabel()
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setPixmap(qpixmap)
            self._page_layout.addWidget(label)

        self.scale_to_width(max(self.width() - 20, 200))
        return True

    def scale_to_width(self, width: int):
        if width < 50 or not self._original_pixmaps:
            return
        first_w = self._original_pixmaps[0].width()
        if first_w <= width:
            for i in range(self._page_layout.count()):
                label = self._page_layout.itemAt(i).widget()
                if label and i < len(self._original_pixmaps):
                    label.setPixmap(self._original_pixmaps[i])
        else:
            for i in range(self._page_layout.count()):
                label = self._page_layout.itemAt(i).widget()
                if label and i < len(self._original_pixmaps):
                    scaled = self._original_pixmaps[i].scaledToWidth(
                        width, Qt.TransformationMode.SmoothTransformation
                    )
                    label.setPixmap(scaled)

    def _clear_pages(self):
        while self._page_layout.count():
            item = self._page_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
