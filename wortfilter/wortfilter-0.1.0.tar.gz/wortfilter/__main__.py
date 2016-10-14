from wortfilter import Application
import sys


def main() -> None:
    app = Application.get_instance()
    app.setupUncaughtExceptionHandler()
    sys.exit(app.run())

if __name__ == '__main__':
    main()
