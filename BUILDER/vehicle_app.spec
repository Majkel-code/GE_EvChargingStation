# -*- mode: python ; coding: utf-8 -*-

import os
import time
import PyInstaller.config
dir = os.getcwd()
timestr = time.strftime("%Y%m%d_%H%M")
PyInstaller.config.CONF['distpath'] = f"{dir}/BUILDER/vehicle/out_{timestr}"

a = Analysis(
    [f'{dir}/VEHICLE/vehicle_server.py'],
    pathex=[],
    binaries=[],
    datas=[(f'{dir}/VEHICLE/veh_config', 'veh_config'),
    (f'{dir}/VEHICLE/veh_modules', 'veh_modules')],
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
    name='vehicle_app',
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
