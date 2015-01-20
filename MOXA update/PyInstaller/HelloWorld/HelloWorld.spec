# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'HelloWorld.py')],
             pathex=['C:\\Users\\Carsten\\Documents\\Projekter\\Moxa\\PyInstaller\\HelloWorld'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='HelloWorld.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
