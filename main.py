import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from resources import IconHelper
from window_manager import WindowManager


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    icon_path = Path(__file__).parent / "public" / "icon" / "iconfont.ttf"
    if not IconHelper.load_icons(str(icon_path)):
        print(f"Warning: Failed to load icon font from {icon_path}")

    manager = WindowManager(app)
    manager.create_window()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
