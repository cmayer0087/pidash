import sys
from core.App import App

if __name__ == "__main__":
    app = App(sys.argv)
    app.load()
    app.mainWindow.show()
    sys.exit(app.exec_())