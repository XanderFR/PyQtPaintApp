from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QStatusBar, QToolBar, QColorDialog, QFileDialog
from PyQt6.QtGui import QPixmap, QPainter, QPen, QAction
from PyQt6.QtCore import Qt, QPoint, QRect, QSize
import sys
import os


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pixmap = QPixmap(600, 600)
        self.pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self.pixmap)
        self.setMouseTracking(True)
        self.drawing = False
        self.lastMousePosition = QPoint()
        self.statusLabel = QLabel()

        self.eraser = False
        self.penColor = Qt.GlobalColor.black
        self.penWidth = 1

    def mouseMoveEvent(self, event):
        mousePosition = event.pos()
        statusText = f"Mouse Position: {mousePosition.x(), mousePosition.y()}"
        self.statusLabel.setText(statusText)
        self.parent.statusBar.addWidget(self.statusLabel)
        if (event.buttons() and Qt.MouseButton.LeftButton) and self.drawing:
            self.draw(mousePosition)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.lastMousePosition = event.pos()
            self.drawing = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def draw(self, points):
        painter = QPainter(self.pixmap)
        if self.eraser == False:
            pen = QPen(self.penColor, self.penWidth)
            painter.setPen(pen)
            painter.drawLine(self.lastMousePosition, points)
            self.lastMousePosition = points
        elif self.eraser == True:
            eraser = QRect(points.x(), points.y(), 12, 12)
            painter.eraseRect(eraser)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        targetRect = QRect()
        targetRect = event.rect()
        painter.drawPixmap(targetRect, self.pixmap, targetRect)
        painter.end()

    def selectTool(self, tool):
        if tool == "Pencil":
            self.penWidth = 2
            self.eraser = False
        elif tool == "Marker":
            self.penWidth = 4
            self.eraser = False
        elif tool == "Eraser":
            self.eraser = True
        elif tool == "Color":
            self.eraser = False
            color = QColorDialog.getColor()
            self.penColor = color

    def new(self):
        self.pixmap.fill(Qt.GlobalColor.white)
        self.update()

    def save(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", os.path.curdir+"newArt.png", "PNG File (*.png)")
        if fileName:
            self.pixmap.save(fileName, "png")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(600, 600)
        self.setWindowTitle("Paint App")

        # Creating a Canvas
        canvas = Canvas(self)
        self.setCentralWidget(canvas)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Creating Toolbar
        toolBar = QToolBar("Toolbar")
        toolBar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolBar)
        toolBar.setMovable(False)

        pencilAct = QAction("Pencil", toolBar)
        pencilAct.triggered.connect(lambda: canvas.selectTool("Pencil"))

        markerAct = QAction("Marker", toolBar)
        markerAct.triggered.connect(lambda: canvas.selectTool("Marker"))

        eraserAct = QAction("Eraser", toolBar)
        eraserAct.triggered.connect(lambda: canvas.selectTool("Eraser"))

        colorsAct = QAction("Colors", toolBar)
        colorsAct.triggered.connect(lambda: canvas.selectTool("Color"))

        toolBar.addAction(pencilAct)
        toolBar.addAction(markerAct)
        toolBar.addAction(eraserAct)
        toolBar.addAction(colorsAct)

        self.newAct = QAction("New")
        self.newAct.triggered.connect(canvas.new)

        self.saveFileAct = QAction("Save")
        self.saveFileAct.triggered.connect(canvas.save)

        self.exitAct = QAction("Exit")
        self.exitAct.triggered.connect(self.close)

        self.menuBar().setNativeMenuBar(False)

        fileMenu = self.menuBar().addMenu("File")
        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.saveFileAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
