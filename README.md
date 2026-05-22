# 便利贴样式的悬浮窗 Floating Window with Sticky Note Style

## 支持的文件类型 Supported File Types

pdf（[PyMuPDF](https://github.com/pymupdf/PyMuPDF)）、txt

## 概述 Overview

轻量级桌面悬浮工具，类似便利贴，用于快速查看 PDF 和 TXT 文件。窗口可置顶、可拖动调整大小，支持多窗口管理。

A lightweight desktop floating tool, similar to sticky notes, for quickly viewing PDF and TXT files. The window can be set to stay on top, can be dragged and resized, and supports multi-window management.

## 技术栈 Tech Stack

| 组件 | 技术 |
|------|------|
| GUI 框架 | PySide6 |
| PDF 渲染 | PyMuPDF |

| Component | Technology |
|------|------|
| GUI Framework | PySide6 |
| PDF Rendering | PyMuPDF |

## 文件结构 File Structure

```
floatingwindow/
  main.py              # 应用入口 Application entry point
  resources.py         # 图标字体加载与渲染工具 Icon font loading and rendering utilities
  floating_window.py   # 悬浮窗口（无边框、标题栏、拖放） Floating window (borderless, custom title bar, drop file)
  pdf_viewer.py        # PDF 渲染与显示 PDF display
  txt_viewer.py        # TXT 文件显示 TXT file display
  window_manager.py    # 多窗口生命周期管理 Multi-window lifecycle management
  requirements.txt     # Python 依赖 Python dependencies
  public/icon/         # 图标字体资源 Icon font resources
```

## 快速开始 Quick Start

```bash
pip install -r requirements.txt
python main.py
```
