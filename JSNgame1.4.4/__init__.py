# JSNgame/__init__.py
import importlib.util
import importlib.machinery  # 必须导入这个！
import os
import sys

# 1. 获取当前目录
_dir = os.path.dirname(__file__)
_core_path = os.path.join(_dir, "_core.dll")

# 2. 检查文件是否存在（避免后续错误）
if not os.path.exists(_core_path):
    raise FileNotFoundError(f"核心文件 _core.dll 不存在，请检查编译是否成功。")

# 3. 显式创建一个 ExtensionFileLoader（专门加载动态库）
loader = importlib.machinery.ExtensionFileLoader("_core", _core_path)
# 4. 根据 loader 创建 spec
spec = importlib.util.spec_from_loader("_core", loader)
# 5. 创建模块对象
_core = importlib.util.module_from_spec(spec)
# 6. 执行加载（即执行动态库中的 PyInit__core）
loader.exec_module(_core)

# 7. 暴露所有公开属性到当前包
for attr_name in dir(_core):
    if not attr_name.startswith('_'):
        globals()[attr_name] = getattr(_core, attr_name)

# 8. 动态继承 __all__
if hasattr(_core, '__all__'):
    __all__ = _core.__all__
else:
    __all__ = [name for name in dir(_core) if not name.startswith('_')]

# 9. 修复子模块查找父包的补丁
sys.modules['JSNgame'] = sys.modules[__name__]
