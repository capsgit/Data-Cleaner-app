__title__ = "Data Cleaning"
__version__ = "0.2.0"
__author__ = "capsgit"
__doc__ = """
The Application is desingned to clean an input CSV-file and return a new cleaned one
- configurable from Front-end
"""

from pathlib import Path
import subprocess
import sys


def main() -> None:
    """Launch the Streamlit application."""

    # ruta al archivo de la app
    app_path = Path("frontend/app.py")

    # ejecutar streamlit usando el python actual
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_path)],
        check=True,
    )

if __name__ == "__main__":
    main()