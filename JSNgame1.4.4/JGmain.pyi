# THE LAST MAKING IN 25.8.31
# HELLO JSNgame 1.3.9
class JGerror(Exception):
    """自定义异常，标识JG专有的报错函数调用(25.7.28)"""
def wrong(e):
def Log(e: Exception) -> dict:
class Screen:
    """游戏屏幕管理类"""
    def __init__(self, size=(100,100), icon='./logo.bmp', title='NewGame', Full=False,size_change=False):
        """初始化游戏窗口"""
        self.size = size  # 窗口尺寸
        self.size_change = size_change  # 控制是否允许缩放的开关
        self.Full = Full
        # 缓存相关属性
        self.image_cache = {}
        self.font_cache = {}
        self.long_bg_cache = {}
        self.tile_size = 512
        self.engine = None
        self.models = {}
    def load(self):
        """更新屏幕显示（比例锁定）"""
    def third_D(self, file, plc=(0,0,0), jiaodu=(0,0,0), light=1.0):
        """渲染3D模型
        
        参数:
            file: 模型文件路径
            plc: 模型位置(x, y, z)，z控制远近
            jiaodu: 旋转角度(x, y, z)
            light: 亮度(0.0-1.0)
        """
    def blit(self, pto='./js.png', plc=(0,0), jd=0, mode='normal', big=None):
    def memory(self, fps=None):
    def fill(self, rgb=(255,255,255), mode='normal', glass=255):
        """填充屏幕背景
        
        参数:
            rgb: RGB颜色值
            mode: 填充模式 ('normal'普通/'glass'半透明)
            glass: 透明度 (0-255)
        """
    def vfill(self, rgb=(0,0,0), glass=255, mode='normal'):
        """高级填充方法 (支持特殊混合模式)
        
        参数:
            rgb: RGB颜色值
            glass: 透明度
            mode: 混合模式
        """    
    def speaking(self, word='...', plc=(0, 0), act=True, big=50,
                 word_rgb=(0, 0, 0), house_rgb=None, speed=0.1, GuDingDaXiao=False):
        """文字逐逐字显示效果 (类似对话效果)"""
    def speaking_with(self, word='...', plc=(0, 0), act=True, big=50,word_rgb=(0, 0, 0), house_rgb=None, speed=0.1, command=[[], []], GuDingDaXiao=False):
        """文字逐字显示 同时每出一个字就执行一次command里的命令"""
    def word(self, words='NEW_WORD', plc=(0, 0), rgb=(255, 255, 255), big=50,
             house_rgb=None, typeface=None, Anti_Aliasing=False, GuDingDaXiao=False):
        """在屏幕上绘制文字（豆包修复25.8.17）"""
    def ts(self, mode='begin', pto=None, rgb=(0,0,0), plc=None, finish_time=2,command=[[],[]]):
        """屏幕淡入淡出过渡效果
        
        参数:
            mode: 模式 ('begin'淡入/'end'淡出)
            pto: 背景图片路径
            rgb: 过渡颜色
            plc: 背景图片位置
            finish_time: 过渡总时间(秒)
        """
    def YinLiangTiao(self, Pos=(0,0), plc=[0,0], size=[100,10], 
                    rgb=[(0,255,0),(170,170,170),(255,255,255)], down=False,word='Volume'):
        """绘制音量控制条（带字体缓存）
        
        参数:
            Pos: 鼠标位置 (用于交互)
            plc: 控制条位置 [x, y]
            size: 控制条尺寸 [宽, 高]
            rgb: 颜色列表 [进度色, 背景色, 文字色]
            down: 是否检测鼠标点击
        """
    def TeXiao(self, name, strength, *args, **kwargs):
        """应用屏幕特效（使用NumPy优化）
        
        参数:
            name: ZhenDong、SeCha、BoWenSeCha 、GuangJiao 、MaSaiKe 、MoHu 、DongTaiMoHu
            strength: 特效强度
        """
    def draw(self, mode, plc=[], size=[], rgb=[[255, 255, 255], [0, 0, 0]]):
        """
        25.8.10新版绘图方法
        
        参数:
            mode (str): 绘图模式 ("Xian", "Yuan", "Fang", "Xin", "Dian")
            plc (list): 图形中心位置 [x, y]
            size (list): 图形尺寸 [x轴长度, y轴长度]
            rgb (list): 颜色设置 [[边框r, 边框g, 边框b], [填充r, 填充g, 填充b]]
        """
    def movie(self, file, plc=[0,0], speed=30.0, blit=True, rgb=None, replay=False):
        """
        播放视频文件(支持MP4/MKV/JMV)，带抠图功能和自动重置机制
        参数:
            file: 视频文件路径
            plc: 播放位置 [x, y]
            speed: 播放帧率(每秒帧数)
            blit: 是否将当前帧绘制到屏幕上
            rgb: 抠图颜色和阈值 [r, g, b, a]，None表示不抠图
            replay: 是否强制重置视频（默认False）
        """
    def TuoDongTiao(self, plc, size, rgb=((0,0,0),(255,0,0)), down=None, up=None, id="default"):
        """
        在屏幕上绘制可交互的拖动条组件（支持多个独立拖动条）
        
        参数:
            plc (list/tuple): 拖动条的位置 [x, y]
            size (list/tuple): 拖动条的尺寸 [宽度, 高度]
            rgb (tuple of tuples): 颜色设置 ((背景色R,G,B), (进度条色R,G,B))
                默认: 黑色背景((0,0,0)), 红色进度条((255,0,0))
            down (bool): 是否允许拖动 (通常传入鼠标按下状态)
                默认: None (自动检测鼠标左键按下状态)
            up (float/int): 强制设置的进度值 (0.0-1.0)
                默认: None (根据鼠标位置自动计算)
            id (str): 拖动条唯一标识符
                默认: "default" (当有多个拖动条时需指定不同id)
        
        返回值:
            float: 当前进度值 (0.0-1.0)
        
        使用示例:
            # 音量拖动条
            volume = screen.TuoDongTiao(
                [100, 100], 
                [200, 20],
                id="volume"
            )
        """
    def surface(self, plc=[0,0], size=[0,0], glass=False):
        """创建一个自定义Surface对象
        
        参数:
            plc: Surface在屏幕上的位置 [x, y]
            size: Surface的尺寸 [宽度, 高度]
            glass: 是否支持透明度（False或0-255的整数）
        
        返回:
            Surface实例
        """
        class Surface:
            def __init__(self, screen, plc, size, glass):
                self.screen = screen  # 父Screen实例
                self.plc = list(plc)  # 位置列表
                self.size = list(size)  # 尺寸列表
                self.glass = glass  # 透明度设置
            def fill(self, color):
                """填充颜色"""
            def blit(self, pto, plc=(0,0), jd=0, big=None):
                """绘制图像到Surface，支持加密图片(.jpt)"""
            def change(self, attr, value):
                """修改属性"""
            def TeXiao(self, mode, strength, *args, **kwargs):
                """应用特效（与Screen.TeXiao相同）"""
            def load(self):
                """将Surface绘制到屏幕上"""
        return Surface(self, plc, size, glass)
Event = {
    # ==================== 核心事件 ====================
    'QUIT': 0x100,             # 用户关闭窗口
    'ACTIVEEVENT': 1,          # 窗口激活/隐藏状态变化 (旧API)
    'KEYDOWN': 768,            # 键盘按键按下 (属性: key, mod, unicode)
    'KEYUP': 769,              # 键盘按键释放
    'MOUSEMOTION': 1024,'MOUSEMOVE': 1024,# 鼠标移动 (属性: pos, rel, buttons)
    'MOUSEBUTTONDOWN': 1025,   # 鼠标按键按下 (属性: pos, button: 左键=1, 右键=3)
    'MOUSEBUTTONUP': 1026,     # 鼠标按键释放
    'MOUSEWHEEL': 1027,        # 鼠标滚轮滚动 (Pygame 2.0+, 属性: x, y)
    
    # ==================== 窗口事件 ====================
    'VIDEORESIZE': 16,         # 窗口大小调整 (属性: size)
    'VIDEOEXPOSE': 17,         # 窗口需要重绘 (旧API)
    'WINDOWFOCUSGAINED': 18,   # 窗口获得焦点 (Pygame 2+)
    'WINDOWFOCUSLOST': 19,     # 窗口失去焦点 (Pygame 2+)
    
    # ==================== 用户与系统事件 ====================
    'USEREVENT': 24,           # 用户自定义事件起点
    'TEXTINPUT': 771,          # 文本输入事件 (属性: text)
    'TEXTEDITING': 770,        # 文本编辑事件 (如输入法预编辑)
    'DROPFILE': 4096,          # 文件拖放事件 (属性: file)
    
    # ==================== 游戏手柄事件 ====================
    'JOYAXISMOTION': 7,        # 手柄摇杆移动 (属性: instance_id, axis, value)
    'JOYBUTTONDOWN': 10,       # 手柄按键按下 (属性: instance_id, button)
    'JOYBUTTONUP': 11,         # 手柄按键释放
    
    # ==================== 键盘按键常量 ====================
    # 字母键
    'K_a': 97, 'K_b': 98, 'K_c': 99, 'K_d': 100, 'K_e': 101, 'K_f': 102,
    'K_g': 103, 'K_h': 104, 'K_i': 105, 'K_j': 106, 'K_k': 107, 'K_l': 108,
    'K_m': 109, 'K_n': 110, 'K_o': 111, 'K_p': 112, 'K_q': 113, 'K_r': 114,
    'K_s': 115, 'K_t': 116, 'K_u': 117, 'K_v': 118, 'K_w': 119, 'K_x': 120,
    'K_y': 121, 'K_z': 122,
    
    # 数字键
    'K_0': 48, 'K_1': 49, 'K_2': 50, 'K_3': 51, 'K_4': 52, 'K_5': 53,
    'K_6': 54, 'K_7': 55, 'K_8': 56, 'K_9': 57,
    
    # 功能键
    'K_ESCAPE': 27,            # Esc键
    'K_SPACE': 32,             # 空格键
    'K_RETURN': 13,            # 回车键
    'K_BACKSPACE': 8,          # 退格键
    'K_DELETE': 127,           # 删除键
    'K_END':1073741901,        # END键
    'K_HOME':1073741898,       # HOME键
    'K_TABLE':9,
    'K_F1': 282, 'K_F2': 283, 'K_F3': 284, 'K_F4': 285, 'K_F5': 286, 
    'K_F6': 287, 'K_F7': 288, 'K_F8': 289, 'K_F9': 290, 'K_F10': 291,
    'K_F11': 292, 'K_F12': 293,
    
    # 方向键
    'K_UP': 1073741906,    # 上箭头
    'K_DOWN': 1073741905,  # 下箭头
    'K_LEFT': 1073741904,  # 左箭头
    'K_RIGHT': 1073741903, # 右箭头
    
    # 修饰键
    'K_LSHIFT': 304, 'K_RSHIFT': 303,
    'K_LCTRL': 305, 'K_RCTRL': 306,
    'K_LALT': 307, 'K_RALT': 308,
}
class event2:
    def __init__(self):
        # 原有状态跟踪
        self.mouse_state = {1: False, 2: False, 3: False}
        self.key_state = {}
        self.wheel_state = {'vertical': 0, 'horizontal': 0, 'last_event': 0}
        # 鼠标跟踪
        self.pos = [0.0, 0.0]  # 存储为浮点数列表 [x, y]
        self.last_mouse_event_time = 0
        self.e = None
    def get(self):
        """获取当前事件队列并更新状态"""
    def updata(self):
        return self.get()
    def _update_states(self, e):
        """更新所有输入状态"""
    def get_pos(self, e=None):
        """获取当前鼠标位置
        参数:e: 事件对象 (可选，用于实时更新位置)
        返回:list: [x, y] 浮点数列表，无效时返回 [0.0, 0.0]
        """
    def mouse_down(self, e = None, FangXiang=1):
    def key_down(self, e= None, key= None):
    def test(self, e= None, event_type= None):     
    def test_key(self, e= None, key= None):   
    def test_key_UP(self, e = None, key= None):
    def button(self, e= None, size= None, plc= None):
event = event2()
class Xbox:
    def __init__(self):
        """初始化 Xbox 手柄管理器"""
        self.ctrls = []  # 存储所有 Xbox 手柄对象
        self.ids = []    # 存储所有 Xbox 手柄实例ID
        self.states = {} # 按 ID 存储手柄状态
    def get_id(self):
        """获取所有手柄实例ID列表"""
    def get_name(self, id=None):
        """获取指定手柄的名称"""
    def _get_joy(self, id=None):
        """获取指定ID的手柄对象"""
    def get_event(self, id=None, dead_area=0):
        """
        获取手柄的完整当前状态
        :param id: 手柄实例ID, 默认使用第一个手柄
        :param dead_area: 摇杆死区 (0-10)
        :return: 手柄状态字典 {
            "LS": (x,y,pressed),
            "RS": (x,y,pressed),
            "ABXY": {"a":bool, "b":bool, "y":bool, "z":bool},
            ...
        }
        """
    def event_get(self, pg_event, id=None, dead_area=0):
        """
        处理单个手柄事件
        :param pg_event: pygame 事件对象
        :param id: 手柄实例ID, 默认使用第一个手柄
        :param dead_area: 摇杆死区 (0-10)
        :return: 更新后的手柄状态字典
        """
class mixer:
    """音频管理系统（带音效缓存和立体声定位）"""
    
    def __init__(self):
        self.sound_cache = {}  # 音效缓存
        self.mic_stream = None  # 麦克风流对象
        self.mic_data = {"YinLiang": 0.0, "YinDiao": 0.0}  # 麦克风数据存储
        self.p = None  # PyAudio实例
        self.pa = None  # 存储pyaudio模块
        self.last_audio_data = None  # 存储最后音频数据
        self.bgm_start_time = 0  # 记录BGM的起始播放时间
        self.bgm_play_start_time = 0  # 记录BGM开始播放的系统时间
        self.YINLIANG = 0.5
        self.file = None
    def bgm(self, file, sound_bigs=None, times=-1, start=None):
        """播放背景音乐
        
        参数:
            file: 音频文件路径 (支持.jmus加密格式)
            sound_bigs: 音量大小 (0.0-1.0)
            times: 循环次数 (-1为无限循环)
            start: 起始播放时间(秒)，默认0
        """
    def sound(self, file, sound_bigs=None, plc=0):
        """播放音效（带立体声定位）
        
        参数:
            file: 音频文件路径 (支持.jmus加密格式)
            sound_bigs: 音量大小 (0.0-1.0)
            plc: 立体声定位 (-90~90)
                -90: 完全左声道 (右声道静音)
                 0: 左右声道平衡 (默认)
                90: 完全右声道 (左声道静音)
        
        返回:
            _Sound对象，可单独控制该音效
        """
    class _Sound:
        """音效控制对象（支持立体声定位）"""
        def __init__(self, sound, channel, file, sound_bigs, plc):
            """
            初始化音效控制对象
            
            参数:
                sound: pygame.Sound对象
                channel: 播放通道对象
                file: 音频文件路径
                sound_bigs: 初始音量大小 (0.0-1.0)
                plc: 立体声定位 (-90~90)
            """
            self.sound = sound
            self.channel = channel
            self.file = file
            self.sound_bigs = sound_bigs  # 存储当前音量
            self.plc = plc  # 存储当前立体声定位
            self.valid = True  # 对象有效性标志
        
        def yinliang(self, volume):
            """设置当前音效的音量（不影响立体声比例）
            
            参数:
                volume: 音量大小 (0.0-1.0)
            """
        def _update_volume(self):
            """内部方法：根据当前音量和plc更新声道音量"""
        def set_plc(self, plc):
            """设置立体声定位
            
            参数:
                plc: 立体声定位 (-90~90)
            """
        def stop(self):
            """停止播放但不释放内存"""
        def clean(self):
            """清理缓存使对象失效"""
        def re_play(self):
            """重新播放音效"""
        def stop_bgm(self, *args, **kwargs):
        """停止背景音乐"""
    def stop_all(self, *args, **kwargs):
        """停止所有音频"""
    def volume(self, volume):
        """设置全局音量
        
        参数:
            volume: 音量值 (0.0-1.0)
        """
    def yinliang(self, big):
        """音量设置别名方法 (中文: 音量)"""
    def get_volume(self, *args, **kwargs):
        """获取当前音量"""
    def get_yinliang(self, *args, **kwargs):
        """获取音量别名方法 (中文: 音量)"""
    def open_mkf(self):
        """打开麦克风并开始实时更新数据"""
    def get_mkf(self):
        """获取麦克风数据（包括音调检测）"""
    def close_mkf(self):
        """关闭麦克风并释放资源"""
class Word:
    """文本处理工具类"""
    def check_language(self, text):
        """检测文本的主要语言
        
        参数:
            text: 输入文本
        返回:
            str: 语言类型 ('Chinese'/'English'/'Russian'/'Mixed or other')
        """
    def entry(self, Screen, plc=(0,0), bg_color=(255,255,255), big=(100,50,400), plc_pos=(0,0)):
        """创建文本输入框
        
        参数:
            Screen: 屏幕对象
            plc: 输入框位置
            bg_color: 背景颜色
            big: 尺寸参数 (y位置, 高度, 宽度)
            plc_pos: 鼠标位置 (用于检测激活)
        返回:
            tuple: (文本表面对象, 是否激活状态)
        """
    def FenGe(self, word, FenGe=" "):
        """分割字符串
        
        参数:
            word: 要分割的字符串
            FenGe: 分隔符，默认为空格
            
        返回:
            list: 分割后的字符串列表
        """
class Time:
    """时间管理类（FPS控制）"""
    def __init__(self):
        self.clock = pg.time.Clock()
        self.clock.tick()
    def FPS(self, fps=None):
        """控制帧率"""
    def get_FPS(self):
        """获取当前帧率"""
    def get_time():
        '''获取精准时间'''
        return {'年': , '月': , '日': ,'时': , '分': , '秒': ,'总和': }
class Random:
    def __init__(self):
    def int(self, a, b):
    def float(self, a, b):
    def DaLuan(self, a):
    def QiePian(self, a, b):
    def choose(self, a):
    def MiYao(self, length, binary=True):
class IT:
    def __init__(self):
    def open_www(address, tag=0, autoraise=True):
    def SouSuo(question, deep=5):
class PengZhuangXiang:
    """碰撞箱管理系统"""
    def __init__(self,screen=None):
        self._boxes = []  # 存储所有碰撞箱实例
        self._screen = screen  # 用于存储screen引用
    def set_screen(self, screen):
        """设置screen对象用于绘制"""
    def add(self, plc=[0, 0], size=[100, 100], mode="Fang"):
        """添加新的碰撞箱并返回实例"""
    def remove(self, box):
        """批量删除碰撞箱"""
    def test(self, box1, box2):
        """检测两个碰撞箱之间的碰撞"""
    def show(self):
        """绘制所有碰撞箱"""
class _Box:
    """碰撞箱实例"""
    def __init__(self, plc, size, mode, manager):
        self._plc = list(plc)
        self._size = list(size)
        self._mode = mode
        self._manager = manager
        self._colliding = False
    def change(self, attr, value):
        """更改属性"""
    def remove(self):
        """从管理器中移除自身"""
    def show(self):
        """绘制碰撞箱"""
    def test(self, other):
        """返回当前碰撞箱与另一个碰撞箱的移动向量 [x, y]，用于碰撞反应。
        如果没有碰撞，返回 [0.0, 0.0]。
        """
def Exit():
    """安全退出游戏"""
print('JG:Everything prepared')








