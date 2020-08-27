"""
Cement Command Line Application for Think Stats 2e

Main application entry point:

    $ python app.py
"""
from cement_app.main import CementApp


if __name__ == "__main__":
    with CementApp() as app:
        app.run()
