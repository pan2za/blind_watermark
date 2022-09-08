# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['viewer.py'],
    pathex=['D:\\blind_watermark\\ui'],
    binaries=[],
    datas=[('c:\\program files\\windowsapps\\pythonsoftwarefoundation.python.3.10_3.10.2032.0_x64__qbz5n2kfra8p0\\lib\\site-packages','D:\\blind_watermark\\lib')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='viewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
