# PiDash

With PiDash you can create a custom dashboard for your raspberry pi with a connected display.

## Getting Started

### Installing

Clone this repository to the home directory of pi.
```
git clone https://github.com/cmayer0087/pidash.git /home/pi/pidash
```

Install all requirements.
```
pip3 install -r requirements.txt
```

### Executing program
Set some required env variables and start main.py
```
export QT_QPA_PLATFORM=eglfs
export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/local/qt5pi/plugins/platforms
export LD_LIBRARY_PATH=/usr/local/qt5pi/lib
python3 main.py
```

You can also use the included pidash.service to auto start pidash

## Help

You should create the file dashboard.qml and config.yaml to create your dashboard. dashboard.qml is an QT5 QML file. For more informations read this [Help for QML](https://doc.qt.io/qt-5/qtqml-index.html)

TODO: How to configure connectors an which ones are available

## License

This project is licensed under the MIT License - see the [License.md](License.md) file for details

## Troubleshooting
### No text is displayed
Make shure the fonts folder in /usr/local/qt5pi/lib/ exisits
```
ln -s /usr/share/fonts/truetype/dejavu /usr/local/qt5pi/lib/fonts
```

## Acknowledgments

Inspiration, code snippets, etc.
* [dashzero](https://github.com/panbachi/dashzero)
* [QtMaterialDesignIcons](https://github.com/sthlm58/QtMaterialDesignIcons)