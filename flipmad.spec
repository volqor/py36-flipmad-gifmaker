# -*- mode: python ; coding: utf-8 -*-

import os
import glob
import cv2
import sys

block_cipher = None

# Obtén la ruta base de Python
python_base = sys.exec_prefix

cv2_path = cv2.__file__
cv2_libs = []
cv2_data_path = os.path.join(os.path.dirname(cv2.__file__), '*.so')
for lib in glob.glob(cv2_data_path):
    cv2_libs.append((lib, '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=cv2_libs,
    datas=[('web', 'web'), ('web/assets/images/logo.png', '.')],
    hiddenimports=['cv2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Intenta añadir el archivo opencv_videoio_ffmpeg.so si existe
ffmpeg_so = os.path.join(python_base, 'lib', 'python3.6', 'site-packages', 'cv2', 'opencv_videoio_ffmpeg.so')
if os.path.exists(ffmpeg_so):
    a.datas += [(os.path.basename(ffmpeg_so), ffmpeg_so, 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FGIFMaker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='web/assets/images/logo.png'
)