import os
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

block_cipher = None

# Collect all package data, binaries, and hidden imports
bu_d, bu_b, bu_h = collect_all('browser_use')
gg_d, gg_b, gg_h = collect_all('google.genai')
ga_d, ga_b, ga_h = collect_all('google.auth')
pw_d, pw_b, pw_h = collect_all('playwright')
ft_d, ft_b, ft_h = collect_all('flet')
ft2_d, ft2_b, ft2_h = collect_all('flet_desktop')

all_datas    = bu_d + gg_d + ga_d + pw_d + ft_d + ft2_d
all_binaries = bu_b + gg_b + ga_b + pw_b + ft_b + ft2_b
all_hidden   = (
    bu_h + gg_h + ga_h + pw_h + ft_h + ft2_h +
    collect_submodules('browser_use') +
    collect_submodules('google.genai') +
    collect_submodules('playwright') +
    [
        'flet', 'flet_desktop',
        'google.auth', 'google.auth.credentials',
        'google.auth.transport',
        'pydantic', 'pydantic_core',
        'asyncio', 'asyncio.events',
        'langchain_core',
    ]
)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy', 'numpy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Bluebot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Bluebot',
)
