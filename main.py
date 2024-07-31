import os
import sys
import cv2
import shutil
import subprocess
import numpy as np
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QCheckBox, QLabel, QFileDialog, QScrollArea, QGroupBox, QGridLayout, QSpacerItem, 
                             QSizePolicy, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings










VERSION = 'v1.0.0'
TAG_MESSAGE = f"By VOLQOR for Community ({VERSION})"










class FlipMADApp(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_r = os.path.join('web', 'assets', 'images', 'logo.png')
        
        self.setWindowTitle("FlipMAD GIF Maker")
        self.setWindowIcon(QtGui.QIcon(icon_r))
        self.setGeometry(100, 100, 1000, 600)
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(self.geometry().width(), self.geometry().height())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        self.web_view.load(QUrl.fromLocalFile(os.path.abspath(os.path.join('web', 'index.html'))))
        self.web_view.setFixedSize(320, 320)

        self.scroll_area.setWidget(self.web_view)
        self.scroll_area.setFixedSize(320, 320)
        main_layout.addWidget(self.scroll_area, 2)
        
        controls_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout, 1)

        # Grupo de botones de imagen
        image_group = QGroupBox("Image Controls")
        image_layout = QVBoxLayout()
        
        upload_button = self.create_styled_button("Upload Card Image", self.upload_image)
        image_layout.addWidget(upload_button)
        
        reset_button = self.create_styled_button("Reset WebView", self.reset_webview)
        image_layout.addWidget(reset_button)
        
        image_group.setLayout(image_layout)
        controls_layout.addWidget(image_group)

        # Grupo de botones de tamaño
        size_group = QGroupBox("Size Controls")
        size_layout = QGridLayout()
        sizes = [200, 400, 512, 600]
        self.size_buttons = []
        for i, size in enumerate(sizes):
            size_button = self.create_styled_button(f"{size}x{size}", lambda checked, s=size: self.change_size(s))
            self.size_buttons.append(size_button)
            size_layout.addWidget(size_button, i // 2, i % 2)
        size_group.setLayout(size_layout)
        controls_layout.addWidget(size_group)

        # Grupo de opciones
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        self.show_logo_checkbox = QCheckBox("Show Logo")
        self.show_logo_checkbox.setChecked(True)
        self.show_logo_checkbox.stateChanged.connect(self.toggle_logo)
        options_layout.addWidget(self.show_logo_checkbox)

        self.show_stores_checkbox = QCheckBox("Show Badges")
        self.show_stores_checkbox.setChecked(True)
        self.show_stores_checkbox.stateChanged.connect(self.toggle_stores)
        options_layout.addWidget(self.show_stores_checkbox)
        
        options_group.setLayout(options_layout)
        controls_layout.addWidget(options_group)

        # Grupo de botones de GIF
        gif_group = QGroupBox("GIF Controls")
        gif_layout = QVBoxLayout()
        
        self.create_gif_button = self.create_styled_button("Generate a New GIF", self.create_gif)
        gif_layout.addWidget(self.create_gif_button)
        
        gifs_folder_button = self.create_styled_button("Open GIFs Folder", self.open_gifs_folder)
        gif_layout.addWidget(gifs_folder_button)
        
        gif_group.setLayout(gif_layout)
        controls_layout.addWidget(gif_group)

        # Añadir TAG_MESSAGE en la esquina inferior derecha
        tag_label = QLabel(TAG_MESSAGE)
        tag_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        tag_label.setStyleSheet("color: #888888; font-size: 10px;")
        controls_layout.addWidget(tag_label)

        # Añadir espacio flexible al final
        controls_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_webview)
        self.timer.start(100)

        self.frame_capture_timer = QTimer(self)
        self.frame_capture_timer.timeout.connect(self.capture_frame)

        self.frames = []
        self.frame_count = 0
        self.total_frames = 100
        self.current_size = 320

    def create_styled_button(self, text, connection):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #367c39;
            }
        """)
        button.clicked.connect(connection)
        return button

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            js_code = f"document.getElementById('card-front').style.backgroundImage = 'url({file_name})'; document.getElementById('card-front').textContent = '';"
            self.web_view.page().runJavaScript(js_code)

    def change_size(self, size):
        js_code = f"changeSize({size});"
        self.web_view.page().runJavaScript(js_code)
        
        QTimer.singleShot(100, lambda: self.adjust_webview_size(size))
        
        # Actualizar el estilo de los botones de tamaño
        for button in self.size_buttons:
            if int(button.text().split('x')[0]) == size:
                button.setStyleSheet(button.styleSheet() + "background-color: #367c39;")
            else:
                button.setStyleSheet(button.styleSheet().replace("background-color: #367c39;", ""))
        
        self.current_size = size

    def adjust_webview_size(self, size):
        adjusted_size = size
        self.web_view.setFixedSize(adjusted_size, adjusted_size)
        self.scroll_area.setFixedSize(adjusted_size, adjusted_size)
    
    def toggle_logo(self):
        js_code = f"toggleLogo({str(self.show_logo_checkbox.isChecked()).lower()});"
        self.web_view.page().runJavaScript(js_code)

    def toggle_stores(self):
        js_code = f"toggleStores({str(self.show_stores_checkbox.isChecked()).lower()});"
        self.web_view.page().runJavaScript(js_code)

    def create_gif(self):
        self.create_gif_button.setEnabled(False)
        self.create_gif_button.setText("Waiting for animation...")
        self.frames = []
        self.frame_count = 0
        QTimer.singleShot(5000, self.start_frame_capture)

    def start_frame_capture(self):
        self.create_gif_button.setText("Generating frames...")
        self.frame_capture_timer.start(50)  # 20 fps

    def capture_frame(self):
        pixmap = self.web_view.grab()
        image = pixmap.toImage()
        
        size = image.size()
        s = image.bits().asstring(image.byteCount())
        
        channels = 4
        bytes_per_line = image.bytesPerLine()

        arr = np.frombuffer(s, dtype=np.uint8).reshape((size.height(), size.width(), channels))
        
        self.frames.append(arr)
        self.frame_count += 1

        if self.frame_count >= self.total_frames:
            self.frame_capture_timer.stop()
            self.save_frames_and_create_gif()

    def save_frames_and_create_gif(self):
        temp_r = os.path.join('temp', 'frames')
        if not os.path.exists(temp_r):
            os.makedirs(temp_r)

        for i, frame in enumerate(self.frames):
            val = os.path.join(temp_r, f"frame_{i+1:03d}.png")
            cv2.imwrite(val, frame)

        self.create_gif_from_frames()

    def create_gif_from_frames(self):
        gifs_save_r = os.path.join('GIFs')
        if not os.path.exists(gifs_save_r):
            os.makedirs(gifs_save_r)

        frames_r = os.path.join('temp', 'frames')
        temp_r = os.path.join('temp')
        
        gif_id = 1
        while os.path.exists(os.path.join(gifs_save_r, f"GIF_{gif_id:02d}.gif")):
            gif_id += 1

        gif_path = os.path.join(gifs_save_r, f"GIF_{gif_id:02d}.gif")

        frames = []
        for filename in sorted(os.listdir(frames_r)):
            if filename.endswith(".png"):
                frame_path = os.path.join(frames_r, filename)
                frames.append(Image.open(frame_path))

        frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=50, loop=0)

        shutil.rmtree(temp_r)

        self.create_gif_button.setEnabled(True)
        self.create_gif_button.setText("Create GIF")
        print(f"GIF created and saved as {gif_path}")

        # Mostrar ventana emergente con información del GIF
        self.show_gif_info(gif_path)

    def show_gif_info(self, gif_path):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("GIF Created Successfully")
        msg_box.setText(f"The GIF has been processed successfully.\n\nFile name: {os.path.basename(gif_path)}\nSaved at: {os.path.dirname(gif_path)}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def reset_webview(self):
        self.web_view.reload()
        self.show_logo_checkbox.setChecked(True)
        self.show_stores_checkbox.setChecked(True)
        self.change_size(320)

    def open_gifs_folder(self):
        gifs_folder = os.path.abspath(os.path.join('GIFs'))
        if not os.path.exists(gifs_folder):
            os.makedirs(gifs_folder)

        if sys.platform.startswith('win'):
            os.startfile(gifs_folder)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', gifs_folder])
        else:
            subprocess.Popen(['xdg-open', gifs_folder])

    def update_webview(self):
        self.web_view.page().runJavaScript("console.log('Updating...');")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FlipMADApp()
    window.show()
    sys.exit(app.exec_())
