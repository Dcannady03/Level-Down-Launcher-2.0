# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

# Collect data files and plugins
qt_plugins = collect_data_files('PyQt5', subdir='Qt5/plugins/platforms')  # Qt plugins
requests_data = collect_data_files('requests')  # Requests-related data
urllib3_data = collect_data_files('urllib3')  # urllib3-related data

# Define all data files to include
datas = [
    
    ('assets/images', 'assets/images'),  # Include images folder
    ('assets/styles', 'assets/styles'),  # Include styles folder
] + qt_plugins + requests_data + urllib3_data


# Hidden imports for PyInstaller
hiddenimports = [
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'requests',
    'urllib3',
    'chardet',
    'idna',
    'certifi',
    'unicodedata',
]

# Analysis block
a = Analysis(
    ['splash_screen.py'],  # Main script
    pathex=[],  # Custom path, if needed
    binaries=[],  # Additional binary files
    datas=datas,  # Data files
    hiddenimports=hiddenimports,  # Hidden imports
    hookspath=[],  # Additional hook paths
    hooksconfig={},
    runtime_hooks=[],  # Runtime hooks, if any
    excludes=[],  # Exclude specific libraries
    noarchive=False,
    optimize=0,
)

# Create the executable
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Level_Down_Launcher',
    debug=True,  # Enable debugging
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Enable console output for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.abspath("assets/images/test6.ico"),
    manifest="""
    <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
        <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
            <security>
                <requestedPrivileges>
                    <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
                </requestedPrivileges>
            </security>
        </trustInfo>
    </assembly>
    """
)
