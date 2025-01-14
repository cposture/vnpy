# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 收集所有模块的数据文件
def collect_data_files():
    datas = []
    # UI资源文件
    import vnpy_ctastrategy
    import vnpy_ctabacktester
    import vnpy_datamanager
    import vnpy.trader.ui  # 添加主界面UI模块
    
    modules = [vnpy_ctastrategy, vnpy_ctabacktester, vnpy_datamanager]
    
    # 添加主界面图标
    trader_ui_path = os.path.dirname(vnpy.trader.ui.__file__)
    if os.path.exists(os.path.join(trader_ui_path, 'ico')):
        datas.extend([
            (os.path.join(trader_ui_path, 'ico', '*'), os.path.join('vnpy', 'trader', 'ui', 'ico')),
        ])
    
    # 添加各模块的UI资源
    for module in modules:
        module_path = os.path.dirname(module.__file__)
        # 添加UI文件夹
        if os.path.exists(os.path.join(module_path, 'ui')):
            datas.extend([
                (os.path.join(module_path, 'ui', '*'), os.path.join(module.__name__, 'ui')),
            ])
        # 添加图标文件夹
        if os.path.exists(os.path.join(module_path, 'ui', 'ico')):
            datas.extend([
                (os.path.join(module_path, 'ui', 'ico', '*'), os.path.join(module.__name__, 'ui', 'ico')),
            ])
            
        # 特别处理 vnpy_ctastrategy 的策略文件
        if module.__name__ == 'vnpy_ctastrategy':
            strategies_path = os.path.join(module_path, 'strategies')
            if os.path.exists(strategies_path):
                for file in os.listdir(strategies_path):
                    if file.endswith('.py'):
                        datas.append((
                            os.path.join(strategies_path, file),
                            os.path.join(module.__name__, 'strategies')
                        ))
    
    # 添加 py_mini_racer 相关文件
    import py_mini_racer
    mini_racer_path = os.path.dirname(py_mini_racer.__file__)
    
    # 添加动态库
    if os.path.exists(os.path.join(mini_racer_path, 'libmini_racer.dylib')):
        datas.append((os.path.join(mini_racer_path, 'libmini_racer.dylib'), '.'))
    
    # 添加 icudtl.dat
    if os.path.exists(os.path.join(mini_racer_path, 'icudtl.dat')):
        datas.append((os.path.join(mini_racer_path, 'icudtl.dat'), '.'))
    
    # 添加其他可能的依赖文件
    for file in ['natives_blob.bin', 'snapshot_blob.bin']:
        if os.path.exists(os.path.join(mini_racer_path, file)):
            datas.append((os.path.join(mini_racer_path, file), '.'))
    
    # 添加 akshare 数据文件
    import akshare
    akshare_path = os.path.dirname(akshare.__file__)
    
    # 添加 calendar.json
    calendar_path = os.path.join(akshare_path, 'file_fold', 'calendar.json')
    if os.path.exists(calendar_path):
        datas.append((calendar_path, 'akshare/file_fold'))
    
    # 添加其他数据文件
    for root, dirs, files in os.walk(akshare_path):
        for file in files:
            if file.endswith('.json'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, akshare_path)
                datas.append((full_path, os.path.join('akshare', rel_path)))
    
    return datas

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files(),
    hiddenimports=[
        # 核心功能模块
        'vnpy_ctastrategy',
        'vnpy_ctastrategy.ui',
        'vnpy_ctastrategy.base',
        'vnpy_ctastrategy.engine',
        'vnpy_ctastrategy.template',
        'vnpy_ctastrategy.strategies',  # 添加策略目录
        'vnpy_ctastrategy.strategies.*',  # 添加所有策略文件
        'vnpy_ctabacktester',
        'vnpy_ctabacktester.ui',
        'vnpy_datamanager',
        'vnpy_datamanager.ui',
        'vnpy_sqlite',  # 数据库
        'vnpy_akshare',  # 数据服务
        'akshare',
        
        # UI相关
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
        'PyQt5.sip',
        'PyQt5.QtChart',
        
        # 数据分析相关
        'numpy',
        'pandas',
        'matplotlib',
        'pyqtgraph',
        'akshare',
        'py_mini_racer',
        'py_mini_racer._mini_racer',
        'py_mini_racer._dll',
        
        # TA-Lib相关
        'talib',
        'talib.stream',
        'talib._ta_lib',
        
        # 数据库相关
        'sqlalchemy',
        'sqlite3',
        
        # 网络相关
        'requests',
        'websocket',
        'json',
        
        # 其他常用模块
        'typing',
        'datetime',
        'time',
        'copy',
        'csv',
        'logging',
        'pathlib',
        'threading',
        'traceback',
        'sys',
        'os',
        'importlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',  # 不需要的 GUI 库
        'PIL',      # 不需要的图像处理库
        'scipy',    # 如果不需要科学计算
        'h5py',     # 如果不需要 HDF5 支持
        'IPython',  # 如果不需要交互式 shell
        'ipykernel',
        'notebook',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    module_collection_mode={'numpy': 'pyz', 'pandas': 'pyz'},  # 将大模块打包到 pyz
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher,
    compression_level=9  # 最高压缩级别，可以减少 IO
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='vnpy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,  # 在 Mac 上不需要参数模拟
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    optimize=2  # 使用 Python 的优化标志
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='vnpy'
)

app = BUNDLE(
    coll,
    name='vnpy.app',
    bundle_identifier='com.vnpy.trader',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.10.0',
        'NSRequiresAquaSystemAppearance': 'NO',
    }
)

# 添加 TA-Lib 动态库
import os
import talib
talib_path = os.path.dirname(talib.__file__)
if os.path.exists(os.path.join(talib_path, '_ta_lib.so')):
    a.datas += [(os.path.join('talib', '_ta_lib.so'), os.path.join(talib_path, '_ta_lib.so'), 'BINARY')]
elif os.path.exists(os.path.join(talib_path, '_ta_lib.dylib')):
    a.datas += [(os.path.join('talib', '_ta_lib.dylib'), os.path.join(talib_path, '_ta_lib.dylib'), 'BINARY')]
