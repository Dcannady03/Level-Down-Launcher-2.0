# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

# Collecting PyQt6 data and required files
datas = collect_data_files('PyQt6', include_py_files=False) + [
    ('assets/images/test6.png', 'assets/images/'),
    ('qt.conf', '.')  # Adding qt.conf to root
]

# Collect all PyQt6-related dynamic libraries
binaries = collect_dynamic_libs('PyQt6')  # Automatically find and include DLLs

a = Analysis(
    ['splash_screen.py'],
    pathex=[],
    binaries=binaries,  # Add binaries here
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Level_Down_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    icon='assets/images/test6.png',
    codesign_identity=None,
    entitlements_file=None,
    manifest="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
      <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
        <security>
          <requestedPrivileges>
            <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
          </requestedPrivileges>
        </security>
      </trustInfo>
    </assembly>
    """,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='splash_screen'
)
