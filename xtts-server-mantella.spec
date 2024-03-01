# -*- mode: python ; coding: utf-8 -*-

# Import collect_data_files function from PyInstaller
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect data files for specific packages, if necessary
a = Analysis(['__main__.py'],
             pathex=['D:\\Modelisation_IA\\xtts-api-server-mantella_build_exe_test\\'],
             binaries=[],
             datas=collect_data_files('tts'),  # Collecting data files for 'tts'
             hiddenimports=[
                 'os', 'subprocess', 'sys', 'requests', 'pyaudio', 'pyttsx3', 'fastapi', 'uvicorn', 
                 'loguru', 'pydantic', 'pydub', 'python_dotenv', 'torch', 'torchaudio', 'stream2sentence', 
                 'numpy', 'threading', 'traceback', 'logging', 'wave', 'queue', 'shutil', 'json', 're', 
                 'socket', 'io', 'TTS.api', 'torch.multiprocessing', 'tqdm', 'pathlib', 'packaging.version', 
                 'pydantic.BaseModel', 'typing.Optional', 'typing.Union', 'typing.List', 'typing.Iterator', 
                 'cutlet', 'fugashi', 'fugashi.unidic_lite', 'transformers.AutoModel', 'transformers.AutoTokenizer',
             ],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='xtts-server-mantella',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          argv_emulation=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)

coll = COLLECT(exe,
               a.binaries,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='xtts-server-mantella')
