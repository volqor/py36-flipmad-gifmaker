# 🎭 FlipMAD GIF Maker (Python 3.6.15)

Turn your images into fun GIFs with FlipMAD's unique animation, completely free! This software will help you do it easily thanks to its simple yet intuitive interface developed in Python =D

## 🛠️ Recommended Dependencies for Debian/Ubuntu (recommended but not necessary):

```bash
sudo apt-get install -y build-essential libgl1-mesa-glx libgl1-mesa-dev libglib2.0-dev libgtk2.0-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libjpeg-dev libpng-dev libatlas-base-dev gfortran qt5-default libqt5webkit5-dev
```

## 💻 Local Project Installation

Clone the repository:
```bash
git clone https://github.com/volqor/py36-flipmad-gifmaker
```
```bash
cd py36-flipmad-gifmaker/
```

Install Python dependencies:
```bash
python3 -m pip install --upgrade pip && pip3 cache purge && pip3 install -r DOCs/requirements.txt
```



## 📦 Building the Project

This project is set up for packaging using Pyinstaller in a Python virtual environment (venv) with Python 3.6.15 installed via PyENV on Ubuntu 22.04 (Linux 6.5.0-41-generic #41~22.04.2-Ubuntu SMP PREEMPT_DYNAMIC). The following instructions are based on this setup. If you're using a different system, you may need to make appropriate adjustments (or download the latest pre-compiled version to avoid these potentially tedious steps):

- Install Pyinstaller:
```bash
pip3 install pyinstaller
```

- Package the application using the pre-designed .SPEC file (refer to the file for more details):
```bash
pyinstaller --clean flipmad.spec
```

- Copy the WEB folder to the same directory as the generated binary:
```bash
cp -r web/ dist/
```

- Grant execution permissions to the generated binary:
```bash
cd dist/
```
```bash
sudo chmod +x FGIFMaker
```

Great! You've now successfully compiled the software. You can run it using:
```bash
./FGIFMaker
```




#### 👨‍💻 About the Developer

- [VOLQOR](https://www.bit.ly/volqor)
- [VOLQOR (on X/Twitter)](https://x.com/volqor)

Goodbye world!