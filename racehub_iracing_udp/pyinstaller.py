import PyInstaller.__main__
from pathlib import Path
from sys import platform

from racehub_iracing_udp.generate_version_file import generate_version_file

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "main.py")


def install():
    generate_version_file()

    PyInstaller.__main__.run(
        [
            path_to_main,
            "--onefile",
            "--console",
            "--name=RaceHub-iRacing-Server",
            "--icon=icon.ico" if platform == "win32" else "--icon=icon.icns",
        ]
    )
