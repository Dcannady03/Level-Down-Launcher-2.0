# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

# Collect data files and plugins
qt_plugins = collect_data_files('PyQt5', subdir='Qt/plugins/platforms')
requests_data = collect_data_files('requests')
urllib3_data = collect_data_files('urllib3')

datas = [
    ('base_library.zip', '.'),  # Ensure base_library.zip is added to the root
    ('assets/images', 'assets/images'),
    ('assets/styles', 'assets/styles'),
]

hiddenimports = [
    'requests',
    'urllib3',
    'chardet',
    'idna',
    'certifi',
    'unicodedata'
]

a = Analysis(
    ['splash_screen.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Level_Down_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.abspath("assets/images/test6.ico"),
    # Add the requestedExecutionLevel for admin privileges
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
