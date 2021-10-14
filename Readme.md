# PiDash

With PiDash you can create a custom dashboard for your raspberry pi with a connected display.

## Getting Started

### Installing

* clone this repository to your raspberry pi
* (optionl) It is recommended to use an virtual python environment
    ```
    python3 -m venv .venv
    ```
* install requirements
    ```
    pip install -r requirements.txt
    ```

### Executing program
Just run the main.py
```
python main.py
```

if you use a venv then you activate the environment before
```
. ./.venv/bin/activate
```

Or use the python in the virtual environment directly
```
./.venv/bin/python main.py
```

## Help

You should create the file dashboard.qml and config.yaml to create your dashboard. dashboard.qml is an QT5 QML file. For more informations read this [Help for QML](https://doc.qt.io/qt-5/qtqml-index.html)

TODO: How to configure connectors an which ones are available

## License

This project is licensed under the MIT License - see the [License.md](License.md) file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [dashzero](https://github.com/panbachi/dashzero)
* [QtMaterialDesignIcons](https://github.com/sthlm58/QtMaterialDesignIcons)