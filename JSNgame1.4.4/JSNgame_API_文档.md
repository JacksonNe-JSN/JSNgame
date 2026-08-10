# JSNgame API 参考文档

> **版本**: v1.44_demo  
> **作者**: JacksonNe (JSN)  
> **简介**: 基于 Pygame 的高度封装游戏开发库，集成渲染、音效、事件、AI 寻路、3D 引擎等模块。  
> **安装**: 将 `JSNgame` 文件夹置于项目目录下，`from LIBbase import JSNgame as jg` 即可使用。

---

## 目录

- [快速开始](#快速开始)
- [全局工具](#全局工具)
- [Screen — 屏幕管理](#screen--屏幕管理)
- [event2 / event — 事件系统](#event2--event--事件系统)
- [Event — 事件常量字典](#event--事件常量字典)
- [mixer — 音频管理](#mixer--音频管理)
- [Word — 文本处理](#word--文本处理)
- [Time — 时间管理](#time--时间管理)
- [Random — 随机工具](#random--随机工具)
- [IT — 网络工具](#it--网络工具)
- [PengZhuangXiang — 碰撞箱系统](#pengzhuangxiang--碰撞箱系统)
- [Xbox / XboxController — 手柄](#xbox--xboxcontroller--手柄)
- [XuNiShouBin — 虚拟手柄](#xunishoubin--虚拟手柄)
- [AI_tree — AI 寻路与神经网络](#ai_tree--ai-寻路与神经网络)
- [third_D — 简易 3D 引擎](#third_d--简易-3d-引擎)
- [JSNgame3D — OpenGL 3D 查看器](#jsngame3d--opengl-3d-查看器)
- [message — 桌面消息弹窗](#message--桌面消息弹窗)
- [surface_to_file — 保存图片](#surface_tofile--保存图片)
- [附录：键盘常量速查](#附录键盘常量速查)

---

## 快速开始

```python
from LIBbase import JSNgame as jg

# 1. 创建游戏窗口 (贴纸尺寸 800x600)
screen = jg.Screen(size=(800, 600), title='我的游戏')

# 2. 创建事件和时钟
event = jg.event
clock = jg.Time()

# 3. 主循环
running = True
while running:
    # 处理事件
    for e in event.get():
        if e.type == jg.Event['QUIT']:
            jg.Exit()

    # 绘制
    screen.fill((255, 255, 255))
    screen.word('Hello JSNgame!', plc=(100, 100), rgb=(0, 0, 0), big=40)
    screen.blit('my_image.png', plc=(300, 200))
    screen.load()  # 刷新到窗口

    clock.FPS(60)  # 限制 60 帧
```

---

## 全局工具

### `__version__`
版本号字符串，当前为 `"v1.44_demo"`。

### `class JGerror(Exception)`
自定义异常基类，用于标识库内部的错误。

### `wrong(e)`
全局异常处理函数。打印错误信息、写入 `log.txt` 日志文件，然后退出程序。

| 参数 | 类型 | 说明 |
|------|------|------|
| `e` | `Exception` | 要处理的异常对象 |

### `Log(e) -> str`
将异常格式化为详细的日志字符串（含时间、错误类型、位置追踪）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `e` | `Exception` | 异常对象 |

**返回**: 格式化的日志字符串。

### `Exit(n=1)` / `exit(n=1)`
安全退出 pygame 和程序。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `n` | `int` | 1 | 0 只退出 pygame 不退出进程，1 完全退出 |

### `Key()`
授权验证函数（通常不需要手动调用）。

### `surface_to_file(surface, path, size=None, jiami=False)`
将 pygame Surface 保存为图片。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `surface` | `pygame.Surface` | — | 要保存的 Surface 对象 |
| `path` | `str` | — | 保存路径（不含扩展名） |
| `size` | `tuple` | `None` | 可选，缩放尺寸 `(宽, 高)` |
| `jiami` | `bool` | `False` | `True` 则加密保存为 `.jpt` 格式 |

### `creat_easy(para=None)`
将当前文件覆盖为示例模板代码（会弹出确认对话框）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `para` | `str` | 模板类型，如 `"game"` |

---

## Screen — 屏幕管理

**核心游戏屏幕类**：管理窗口创建、图像绘制、文字渲染、特效、视频播放等所有视觉功能。

### `Screen.__init__(size, icon, title, Full, size_change)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `size` | `tuple` | `(100,100)` | **贴纸原始尺寸**（固定，缩放以此为基础） |
| `icon` | `str` | `'./logo.bmp'` | 窗口图标路径 |
| `title` | `str` | `'NewGame'` | 窗口标题 |
| `Full` | `int` | `0` | 0=窗口, 1=独占全屏, 2=有框全屏, 3=无框全屏 |
| `size_change` | `int` | `0` | 0=不可调, 1=可调(最小=size), 2=可调(无限制) |

> **注意**: `Full` 和 `size_change` 同时非零时会冲突，自动将 `Full` 降为 0。

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `size` | `tuple` | 贴纸原始尺寸 |
| `screen` | `pygame.Surface` | 内部绘制表面（贴纸），你画图的目标 |
| `screens` | `pygame.Surface` | 实际窗口表面 |
| `copy` | `list` | 屏幕历史快照（最多 144 帧） |
| `image_cache` | `dict` | 图片缓存字典 |
| `font_cache` | `dict` | 字体缓存字典 |

### 核心绘图方法

#### `load()`
将贴纸 (`self.screen`) 按比例缩放**居中**绘制到窗口（自动留黑边），并更新历史快照。等同于"刷帧"。  
**每帧最后必须调用一次**。

#### `blit(pto, plc, jd, mode, big, glass, jd_center)`
绘制图像到贴纸。最常用的绘图方法。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `pto` | `str` / `pygame.Surface` | — | 图片路径（支持 `.png/.jpg/.jpt`）或 Surface 对象 |
| `plc` | `tuple` | `(0,0)` | 绘制位置 `(x, y)` |
| `jd` | `float` / `int` | `0` | 旋转角度（度） |
| `mode` | `str` | `'normal'` | 绘制模式：`'normal'` 普通 / `'long_bg'` 长背景滚动 |
| `big` | `int`/`float`/`list` | `None` | 缩放：`float` 等比例 / `[w, h]` 指定像素 |
| `glass` | `int` | `255` | 透明度 (0-255, 255=不透明) |
| `jd_center` | `tuple` | `None` | 自定义旋转中心 `(x, y)`，默认图像中心 |

**长背景模式** (`mode='long_bg'`)：将图片水平分块渲染，适合横向卷轴背景。`plc` 的 x 坐标控制滚动偏移。

#### `word(words, plc, rgb, big, house_rgb, typeface, Anti_Aliasing, GuDingDaXiao)`
在屏幕上绘制文字。自动检测中/英/俄文并选用合适字体。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `words` | `str` | `'NEW_WORD'` | 要绘制的文本 |
| `plc` | `tuple` | `(0,0)` | 位置 `(x, y)` |
| `rgb` | `tuple` | `(255,255,255)` | 文字颜色 `(R, G, B)` |
| `big` | `int` | `50` | 字号（会自动按语言缩放） |
| `house_rgb` | `tuple` | `None` | 背景色 `(R, G, B)`，为 `None` 则透明背景 |
| `typeface` | `str` | `None` | 指定字体文件名（放于 `zt/` 文件夹），如 `"simhei.ttf"`。`"pygame"` 用默认字体 |
| `Anti_Aliasing` | `bool` | `False` | 是否启用抗锯齿 |
| `GuDingDaXiao` | `int`/`bool` | `False` | `0/False`=自适应, `1/True`=固定, `2`=特殊固定模式 |

**返回**: `pygame.Surface` 文本渲染后的表面。

#### `speaking(word, plc, act, big, word_rgb, house_rgb, speed, GuDingDaXiao)`
文字逐字显示效果（类似 RGP 对话）。**阻塞函数**，执行期间循环卡住。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `word` | `str` | `'...'` | 要显示的文本 |
| `plc` | `tuple` | `(0,0)` | 位置 |
| `act` | `bool` | `True` | 是否执行逐字动画 |
| `big` | `int` | `50` | 字号 |
| `word_rgb` | `tuple` | `(0,0,0)` | 文字颜色 |
| `house_rgb` | `tuple` | `None` | 背景色 |
| `speed` | `float` | `0.1` | 每字间隔时间（秒） |
| `GuDingDaXiao` | `bool` | `False` | 是否固定大小 |

**返回**: `False`（完成时）。

#### `speaking_with(word, plc, act, big, word_rgb, house_rgb, speed, command, GuDingDaXiao)`
逐字显示，每出一个字执行一次 `command`。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `command` | `list` | `[[], []]` | 要执行的命令列表，每个元素为 `[函数, 参数1, 参数2...]` |

其余参数同 `speaking()`。

#### `fill(rgb, mode, glass)`
填充屏幕背景。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `rgb` | `tuple` | `(255,255,255)` | 颜色 |
| `mode` | `str` | `'normal'` | `'normal'` 普通填充 / `'glass'` 半透明填充 |
| `glass` | `int` | `255` | 透明度 (0-255，仅 `mode='glass'` 生效) |

#### `vfill(rgb, glass, mode)`
高级填充方法。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `rgb` | `tuple` | `(0,0,0)` | 颜色 |
| `glass` | `int` | `255` | 透明度 |
| `mode` | `str` | `'normal'` | `'normal'` 预乘混合 / `'glass'` 最小值混合 |

### 特效与过渡

#### `TeXiao(name, strength, *args, **kwargs)`
应用屏幕特效（基于 NumPy 实现）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | `str` | 特效名称（见下表） |
| `strength` | `int` | 特效强度 (0-100) |
| `**kwargs` | — | 额外参数，如 `jd=10.5` 指定色差方向（时钟角度） |

| 特效名称 | 说明 |
|----------|------|
| `'ZhenDong'` | 屏幕震动 + 色差 |
| `'SeCha'` | 色差偏移（红蓝通道分离），可用 `jd` 参数控制方向 |
| `'BoWenSeCha'` | 波纹色差（动态动画效果），可用 `jd` 参数控制方向 |
| `'GuangJiao'` | 广角/鱼眼畸变效果 |
| `'MaSaiKe'` | 马赛克效果 |
| `'MoHu'` | 高斯模糊（下采样+上采样） |
| `'DongTaiMoHu'` | 动态模糊（混合历史帧） |

#### `ts(mode, pto, rgb, plc, finish_time, command)`
屏幕淡入/淡出过渡效果。**阻塞函数**。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `mode` | `str` | `'begin'` | `'begin'` 淡入（从黑到画面） / `'end'` 淡出（到黑） |
| `pto` | `str`/`list` | `None` | 背景图片路径或路径列表 |
| `rgb` | `tuple` | `(0,0,0)` | 过渡颜色 |
| `plc` | `tuple` | `None` | 背景图片位置 |
| `finish_time` | `float` | `2` | 过渡总时长（秒） |
| `command` | `list` | `[[], []]` | 每帧同时执行的命令 |

**返回**: `False`（完成时）。

### 绘图方法

#### `draw(mode, plc, size, rgb)`
绘制基本几何图形。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `mode` | `str` | — | 绘图模式（见下表） |
| `plc` | `list` | `[]` | 中心位置 `[x, y]` |
| `size` | `list` | `[]` | 尺寸 `[宽, 高]` |
| `rgb` | `list` | `[[255,255,255], [0,0,0]]` | 颜色 `[边框色, 填充色]`，填充为 `[None, None, None]` 时不填充 |

| mode 值 | 别名 | 说明 |
|---------|------|------|
| `'Xian'` | `'line'` | 线（size 为终点偏移） |
| `'Yuan'` | `'round'` | 椭圆/圆 |
| `'Fang'` | `'square'` | 矩形 |
| `'Xin'` | `'heart'` | 心形（参数方程） |
| `'Dian'` | `'point'` | 圆点 |

### 交互组件

#### `YinLiangTiao(Pos, plc, size, rgb, down, word)`
绘制音量控制条（可交互）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `Pos` | `tuple` | `(0,0)` | 鼠标位置（用于交互检测） |
| `plc` | `list` | `[0,0]` | 控制条位置 |
| `size` | `list` | `[100,10]` | 控制条尺寸 |
| `rgb` | `list` | 见源码 | `[进度色, 背景色, 文字色]` |
| `down` | `bool` | `False` | 是否检测鼠标点击拖动 |
| `word` | `str` | `'Volume'` | 显示的文字标签 |

**返回**: `float` 当前音量值 (0.0-1.0)。

#### `TuoDongTiao(plc, size, rgb, down, up, id)`
可交互拖动条组件，支持多个独立实例。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `plc` | `list`/`tuple` | — | 位置 `[x, y]` |
| `size` | `list`/`tuple` | — | 尺寸 `[宽度, 高度]` |
| `rgb` | `tuple` | `((0,0,0), (255,0,0))` | `(背景色, 进度条色)` |
| `down` | `bool` | `None` | `None` 自动检测左键 / `True/False` 手动控制 |
| `up` | `float` | `None` | 强制设置进度值 (0.0-1.0) |
| `id` | `str` | `"default"` | 唯一标识符（多个拖动条必须不同 id） |

**返回**: `float` 当前进度值 (0.0-1.0)。

### 视频播放

#### `movie(file, plc, speed, blit, rgb, replay)`
播放视频文件（支持 MP4/MKV/JMV 加密格式），带抠图功能。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `file` | `str` | — | 视频文件路径 |
| `plc` | `list` | `[0,0]` | 绘制位置 |
| `speed` | `float` | `30.0` | 播放帧率 |
| `blit` | `bool` | `True` | 是否将当前帧绘制到屏幕 |
| `rgb` | `list` | `None` | 抠图参数 `[R, G, B, 阈值]`，`None` 不抠图 |
| `replay` | `bool` | `False` | 是否强制重置播放 |

**返回**: `int` 当前帧号。

### 3D 渲染

#### `third_D(file, plc, jiaodu, light)`
渲染 3D 模型（调用内置简易 3D 引擎）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `file` | `str` | — | 模型文件路径 |
| `plc` | `tuple` | `(0,0,0)` | 位置 `(x, y, z)`，z 控制远近 |
| `jiaodu` | `tuple` | `(0,0,0)` | 旋转角度 `(x, y, z)` |
| `light` | `float` | `1.0` | 光照强度 (0.0-1.0) |

### 其他方法

#### `handle_events()`
处理窗口大小调整事件。**返回**: `bool` 是否调整了大小。

#### `memory(fps)`
获取屏幕历史快照。`fps=None` 返回全部历史列表，指定帧号返回对应帧。

#### `surface(plc, size, glass) -> Surface实例`
创建自定义的子 Surface 对象，支持独立的 fill/blit/change/TeXiao/load 操作。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `plc` | `list` | `[0,0]` | 在屏幕上的位置 |
| `size` | `list` | `[0,0]` | 尺寸 |
| `glass` | `int`/`bool` | `False` | 透明度支持：`False` 无 / `0-255` 整数值 |

返回的 Surface 对象有以下方法：

| 方法 | 说明 |
|------|------|
| `.fill(color)` | 填充颜色 |
| `.blit(pto, plc, jd, big)` | 绘制图像到子 Surface |
| `.change(attr, value)` | 修改属性（`"size"`/`"plc"`/`"glass"`） |
| `.TeXiao(mode, strength)` | 应用特效 |
| `.load()` | 将子 Surface 绘制到屏幕 |

#### `clean_cache(Type, n)`
清理内部缓存。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `Type` | `str` | `"all"` | `"all"`=全部, `"img"`=图片, `"word"`=字体 |
| `n` | `str` | `None` | 指定要删除的缓存键（路径名） |

---

## event2 / event — 事件系统

全局事件处理实例：`event = jg.event`（在导入时自动创建）。

### `event.get() -> list`
获取 pygame 事件队列，同时更新内部状态（鼠标、键盘、滚轮）。每帧开头调用一次。

### `event.updata()`
`get()` 的别名方法。

### `event.get_pos() -> list`
直接查询当前鼠标位置，返回 `[x, y]`。

### `event.mouse_down(FangXiang) -> bool`
检测鼠标按键是否按住。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `FangXiang` | `int` | `1` | 1=左键, 2=中键, 3=右键 |

**返回**: `True` 表示该键当前被按住。

### `event.click(FangXiang, n) -> bool`
检测在 n 秒内是否**按下**了鼠标按键（边缘触发，消费制）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `FangXiang` | `int` | `1` | 1=左键, 2=中键, 3=右键 |
| `n` | `float` | `0.5` | 时间窗口（秒） |

**返回**: `True` 表示在该时间窗口内发生过按下事件且未被消费。

### `event.key_down(key) -> bool`
检测键盘按键是否按住。

| 参数 | 类型 | 说明 |
|------|------|------|
| `key` | `int` | 按键值，使用 `jg.Event['K_a']` 等常量 |

**返回**: `bool`。

### `event.test(e, event_type) -> bool`
检测事件类型是否匹配。

| 参数 | 类型 | 说明 |
|------|------|------|
| `e` | `pygame.event.Event` | 事件对象，不传则用内部缓存的最后事件 |
| `event_type` | `int` | 事件类型值 |

### `event.test_key(e, key) -> bool`
检测按键按下事件。

### `event.test_key_UP(e, key) -> bool`
检测按键释放事件。

### `event.button(e, size, plc) -> bool`
检测鼠标是否在矩形区域内。

| 参数 | 类型 | 说明 |
|------|------|------|
| `e` | `Event` / `list` | 事件或鼠标位置 |
| `size` | `tuple` | 区域尺寸 |
| `plc` | `tuple` | 区域位置 |

### `event.wheel_down(e=None) -> int`
获取垂直滚轮累积值（并清零计数器）。

### `event.wheel_horizontal(e=None) -> int`
获取水平滚轮累积值（并清零计数器）。

### `event.pin(plc)`
将鼠标锁定到指定位置。`plc = [x, y]`。

### `event.hide_mouse()`
隐藏鼠标指针。

### `event.ShouBin(mode, id) -> XboxController|XuNiShouBin`
创建手柄控制器。

| 参数 | 类型 | 说明 |
|------|------|------|
| `mode` | `str` | `'xbox'` 或 `'x'` = Xbox 手柄 / `'virtual'` 或 `'xuni'` = 虚拟手柄 |
| `id` | — | 手柄标识 |

---

## Event — 事件常量字典

使用 `jg.Event['常量名']` 获取数值。

### 核心事件

| 常量 | 值 | 说明 |
|------|-----|------|
| `'QUIT'` | 0x100 | 关闭窗口 |
| `'KEYDOWN'` | 768 | 按键按下 |
| `'KEYUP'` | 769 | 按键释放 |
| `'MOUSEMOTION'` / `'MOUSEMOVE'` | 1024 | 鼠标移动 |
| `'MOUSEBUTTONDOWN'` | 1025 | 鼠标按下 |
| `'MOUSEBUTTONUP'` | 1026 | 鼠标释放 |
| `'MOUSEWHEEL'` | 1027 | 滚轮滚动 |

### 窗口事件

| 常量 | 值 | 说明 |
|------|-----|------|
| `'VIDEORESIZE'` | 16 | 窗口大小改变 |
| `'WINDOWFOCUSGAINED'` | 18 | 获得焦点 |
| `'WINDOWFOCUSLOST'` | 19 | 失去焦点 |

### 键盘按键常量

| 分类 | 示例常量 |
|------|---------|
| 字母键 | `'K_a'` ~ `'K_z'` (97-122) |
| 数字键 | `'K_0'` ~ `'K_9'` (48-57) |
| 功能键 | `'K_ESCAPE'`(27), `'K_SPACE'`(32), `'K_RETURN'`(13), `'K_BACKSPACE'`(8), `'K_DELETE'`(127) |
| 方向键 | `'K_UP'`, `'K_DOWN'`, `'K_LEFT'`, `'K_RIGHT'` |
| F 键 | `'K_F1'` ~ `'K_F12'` (282-293) |
| 修饰键 | `'K_LCTRL'`, `'K_RCTRL'`, `'K_LSHIFT'`, `'K_RSHIFT'`, `'K_LALT'`, `'K_RALT'` |

---

## mixer — 音频管理

### `mixer.__init__(channels)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `channels` | `int` | `15` | 音频通道数 |

### BGM（背景音乐）

#### `mixer.bgm(file, sound_bigs, times, start)`
播放背景音乐。支持 `.jmus` 加密格式。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `file` | `str` | — | 音频文件路径 |
| `sound_bigs` | `float` | `None` | 音量 (0.0-1.0)，默认使用全局音量 |
| `times` | `int` | `-1` | 循环次数，-1=无限循环 |
| `start` | `float` | `None` | 起始位置（秒） |

#### `mixer.bgm_where() -> float`
获取当前 BGM 播放位置（秒）。

#### `mixer.stop_bgm()`
停止背景音乐。

### 音效

#### `mixer.sound(file, sound_bigs, plc, play) -> _Sound`
播放音效（带立体声定位）。支持 `.jmus` 加密格式。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `file` | `str` | — | 音频文件路径 |
| `sound_bigs` | `float` | `None` | 音量 (0.0-1.0) |
| `plc` | `int` | `0` | 立体声定位 (-90~90)：-90=全左, 0=居中, 90=全右 |
| `play` | `bool/int` | `1` | 是否立即播放 |

**返回**: `_Sound` 对象用于后续控制。

### `_Sound` 音效控制对象

| 方法 | 参数 | 说明 |
|------|------|------|
| `.yinliang(volume)` | `0.0-1.0` | 设置该音效音量 |
| `.set_plc(plc)` | `-90~90` | 设置立体声定位 |
| `.stop()` | — | 停止播放 |
| `.clean()` | — | 清理释放 |
| `.re_play()` | — | 重新播放 |
| `.play()` | — | 在另一个通道同时播放（创建双胞胎），返回自身 |
| `.stop_twin(index)` | `int`/`None` | 停止指定双胞胎通道 |
| `.get_twin_count()` | — | 获取双胞胎数量 |

### 全局控制

| 方法 | 参数 | 说明 |
|------|------|------|
| `mixer.volume(volume)` | `0.0-1.0` | 设置全局音量 |
| `mixer.get_volume()` | — | 获取当前音量 |
| `mixer.stop_all()` | — | 停止所有音频 |

### 麦克风

| 方法 | 说明 |
|------|------|
| `mixer.open_mkf()` | 打开麦克风（需安装 `pyaudio`） |
| `mixer.get_mkf()` | 获取麦克风数据，返回 `{"YinLiang": float, "YinDiao": float}` |
| `mixer.close_mkf()` | 关闭麦克风 |

---

## Word — 文本处理

### 语言检测

#### `Word().is_chinese(chars) -> bool`
检查字符是否为中文（Unicode 范围 `\u4e00`~`\u9fff`）。

#### `Word().is_russian(chars) -> bool`
检查字符是否为俄文西里尔字母（Unicode 范围 `\u0400`~`\u04FF`）。

#### `Word().check_language(text) -> str`
检测文本主要语言。

| 参数 | 类型 | 说明 |
|------|------|------|
| `text` | `str` | 输入文本 |

**返回**: `'Chinese'` / `'English'` / `'Russian'` / `'Mixed or other'`

### 其他工具

#### `Word().entry(Screen, plc, bg_color, big, plc_pos) -> tuple`
创建文本输入框。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `Screen` | `pygame.Surface` | — | 屏幕对象 |
| `plc` | `tuple` | `(0,0)` | 位置 |
| `bg_color` | `tuple` | `(255,255,255)` | 背景色 |
| `big` | `tuple` | `(100,50,400)` | `(y偏移, 高度, 宽度)` |
| `plc_pos` | `tuple` | `(0,0)` | 鼠标位置（用于激活检测） |

**返回**: `(text_surface, active_bool)`

#### `Word().find_dir(root, file) -> str|bool`
在目录中递归搜索文件。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `root` | `str` | `'C:'` | 起始目录 |
| `file` | `str` | `'360'` | 目标文件名 |

**返回**: 找到返回完整路径，否则返回 `False`。

#### `Word().FenGe(word, FenGe) -> list`
分割字符串。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `word` | `str` | — | 要分割的字符串 |
| `FenGe` | `str` | `" "` | 分隔符 |

**返回**: 分割后的列表。

---

## Time — 时间管理

### `Time.FPS(fps) -> int`
控制帧率。每帧在循环末尾调用。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `fps` | `int` | `None` | 目标帧率，不传则返回实际帧时间 |

**返回**: 实际帧时间（毫秒）。

### `Time.get_FPS() -> float`
获取当前实际帧率。

### `Time.get_time() -> dict` (静态方法)
获取当前精确时间。

**返回**: `{'年': int, '月': int, '日': int, '时': int, '分': int, '秒': int, '总和': str}`

---

## Random — 随机工具

| 方法 | 参数 | 说明 |
|------|------|------|
| `.int(a, b)` | `int, int` | 返回 `[a, b]` 之间的随机整数 |
| `.float(a, b)` | `int/float` | 返回 `[a, b]` 之间的随机浮点数 |
| `.DaLuan(a)` | `list` | 打乱列表并返回新列表（不修改原列表） |
| `.QiePian(a, b)` | `list, int` | 从列表 a 中随机选取 b 个元素 |
| `.choose(a)` | `list` | 随机选择一个元素 |
| `.MiYao(length, binary)` | `int, bool` | 生成密码学安全的随机密钥。`binary=True` 返回 bytes，否则返回 hex 字符串 |

---

## IT — 网络工具

### `IT.open_www(address, tag, autoraise)`
打开网页。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `address` | `str` | — | 网址 |
| `tag` | `int` | `0` | 浏览器打开方式 |
| `autoraise` | `bool` | `True` | 是否自动激活窗口 |

### `IT.SouSuo(question, deep)`
调用 JSN 搜索功能。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `question` | `str` | — | 搜索问题 |
| `deep` | `int` | `5` | 搜索深度 |

---

## PengZhuangXiang — 碰撞箱系统

### `PengZhuangXiang.__init__(screen)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `screen` | `Screen` | `None` | 屏幕对象（用于可视化绘制） |

### 方法

#### `.add(plc, size, mode) -> _Box`
添加碰撞箱。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `plc` | `list` | `[0,0]` | 位置（矩形=左上角，圆形=圆心） |
| `size` | `list` | `[100,100]` | 尺寸 `[宽, 高]` |
| `mode` | `str` | `"Fang"` | `"Fang"` = 矩形, `"round"` = 圆形 |

**返回**: `_Box` 实例。

#### `.remove(box) -> bool`
移除碰撞箱。

#### `.test(box1, box2) -> list|None`
检测两个碰撞箱是否碰撞。

**返回**: `[方向列表1, 方向列表2]` 或 `None`（无碰撞）。

#### `.show()`
绘制所有碰撞箱到屏幕（需先调用 `set_screen()`）。
- 未碰撞时显示**蓝色**边框
- 碰撞时显示**红色**边框

#### `.set_screen(screen)`
设置绘制目标屏幕。

### `_Box` 碰撞箱实例

| 属性 | 类型 | 说明 |
|------|------|------|
| `.plc` | `list` | 位置，可读写 |
| `.size` | `list` | 尺寸，可读写 |
| `.mode` | `str` | 模式，只读 |

| 方法 | 说明 |
|------|------|
| `.change(attr, value)` | 修改属性（`"plc"` / `"size"`） |
| `.remove()` | 从管理器移除自身 |
| `.show()` | 绘制自身 |
| `.test(other)` | 返回分离向量 `[move_x, move_y]`（碰撞时）或 `[0.0, 0.0]`（无碰撞时） |

---

## Xbox / XboxController — 手柄

### `Xbox` 手柄管理器

```python
xbox = jg.Xbox()
```

#### `.get_event(id, dead_area) -> dict`
获取手柄完整状态。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | — | `None` | 手柄实例 ID，默认第一个 |
| `dead_area` | `int` | `0` | 摇杆死区 (0-10) |

**返回**:
```python
{
    "LS": (x, y, pressed),       # 左摇杆 (-10~10, 按下bool)
    "RS": (x, y, pressed),       # 右摇杆
    "ABXY": {"a": float, "b": float, "y": float, "x": float},  # 0.0~1.0
    "LT": float,                 # 左扳机 0.0~1.0
    "RT": float,                 # 右扳机
    "LB": float,                 # 左肩键
    "RB": float,                 # 右肩键
    "DP": (x, y),                # 方向键 (-1,0,1)
    "MENU": float,               # 菜单键
    "XBOX": float,               # Xbox 键
    "ZT": bool                   # 是否有任何输入
}
```

### `XboxController` 单手柄控制

通过 `event.ShouBin('xbox', id)` 获取。

| 方法 | 说明 |
|------|------|
| `.get()` | 获取状态（返回同上但按钮为 bool） |
| `.ZhenDong(strength)` | 震动 (0-100) |
| `.is_connected()` | 检查连接状态 |

---

## XuNiShouBin — 虚拟手柄

通过 `event.ShouBin('virtual', id)` 获取。用鼠标模拟摇杆。

| 方法 | 说明 |
|------|------|
| `.show(screen)` | 在屏幕上绘制虚拟手柄 |
| `.load(e)` | 处理鼠标事件更新手柄状态 |
| `.test()` | 返回 `[x_ratio, y_ratio]` (-1~1) |

---

## AI_tree — AI 寻路与神经网络

### `Game_AI` 寻路

```python
ai = jg.AI_tree.Game_AI()
```

#### `.find_road(start, end, obstacles, difficult, mode) -> 方向|bool|None`
**终极 AI 寻路函数**。智能切换算法（近距离 A\*，中距离中等，远距离低质量）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `start` | `tuple` | — | 起点 `(x, y)` |
| `end` | `tuple` | — | 终点 `(x, y)` |
| `obstacles` | `list` | — | 障碍物列表 |
| `difficult` | `int` | `0` | 难度参数 |
| `mode` | `int` | `0` | 方向模式：0=4方向, 1=8方向 |

**返回**:
- `[dx, dy]` 移动方向
- `True` 已到达
- `False` 无解
- `None` 暂时无路

内置 100% 无解检测（洪水填充算法）。

### `Jai` 神经网络 AI

```python
jai = jg.AI_tree.Jai(model_path, mode='train', ...)
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model_path` | `str` | — | 模型保存路径 |
| `mode` | `str` | `'train'` | `'train'` 训练 / `'use'` 使用 |
| `gamma` | `float` | 默认 | 折扣因子 |
| `lr` | `float` | 默认 | 学习率 |
| `batch_size` | `int` | 默认 | 批次大小 |
| `epochs_per_game` | `int` | 默认 | 每局训练轮数 |
| `max_actions` | `int` | 默认 | 最大动作数 |

| 方法 | 参数 | 说明 |
|------|------|------|
| `.out(state, can_move)` | `state`=状态, `can_move`=可选动作数 | 输出动作编号 |
| `.report(state, action, point)` | 状态、动作、奖励 | 反馈奖励（训练模式存储经验） |
| `.init()` | — | 一局结束触发学习 |
| `.set_print(level)` | `0`=静默, `1`=基础, `2`=详细, `3`=拟人 | 控制输出级别 |

---

## third_D — 简易 3D 引擎

基于射线投射风格的伪 3D 引擎。

```python
from LIBbase.JSNgame import third_D
engine = third_D.Simple3DEngine(width, height)
```

### 核心方法

| 方法 | 说明 |
|------|------|
| `.load()` | 执行一帧渲染 |
| `.move(FX, speed)` | 移动玩家：`'f'/'b'/'l'/'r'` (前/后/左/右) |
| `.turn(FX, jd)` | 旋转视角（弧度或角度字符串如 `"45°"`） |
| `.ray(plc, jd, num, pitch)` | 射线投射检测 |

### 环境配置

| 方法 | 说明 |
|------|------|
| `.set_longway(rgb, plc)` | 设置远景颜色和位置 |
| `.set_sky(texture)` | 设置天空纹理 |
| `.set_floor(texture)` | 设置地面纹理 |
| `.set_bg(bg)` | 设置背景 |
| `.wall(color, world_layout)` | 设置墙壁颜色/纹理和地图 |

### 广告牌（Billboard）

| 方法 | 说明 |
|------|------|
| `.create_billboard(...)` | 创建广告牌 |
| `.get_billboard(id)` | 获取广告牌 |
| `.remove_billboard(id)` | 移除广告牌 |

### AI 寻路（3D）

| 方法 | 说明 |
|------|------|
| `.AI_find_road(ai_pos, target_pos, speed)` | 3D 场景中的 AI 寻路 |

---

## JSNgame3D — OpenGL 3D 查看器

独立 3D 模型查看器，基于 OpenGL。

```python
from LIBbase.JSNgame import JSNgame3D
viewer = JSNgame3D.Object()
```

| 方法 | 参数 | 说明 |
|------|------|------|
| `.add(path, id, plc, big, jd)` | 路径、ID、位置、缩放、角度 | 加载 OBJ 模型 |
| `.handle_events()` | — | 处理鼠标拖拽旋转/滚轮缩放 |
| `.render()` | — | 渲染所有模型 |

---

## message — 桌面消息弹窗

基于 tkinter 和 plyer 的桌面通知工具。

```python
from LIBbase.JSNgame import message
# 或
jg.message
```

| 方法 | 参数 | 说明 | 返回 |
|------|------|------|------|
| `Message.text(title, text)` | 标题, 内容 | 信息弹窗 | `'ok'` |
| `Message.JingGao(title, text)` | 标题, 内容 | 警告弹窗 | `'ok'` |
| `Message.error(title, text)` | 标题, 内容 | 错误弹窗 | `'ok'` |
| `Message.ask(title, text)` | 标题, 内容 | 是/否选择 | `bool` |
| `Message.QueRen(title, text)` | 标题, 内容 | 确定/取消 | `bool` |
| `Message.windows(title, text, ico, time)` | 标题, 内容, 图标, 时长 | 系统通知 | — |

---

## 附录：键盘常量速查

使用 `jg.Event['常量名']` 获取。

| 按键 | 常量 | 值 |
|------|------|-----|
| A-Z | `'K_a'` ~ `'K_z'` | 97~122 |
| 0-9 | `'K_0'` ~ `'K_9'` | 48~57 |
| 空格 | `'K_SPACE'` | 32 |
| 回车 | `'K_RETURN'` / `'K_ENTER'` | 13 |
| 退格 | `'K_BACKSPACE'` | 8 |
| 删除 | `'K_DELETE'` | 127 |
| Esc | `'K_ESCAPE'` | 27 |
| Tab | `'K_TABLE'` | 9 |
| 上箭头 | `'K_UP'` | 1073741906 |
| 下箭头 | `'K_DOWN'` | 1073741905 |
| 左箭头 | `'K_LEFT'` | 1073741904 |
| 右箭头 | `'K_RIGHT'` | 1073741903 |
| F1~F12 | `'K_F1'` ~ `'K_F12'` | 282~293 |
| 左 Shift | `'K_LSHIFT'` | 1073742049 |
| 右 Shift | `'K_RSHIFT'` | 1073742049 |
| 左 Ctrl | `'K_LCTRL'` | 1073742048 |
| 右 Ctrl | `'K_RCTRL'` | 306 |
| 左 Alt | `'K_LALT'` | 307 |
| 右 Alt | `'K_RALT'` | 308 |
| Home | `'K_HOME'` | 1073741898 |
| End | `'K_END'` | 1073741901 |

---

*文档生成于 2025 年，基于 JSNgame v1.44_demo 源码。*
