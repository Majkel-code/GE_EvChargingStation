# -*- mode: python ; coding: utf-8 -*-

import os
import time
import PyInstaller.config
dir = os.getcwd()
timestr = time.strftime("%Y%m%d_%H%M")
PyInstaller.config.CONF['distpath'] = f"{dir}/BUILDER/charger/out_{timestr}"

a = Analysis(
    [f'{dir}/CHARGER/charger_server.py'],
    pathex=[],
    binaries=[],
    datas=[(f'{dir}/CHARGER/config', 'config'),
    (f'{dir}/CHARGER/modules', 'modules'),
    (f'{dir}/CHARGER/simulations', 'simulations')],
    hiddenimports=['requests', 'multiprocessing'],
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
    name='charger_app',
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
