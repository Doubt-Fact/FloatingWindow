from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QSizePolicy, QStackedWidget, QFileDialog,
)
from PySide6.QtCore import Qt, Signal, QPoint, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QFont, QCursor

from resources import IconHelper

_EDGE_SIZE = 6


class TitleBarButton(QPushButton):
    def __init__(self, codepoint: str, size: int = 20, color: QColor = QColor(80, 80, 80)):
        super().__init__()
        self._codepoint = codepoint
        self._size = size
        self._color = color
        self._hover_color = QColor(40, 40, 40)
        self.setFixedSize(30, 30)
        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_icon()

    def _update_icon(self, color=None):
        c = color or self._color
        self.setIcon(IconHelper.icon_pixmap(self._codepoint, self._size, c))

    def set_icon(self, codepoint: str, color: QColor = None):
        self._codepoint = codepoint
        self._update_icon(color)

    def enterEvent(self, event):
        self._update_icon(self._hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._update_icon()
        super().leaveEvent(event)


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(34)
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 4, 0)
        layout.setSpacing(4)

        self._file_icon = QLabel()
        self._file_icon.setFixedSize(20, 20)
        self._file_icon.hide()
        layout.addWidget(self._file_icon)

        self._title_label = QLabel("New Note")
        self._title_label.setStyleSheet("color: #555; font-size: 12px;")
        self._title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(self._title_label)

        layout.addStretch()

        self._pinned = True
        self._pin_btn = TitleBarButton(IconHelper.ICON_PINNED, 18, QColor(70, 130, 220))
        self._pin_btn.setToolTip("Unpin from top")
        self._pin_btn.clicked.connect(self._toggle_pin)
        layout.addWidget(self._pin_btn)

        self._add_btn = TitleBarButton(IconHelper.ICON_ADD, 18)
        self._add_btn.setToolTip("New window")
        layout.addWidget(self._add_btn)

        self._close_btn = TitleBarButton(IconHelper.ICON_CLOSE, 18, QColor(180, 60, 60))
        self._close_btn._hover_color = QColor(220, 50, 50)
        self._close_btn.setToolTip("Close")
        layout.addWidget(self._close_btn)

    @property
    def add_button(self):
        return self._add_btn

    @property
    def close_button(self):
        return self._close_btn

    def set_title(self, text: str):
        self._title_label.setText(text)
        self._title_label.setToolTip(text)

    def set_file_icon(self, codepoint: str):
        self._file_icon.setPixmap(IconHelper.icon_pixmap(codepoint, 16, QColor(100, 100, 100)))
        self._file_icon.show()

    @property
    def is_pinned(self):
        return self._pinned

    def _toggle_pin(self):
        self._pinned = not self._pinned
        window = self.window()
        window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, self._pinned)
        window.show()
        if self._pinned:
            self._pin_btn.set_icon(IconHelper.ICON_PINNED, QColor(70, 130, 220))
            self._pin_btn.setToolTip("Unpin from top")
        else:
            self._pin_btn.set_icon(IconHelper.ICON_UNPINNED, QColor(160, 160, 160))
            self._pin_btn.setToolTip("Pin to top")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            delta = event.position().toPoint() - self._drag_pos
            self.window().move(self.window().pos() + delta)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(245, 245, 245))
        painter.setPen(QPen(QColor(220, 220, 220), 1))
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)
        painter.end()


class PlaceholderWidget(QWidget):
    file_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel()
        icon.setPixmap(IconHelper.icon_pixmap(IconHelper.ICON_PDF, 48, QColor(180, 180, 180)))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        hint = QLabel("Drop PDF / TXT file here")
        hint.setStyleSheet("color: #aaa; font-size: 14px;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

        browse_btn = QPushButton("Browse")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setStyleSheet("""
            QPushButton {
                background: #e0e0e0; border: none; border-radius: 4px;
                padding: 6px 20px; color: #555; font-size: 12px;
            }
            QPushButton:hover { background: #d0d0d0; }
        """)
        browse_btn.clicked.connect(self._browse)
        layout.addWidget(browse_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "",
            "Documents (*.pdf *.txt);;PDF (*.pdf);;Text (*.txt)"
        )
        if path:
            self.file_selected.emit(path)


class DropOverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 80))
        painter.setPen(QPen(QColor(100, 160, 255), 2, Qt.PenStyle.DashLine))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        m = 8
        painter.drawRoundedRect(m, m, self.width() - 2 * m, self.height() - 2 * m, 8, 8)
        font = QFont()
        font.setPixelSize(18)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Drop file here")
        painter.end()


class FloatingNoteWidget(QWidget):
    closed = Signal()
    open_file_in_new_window = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setMinimumSize(250, 200)
        self.resize(420, 520)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setStyleSheet("background: #fafafa;")

        self._content = None
        self._resize_edge = None
        self._resize_start_pos = None
        self._resize_start_geo = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._title_bar = CustomTitleBar(self)
        self._title_bar.close_button.clicked.connect(self.close)
        self._title_bar.add_button.clicked.connect(lambda: self.open_file_in_new_window.emit(None))
        main_layout.addWidget(self._title_bar)

        self._stack = QStackedWidget()
        main_layout.addWidget(self._stack)

        self._placeholder = PlaceholderWidget()
        self._placeholder.file_selected.connect(self._load_file)
        self._stack.addWidget(self._placeholder)

        self._drop_overlay = DropOverlayWidget(self)

    def _edge_at(self, pos: QPoint) -> str | None:
        r = self.rect()
        x, y = pos.x(), pos.y()
        on_left = x < _EDGE_SIZE
        on_right = x > r.width() - _EDGE_SIZE
        on_top = y < _EDGE_SIZE
        on_bottom = y > r.height() - _EDGE_SIZE
        if on_top and on_left:
            return "top_left"
        if on_top and on_right:
            return "top_right"
        if on_bottom and on_left:
            return "bottom_left"
        if on_bottom and on_right:
            return "bottom_right"
        if on_top:
            return "top"
        if on_bottom:
            return "bottom"
        if on_left:
            return "left"
        if on_right:
            return "right"
        return None

    _EDGE_CURSORS = {
        "top": Qt.CursorShape.SizeVerCursor,
        "bottom": Qt.CursorShape.SizeVerCursor,
        "left": Qt.CursorShape.SizeHorCursor,
        "right": Qt.CursorShape.SizeHorCursor,
        "top_left": Qt.CursorShape.SizeFDiagCursor,
        "top_right": Qt.CursorShape.SizeBDiagCursor,
        "bottom_left": Qt.CursorShape.SizeBDiagCursor,
        "bottom_right": Qt.CursorShape.SizeFDiagCursor,
    }

    def mouseMoveEvent(self, event):
        if self._resize_edge and self._resize_start_pos and self._resize_start_geo:
            self._do_resize(event.globalPosition().toPoint())
            return
        edge = self._edge_at(event.position().toPoint())
        if edge:
            self.setCursor(QCursor(self._EDGE_CURSORS[edge]))
        else:
            self.unsetCursor()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            edge = self._edge_at(event.position().toPoint())
            if edge:
                self._resize_edge = edge
                self._resize_start_pos = event.globalPosition().toPoint()
                self._resize_start_geo = self.geometry()

    def mouseReleaseEvent(self, event):
        self._resize_edge = None
        self._resize_start_pos = None
        self._resize_start_geo = None

    def _do_resize(self, global_pos: QPoint):
        delta = global_pos - self._resize_start_pos
        geo = self._resize_start_geo
        min_w, min_h = self.minimumWidth(), self.minimumHeight()

        left = geo.left()
        top = geo.top()
        right = geo.right()
        bottom = geo.bottom()

        edge = self._resize_edge
        if "right" in edge or edge == "right":
            right = geo.right() + delta.x()
        if "left" in edge or edge == "left":
            left = geo.left() + delta.x()
        if "bottom" in edge or edge == "bottom":
            bottom = geo.bottom() + delta.y()
        if "top" in edge or edge == "top":
            top = geo.top() + delta.y()

        w = right - left + 1
        h = bottom - top + 1
        if w < min_w:
            if "left" in edge or edge == "left":
                left = right - min_w + 1
            else:
                right = left + min_w - 1
        if h < min_h:
            if "top" in edge or edge == "top":
                top = bottom - min_h + 1
            else:
                bottom = top + min_h - 1

        self.setGeometry(left, top, right - left + 1, bottom - top + 1)

    def set_content(self, widget: QWidget):
        if self._content is not None:
            self._stack.removeWidget(self._content)
            self._content.deleteLater()
        self._content = widget
        self._stack.addWidget(widget)
        self._stack.setCurrentWidget(widget)
        QTimer.singleShot(0, self._scale_content)

    def _scale_content(self):
        if self._content and hasattr(self._content, "scale_to_width"):
            self._content.scale_to_width(self.width() - 12)

    @property
    def title_bar(self):
        return self._title_bar

    def _load_file(self, file_path: str):
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "pdf":
            from pdf_viewer import PdfViewerWidget
            viewer = PdfViewerWidget()
            if viewer.load_pdf(file_path):
                self.set_content(viewer)
                name = file_path.replace("\\", "/").rsplit("/", 1)[-1]
                self._title_bar.set_title(name)
                self._title_bar.set_file_icon(IconHelper.ICON_PDF)
        elif ext == "txt":
            from txt_viewer import TxtViewerWidget
            viewer = TxtViewerWidget()
            viewer.load_txt(file_path)
            self.set_content(viewer)
            name = file_path.replace("\\", "/").rsplit("/", 1)[-1]
            self._title_bar.set_title(name)
            self._title_bar.set_file_icon(IconHelper.ICON_PDF)

    def load_file(self, file_path: str):
        self._load_file(file_path)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._drop_overlay.setGeometry(
            0, self._title_bar.height(),
            self.width(), self.height() - self._title_bar.height()
        )
        self._scale_content()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                ext = url.toLocalFile().rsplit(".", 1)[-1].lower()
                if ext in ("pdf", "txt"):
                    event.acceptProposedAction()
                    self._drop_overlay.show()
                    return

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self._drop_overlay.hide()

    def dropEvent(self, event):
        self._drop_overlay.hide()
        if not event.mimeData().hasUrls():
            return
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            ext = path.rsplit(".", 1)[-1].lower()
            if ext in ("pdf", "txt"):
                files.append(path)
        if not files:
            return
        self._load_file(files[0])
        for path in files[1:]:
            self.open_file_in_new_window.emit(path)
