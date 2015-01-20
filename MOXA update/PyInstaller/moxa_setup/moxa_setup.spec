# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'moxa_setup.py')],
             pathex=['C:\\Users\\Carsten\\Documents\\Projekter\\Moxa\\PyInstaller\\moxa_setup'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='moxa_setup.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
