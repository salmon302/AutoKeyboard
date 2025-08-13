# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.', 'src'],
    binaries=[],
    datas=[('src', 'src')],
    hiddenimports=[
        'pynput.keyboard._win32',
        'pynput.mouse._win32', 
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'gui.main_window',
        'core.key_recorder', 
        'core.key_player',
        'core.hotkey_manager',
        'data.settings',
        'data.key_sequence', 
        'utils.key_utils'
    ],
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
    name='AutoKeyboard-Presser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app (no console window)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
    version_file=None
)
