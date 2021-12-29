# piQtDash

A highly customizable dashboard to show on TFT displays.
This project can be used to display your very own dashboard.
The dasboard is fully customizable with QML (QT5) which is loaded on runtime.
Connectors provide data to display or functions to control other stuff like home assistant.

Disclaimer: I use this to display and control room temperature and humidity on an shpi device.
My own dashboard.yaml is not included, because its highly customized to my own needs.

## Getting Started

### Installing

Clone this repository to the home directory of pi.
```
git clone https://github.com/cmayer0087/piQtDash.git /home/pi/piQtDash
```

Install all requirements.
```
pip3 install -r requirements.txt
```

and follow this guide 
```
https://wiki.qt.io/RaspberryPi2EGLFS
```
### Executing program
Set some required env variables and start main.py
```
export QT_QPA_PLATFORM=eglfs
export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/local/qt5pi/plugins/platforms
export LD_LIBRARY_PATH=/usr/local/qt5pi/lib
python3 main.py
```

You can also use the included piQtDash.service to auto start piQtDash

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