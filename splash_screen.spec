# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['splash_screen.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/dcann/AppData/Local/Programs/Python/Python311/Lib/site-packages/PyQt5/Qt/plugins/platforms', 'PyQt5/Qt5/plugins/platforms')],
    hiddenimports=[],
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
    name='splash_screen',
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
)
