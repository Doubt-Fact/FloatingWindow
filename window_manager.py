from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

from floating_window import FloatingNoteWidget


class WindowManager(QObject):
    def __init__(self, app: QApplication, parent=None):
        super().__init__(parent)
        self._app = app
        self._windows: list[FloatingNoteWidget] = []
        self._offset = 0

    def create_window(self, file_path: str | None = None) -> FloatingNoteWidget:
        window = FloatingNoteWidget()
        window.closed.connect(lambda: self._remove_window(window))
        window.open_file_in_new_window.connect(self.create_window)

        self._offset += 30
        if self._offset > 150:
            self._offset = 30
        pos = window.pos()
        window.move(pos.x() + self._offset, pos.y() + self._offset)

        if file_path:
            window.load_file(file_path)

        window.show()
        self._windows.append(window)
        return window

    def _remove_window(self, window: FloatingNoteWidget):
        if window in self._windows:
            self._windows.remove(window)
        if not self._windows:
            self._app.quit()
