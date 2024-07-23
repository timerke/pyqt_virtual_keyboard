from distutils.util import convert_path
from setuptools import find_packages, setup


data = {}
version_path = convert_path("version.py")
with open(version_path) as version_file:
    exec(version_file.read(), data)


setup(name="pyqt_virtual_keyboard",
      version=data["VERSION"],
      description="Virtual keyboard based on PyQt",
      url="https://github.com/timerke/pyqt_virtual_keyboard",
      packages=find_packages(),
      python_requires=">=3.6, <=3.9.13",
      install_requires=[
          "PyQt5>=5.8.2",
      ],
      package_data={"pyqt_virtual_keyboard": ["backspace.png",
                                              "keyboard.png",
                                              "keyboard_en.ui",
                                              "keyboard_ru.ui",
                                              "keyboarddialog.ui",
                                              "up-arrow.png",
                                              "up-arrow-black.png",
                                              "world.png"],
                    },
      )
