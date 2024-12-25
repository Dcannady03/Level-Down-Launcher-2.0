from cx_Freeze import setup, Executable

executables = [
    Executable(
        script="splash_screen.py",
        base="Win32GUI",
        target_name="Level_Down_Launcher.exe",
        icon="assets/images/test6.ico"
    )
]

build_options = {
    "packages": ["os", "sys", "requests", "PyQt5"],
    "include_files": [
        ("assets", "assets"),
        "base_library.zip"
    ],
}

setup(
    name="Level Down Launcher",
    version="2.0",
    description="Level Down Launcher Application",
    options={"build_exe": build_options},
    executables=executables
)
