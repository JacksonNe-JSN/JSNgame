"""
JG.check - JSNgame 库完整性检查系统
版本: 1.0.0
作者: JSN
创建日期: 2025-09-12
描述: 全面检查 JSNgame 库的功能完整性、兼容性、性能和质量
"""

import sys
import os
import platform
import time
import datetime
import subprocess
import json
import traceback
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import inspect
import hashlib
import tempfile

# ===================== 配置部分 =====================
class CheckConfig:
    """检查配置"""
    def __init__(self):
        self.library_path = None  # 库路径
        self.test_data_path = "./try_img"  # 测试数据路径
        self.log_file = "./JG_check_report.json"  # 日志文件
        self.verbose = True  # 详细输出
        self.interactive_mode = True  # 交互模式
        self.timeout_duration = 30  # 单次测试超时时间(秒)
        self.check_level = "comprehensive"  # 检查级别: basic/standard/comprehensive
        
        # 测试文件
        self.test_files = {
            "image": ["little_python_logo.png", "python_logo.png"],
            "encrypted_image": ["j1.jpt"],
            "audio": ["j1.mp3"],
            "encrypted_audio": ["j1.jmus"],
            "video": ["mp4.mp4"],
            "encrypted_video": ["j1.jmv"]  # 假设有这个文件
        }
        
        # 评分标准
        self.scoring_weights = {
            "core": 0.25,
            "graphics": 0.20,
            "audio": 0.15,
            "ai": 0.15,
            "compatibility": 0.10,
            "performance": 0.10,
            "documentation": 0.05
        }

# ===================== 工具函数 =====================
class CheckUtils:
    """检查工具类"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """获取系统信息"""
        info = {
            "platform": platform.platform(),
            "python_version": sys.version,
            "python_executable": sys.executable,
            "processor": platform.processor(),
            "architecture": platform.architecture(),
            "machine": platform.machine(),
            "node": platform.node(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "cpu_count": os.cpu_count(),
            "memory": None  # 可通过 psutil 获取，这里简化
        }
        return info
    
    @staticmethod
    def calculate_md5(file_path: str) -> str:
        """计算文件MD5"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """格式化时间"""
        if seconds < 1:
            return f"{seconds*1000:.1f}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        else:
            mins = seconds // 60
            secs = seconds % 60
            return f"{int(mins)}m {secs:.1f}s"
    
    @staticmethod
    def check_file_exists(file_path: str) -> Tuple[bool, str, Optional[int]]:
        """检查文件是否存在及其信息"""
        try:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                return True, f"存在 ({size/1024:.1f}KB)", size
            return False, "不存在", None
        except Exception as e:
            return False, f"检查失败: {str(e)}", None

# ===================== 检查基类 =====================
class CheckItem:
    """检查项基类"""
    
    def __init__(self, name: str, category: str, weight: float = 1.0):
        self.name = name
        self.category = category
        self.weight = weight
        self.start_time = None
        self.end_time = None
        self.duration = 0
        self.result = None
        self.score = 0
        self.details = {}
        self.errors = []
        self.warnings = []
        self.suggestions = []
        
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """运行检查"""
        self.start_time = time.time()
        
        try:
            self._execute(context)
            self.result = "PASS" if self.score >= 7 else "FAIL"
        except Exception as e:
            self.result = "ERROR"
            self.errors.append(f"检查过程中发生异常: {str(e)}")
            if context.get("verbose", False):
                self.errors.append(traceback.format_exc())
        finally:
            self.end_time = time.time()
            self.duration = self.end_time - self.start_time
            
        return self._get_report()
    
    def _execute(self, context: Dict[str, Any]):
        """执行具体检查（子类实现）"""
        raise NotImplementedError
    
    def _get_report(self) -> Dict[str, Any]:
        """获取检查报告"""
        return {
            "name": self.name,
            "category": self.category,
            "result": self.result,
            "score": self.score,
            "duration": self.duration,
            "details": self.details,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions
        }
    
    def _add_error(self, error: str):
        """添加错误"""
        self.errors.append(error)
        self.score = max(0, self.score - 2)  # 错误扣分
        
    def _add_warning(self, warning: str):
        """添加警告"""
        self.warnings.append(warning)
        self.score = max(0, self.score - 0.5)  # 警告扣分
        
    def _add_suggestion(self, suggestion: str):
        """添加建议"""
        self.suggestions.append(suggestion)
        
    def _user_score(self, prompt: str, min_score: int = 0, max_score: int = 10) -> int:
        """获取用户评分"""
        if not self._context.get("interactive_mode", True):
            return 8  # 非交互模式默认评分
            
        try:
            print(f"\n{'='*60}")
            print(f"用户评分: {self.name}")
            print(f"描述: {prompt}")
            print(f"请观察程序显示的效果，然后评分 ({min_score}-{max_score}分)")
            print("="*60)
            
            while True:
                try:
                    score = int(input(f"请输入评分 ({min_score}-{max_score}): "))
                    if min_score <= score <= max_score:
                        return score
                    else:
                        print(f"评分必须在 {min_score} 到 {max_score} 之间")
                except ValueError:
                    print("请输入有效的数字")
        except KeyboardInterrupt:
            print("\n用户中断评分，使用默认评分")
            return 7
        except Exception:
            return 7

# ===================== 具体检查项 =====================

class ModuleImportCheck(CheckItem):
    """模块导入检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10  # 初始分数
        
        # 尝试导入JSNgame
        try:
            import LIBbase.JSNgame as jg
            self.details["import_success"] = True
            self.details["version"] = getattr(jg, "__version__", "未知")
            
            # 检查所有公开的模块和类
            if hasattr(jg, "__all__"):
                missing = []
                for item in jg.__all__:
                    try:
                        getattr(jg, item)
                    except AttributeError:
                        missing.append(item)
                
                if missing:
                    self._add_warning(f"__all__中声明的以下项无法导入: {', '.join(missing)}")
                else:
                    self.details["all_items_available"] = True
                    
            # 存储模块引用到上下文
            context["jg_module"] = jg
            
        except ImportError as e:
            self._add_error(f"无法导入JSNgame库: {str(e)}")
            self.score = 0
        except Exception as e:
            self._add_error(f"导入过程中发生错误: {str(e)}")
            self.score = 5

class CoreFunctionsCheck(CheckItem):
    """核心函数检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        # 检查关键函数
        key_functions = [
            "init", "wrong", "Log", "Exit", "exit", "Key", "creat_easy"
        ]
        
        for func_name in key_functions:
            if hasattr(jg, func_name):
                func = getattr(jg, func_name)
                self.details[f"function_{func_name}"] = {
                    "exists": True,
                    "type": type(func).__name__,
                    "callable": callable(func)
                }
            else:
                self._add_warning(f"关键函数 {func_name} 不存在")
                
        # 检查自定义异常
        if hasattr(jg, "JGerror"):
            try:
                raise jg.JGerror("测试异常")
                self.details["JGerror_works"] = True
            except jg.JGerror:
                self.details["JGerror_works"] = True
            except Exception as e:
                self._add_warning(f"JGerror异常测试失败: {str(e)}")
                
        # 检查初始化函数
        try:
            jg.init()
            self.details["init_success"] = True
        except Exception as e:
            self._add_error(f"init()函数执行失败: {str(e)}")

class ScreenClassCheck(CheckItem):
    """Screen类检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        # 检查Screen类存在
        if not hasattr(jg, "Screen"):
            self._add_error("Screen类不存在")
            return
            
        ScreenClass = jg.Screen
        
        # 测试创建屏幕
        try:
            screen = ScreenClass(size=(800, 600), title="JG.check - Screen测试")
            self.details["screen_creation"] = "成功"
            
            # 测试基本方法
            test_methods = [
                ("fill", [(255, 0, 0)], {}),  # 填充红色
                ("load", [], {}),  # 加载屏幕
            ]
            
            for method_name, args, kwargs in test_methods:
                if hasattr(screen, method_name):
                    try:
                        method = getattr(screen, method_name)
                        method(*args, **kwargs)
                        self.details[f"method_{method_name}"] = "成功"
                    except Exception as e:
                        self._add_warning(f"方法 {method_name} 执行失败: {str(e)}")
                else:
                    self._add_warning(f"方法 {method_name} 不存在")
                    
            # 用户评分：基本渲染
            prompt = "请观察屏幕是否成功显示红色背景"
            score = self._user_score(prompt)
            self.details["user_score_basic"] = score
            self.score = (self.score * 0.7) + (score * 0.3)
            
            # 测试图像渲染
            test_image = os.path.join(context["test_data_path"], "little_python_logo.png")
            if os.path.exists(test_image):
                try:
                    screen.blit(test_image, (100, 100))
                    screen.load()
                    self.details["image_blit"] = "成功"
                    
                    # 用户评分：图像渲染
                    prompt = "请观察屏幕是否成功显示Python logo图像"
                    score = self._user_score(prompt)
                    self.details["user_score_image"] = score
                    self.score = (self.score * 0.7) + (score * 0.3)
                except Exception as e:
                    self._add_warning(f"图像渲染失败: {str(e)}")
                    
            # 测试文字渲染
            try:
                screen.word("JG.check 测试文字", (200, 200), big=30, rgb=(255, 255, 255))
                screen.load()
                self.details["text_rendering"] = "成功"
                
                # 用户评分：文字渲染
                prompt = "请观察屏幕是否成功显示白色测试文字"
                score = self._user_score(prompt)
                self.details["user_score_text"] = score
                self.score = (self.score * 0.7) + (score * 0.3)
            except Exception as e:
                self._add_warning(f"文字渲染失败: {str(e)}")
                
            # 测试图形绘制
            try:
                screen.draw("Fang", plc=(400, 300), size=[100, 50], 
                           rgb=[[0, 255, 0], [0, 100, 0]])
                screen.load()
                self.details["shape_drawing"] = "成功"
            except Exception as e:
                self._add_warning(f"图形绘制失败: {str(e)}")
                
            # 测试特效
            try:
                screen.TeXiao("MoHu", 50)
                screen.load()
                self.details["effect_blur"] = "成功"
            except Exception as e:
                self._add_warning(f"模糊特效失败: {str(e)}")
                
            # 测试视频播放（如果有）
            test_video = os.path.join(context["test_data_path"], "mp4.mp4")
            if os.path.exists(test_video):
                try:
                    frame = screen.movie(test_video, [300, 300], speed=30, blit=True)
                    if frame is not None:
                        self.details["video_playback"] = f"成功 (帧: {frame})"
                    else:
                        self.details["video_playback"] = "失败 (返回None)"
                except Exception as e:
                    self._add_warning(f"视频播放失败: {str(e)}")
                    
            # 清理
            try:
                import pygame
                pygame.quit()
            except:
                pass
                
        except Exception as e:
            self._add_error(f"Screen类测试失败: {str(e)}")

class EventSystemCheck(CheckItem):
    """事件系统检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        # 检查事件常量
        if hasattr(jg, "Event"):
            event_dict = jg.Event
            self.details["event_constants_count"] = len(event_dict)
            
            # 检查关键事件常量
            key_events = ["QUIT", "KEYDOWN", "KEYUP", "MOUSEMOTION", "MOUSEBUTTONDOWN"]
            missing = [e for e in key_events if e not in event_dict]
            if missing:
                self._add_warning(f"缺少关键事件常量: {', '.join(missing)}")
            else:
                self.details["key_events_present"] = True
                
        # 检查事件实例
        if hasattr(jg, "event"):
            event_instance = jg.event
            self.details["event_instance_type"] = type(event_instance).__name__
            
            # 测试事件方法
            test_methods = ["get", "get_pos", "mouse_down", "key_down", "test"]
            
            for method_name in test_methods:
                if hasattr(event_instance, method_name):
                    self.details[f"event_method_{method_name}"] = "存在"
                else:
                    self._add_warning(f"事件方法 {method_name} 不存在")
        else:
            self._add_error("全局event实例不存在")

class AudioSystemCheck(CheckItem):
    """音频系统检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        # 检查mixer类
        if not hasattr(jg, "mixer"):
            self._add_error("mixer类不存在")
            return
            
        # 测试基本音频功能
        try:
            mixer = jg.mixer()
            self.details["mixer_creation"] = "成功"
            
            # 测试音频文件播放
            test_audio = os.path.join(context["test_data_path"], "j1.mp3")
            if os.path.exists(test_audio):
                try:
                    # 设置音量
                    mixer.volume(0.3)
                    self.details["volume_set"] = "成功"
                    
                    # 播放背景音乐
                    mixer.bgm(test_audio, sound_bigs=0.5)
                    self.details["bgm_playback"] = "成功"
                    
                    # 停止音乐
                    time.sleep(1)  # 播放1秒
                    mixer.stop_bgm()
                    self.details["bgm_stop"] = "成功"
                    
                    # 测试音效
                    sound = mixer.sound(test_audio, sound_bigs=0.5, plc=0)
                    if sound:
                        self.details["sound_playback"] = "成功"
                        sound.clean()  # 清理
                        
                except Exception as e:
                    self._add_warning(f"音频播放测试失败: {str(e)}")
                    
            # 测试加密音频
            test_encrypted = os.path.join(context["test_data_path"], "j1.jmus")
            if os.path.exists(test_encrypted):
                try:
                    mixer.bgm(test_encrypted, sound_bigs=0.3)
                    time.sleep(1)
                    mixer.stop_bgm()
                    self.details["encrypted_audio"] = "成功"
                except Exception as e:
                    self._add_warning(f"加密音频播放失败: {str(e)}")
                    
        except Exception as e:
            self._add_error(f"音频系统测试失败: {str(e)}")

class AIClassCheck(CheckItem):
    """AI类检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        # 检查AI_tree模块
        try:
            from LIBbase.JSNgame.AI_tree import Game_AI, find_road
            self.details["ai_import"] = "成功"
            
            # 测试基本寻路
            ai = Game_AI()
            
            # 简单测试场景
            start = [0, 0]
            end = [5, 5]
            obstacles = [[1, 1], [1, 2], [2, 1], [3, 3], [4, 4]]
            
            # 测试寻路
            try:
                move = ai.find_road(start, end, obstacles, difficult=2, mode=1)
                if move is not None:
                    self.details["basic_pathfinding"] = f"成功 (移动: {move})"
                else:
                    self.details["basic_pathfinding"] = "返回None"
            except Exception as e:
                self._add_warning(f"基本寻路失败: {str(e)}")
                
            # 测试高级寻路
            try:
                # 创建更复杂的障碍
                complex_obstacles = []
                for x in range(10):
                    for y in range(10):
                        if (x + y) % 3 == 0:
                            complex_obstacles.append([x, y])
                            
                move = ai.find_road([0, 0], [9, 9], complex_obstacles, difficult=4, mode=1)
                if move is not None:
                    self.details["advanced_pathfinding"] = f"成功"
                else:
                    self.details["advanced_pathfinding"] = "可能无解"
            except Exception as e:
                self._add_warning(f"高级寻路失败: {str(e)}")
                
            # 测试世界地图模式
            try:
                world = [
                    ['air', 'wall', 'air', 'air'],
                    ['air', 'wall', 'air', 'wall'],
                    ['air', 'air', 'air', 'wall'],
                    ['wall', 'wall', 'air', 'air']
                ]
                move = ai.find_road(ai_mode="world", world=world, difficult=2)
                if move is not None:
                    self.details["world_map_pathfinding"] = "成功"
            except Exception as e:
                self._add_warning(f"世界地图寻路失败: {str(e)}")
                
        except ImportError as e:
            self._add_error(f"无法导入AI模块: {str(e)}")
        except Exception as e:
            self._add_error(f"AI测试失败: {str(e)}")

class CollisionDetectionCheck(CheckItem):
    """碰撞检测检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        # 检查PengZhuangXiang类
        if not hasattr(jg, "PengZhuangXiang"):
            self._add_error("PengZhuangXiang类不存在")
            return
            
        try:
            # 创建碰撞检测系统
            pzx = jg.PengZhuangXiang()
            self.details["collision_system"] = "创建成功"
            
            # 创建两个矩形碰撞箱
            box1 = pzx.add(plc=[100, 100], size=[50, 50], mode="Fang")
            box2 = pzx.add(plc=[130, 130], size=[50, 50], mode="Fang")
            
            # 测试碰撞检测
            collision_result = pzx.test(box1, box2)
            if collision_result:
                self.details["collision_detection"] = f"成功 (结果: {collision_result})"
            else:
                self.details["collision_detection"] = "未检测到碰撞"
                
            # 移动碰撞箱使其分离
            box2.plc = [200, 200]
            collision_result = pzx.test(box1, box2)
            if not collision_result:
                self.details["non_collision"] = "成功 (正确检测无碰撞)"
                
            # 测试圆形碰撞
            circle1 = pzx.add(plc=[300, 300], size=[40, 40], mode="round")
            circle2 = pzx.add(plc=[330, 330], size=[40, 40], mode="round")
            
            collision_result = pzx.test(circle1, circle2)
            if collision_result:
                self.details["circle_collision"] = "成功"
                
            # 清理
            pzx.remove(box1)
            pzx.remove(box2)
            pzx.remove(circle1)
            pzx.remove(circle2)
            
        except Exception as e:
            self._add_error(f"碰撞检测测试失败: {str(e)}")

class EncryptionDecryptionCheck(CheckItem):
    """加密解密功能检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        test_data_path = context["test_data_path"]
        utils = CheckUtils()
        
        # 检查加密解密函数
        decrypt_funcs = ["image_bytes", "music_bytes", "video_bytes"]
        encrypt_funcs = ["image_bytes", "music_bytes", "video_bytes"]
        
        for func_name in decrypt_funcs:
            if hasattr(jg, func_name):
                self.details[f"decrypt_{func_name}"] = "存在"
            else:
                self._add_warning(f"解密函数 {func_name} 不存在")
                
        # 测试图像加密解密
        test_image = os.path.join(test_data_path, "little_python_logo.png")
        test_encrypted = os.path.join(test_data_path, "j1.jpt")
        
        if os.path.exists(test_image) and os.path.exists(test_encrypted):
            try:
                # 计算原始文件MD5
                original_md5 = utils.calculate_md5(test_image)
                
                # 测试解密（如果有解密函数）
                if hasattr(jg, "image_bytes"):
                    # 这里简化测试，实际需要完整的加密解密流程
                    self.details["image_decryption_test"] = "跳过（需要完整流程）"
                    
            except Exception as e:
                self._add_warning(f"加密解密测试失败: {str(e)}")
                
        # 测试音频加密解密
        test_audio = os.path.join(test_data_path, "j1.mp3")
        test_encrypted_audio = os.path.join(test_data_path, "j1.jmus")
        
        if os.path.exists(test_audio) and os.path.exists(test_encrypted_audio):
            self.details["audio_files_exist"] = "是"
            
        # 检查JSNrt模块
        try:
            from JSN import JSNrt
            self.details["JSNrt_module"] = "可导入"
        except ImportError as e:
            self._add_warning(f"无法导入JSNrt模块: {str(e)}")

class CompatibilityCheck(CheckItem):
    """兼容性检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        # 检查Python版本兼容性
        python_version = sys.version_info
        self.details["python_version"] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
        
        if python_version.major == 3 and python_version.minor >= 7:
            self.details["python_compatibility"] = "良好 (Python 3.7+)"
        else:
            self._add_warning("建议使用Python 3.7或更高版本")
            
        # 检查操作系统
        system = platform.system()
        self.details["operating_system"] = system
        
        if system in ["Windows", "Linux", "Darwin"]:
            self.details["os_compatibility"] = "支持"
        else:
            self._add_warning(f"未在 {system} 系统上充分测试")
            
        # 检查关键依赖
        dependencies = {
            "pygame": "游戏渲染和音频",
            "numpy": "图像处理和AI计算",
            "opencv-python": "视频处理",
            "tkinter": "消息对话框"
        }
        
        missing_deps = []
        for dep, purpose in dependencies.items():
            try:
                __import__(dep.replace("-", ""))
                self.details[f"dep_{dep}"] = "已安装"
            except ImportError:
                missing_deps.append(f"{dep} ({purpose})")
                self.details[f"dep_{dep}"] = "未安装"
                
        if missing_deps:
            self._add_warning(f"缺少依赖: {', '.join(missing_deps)}")
            self.score -= len(missing_deps) * 0.5
            
        # 检查文件编码
        try:
            with open(__file__, "r", encoding="utf-8") as f:
                f.read()
            self.details["utf8_encoding"] = "支持"
        except UnicodeDecodeError:
            self._add_warning("文件编码可能不是UTF-8")

class PerformanceCheck(CheckItem):
    """性能检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        
        # 测试导入速度
        start_time = time.time()
        try:
            import LIBbase.JSNgame as jg
            import_time = time.time() - start_time
            self.details["import_time"] = f"{import_time:.3f}s"
            
            if import_time < 1.0:
                self.details["import_performance"] = "优秀"
            elif import_time < 3.0:
                self.details["import_performance"] = "良好"
                self.score -= 1
            else:
                self.details["import_performance"] = "较慢"
                self._add_suggestion("考虑延迟导入或优化初始化")
                self.score -= 2
                
        except Exception as e:
            self._add_error(f"性能测试导入失败: {str(e)}")
            
        # 内存使用测试（简化版）
        import psutil
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # 执行一些操作测试内存
        try:
            if jg:
                # 创建多个对象测试内存
                screens = []
                for i in range(5):
                    try:
                        screen = jg.Screen(size=(100, 100), title=f"Test{i}")
                        screens.append(screen)
                    except:
                        break
                        
                memory_during = process.memory_info().rss / 1024 / 1024
                memory_increase = memory_during - memory_before
                
                self.details["memory_usage"] = f"{memory_increase:.1f}MB 增加"
                
                if memory_increase < 50:
                    self.details["memory_performance"] = "良好"
                elif memory_increase < 100:
                    self.details["memory_performance"] = "中等"
                    self.score -= 1
                else:
                    self.details["memory_performance"] = "较高"
                    self._add_suggestion("检查内存泄漏")
                    self.score -= 2
                    
                # 清理
                del screens
                
        except Exception as e:
            self.details["memory_test"] = f"跳过: {str(e)}"

class DocumentationCheck(CheckItem):
    """文档检查"""
    
    def _execute(self, context: Dict[str, Any]):
        self.score = 10
        jg = context.get("jg_module")
        
        if not jg:
            self._add_error("JSNgame模块未加载")
            return
            
        # 检查docstring
        classes_to_check = ["Screen", "mixer", "PengZhuangXiang", "Game_AI"]
        
        documented_classes = 0
        for class_name in classes_to_check:
            if hasattr(jg, class_name):
                cls = getattr(jg, class_name)
                doc = cls.__doc__
                if doc and len(doc.strip()) > 50:  # 假设有意义的文档至少50字符
                    documented_classes += 1
                    self.details[f"doc_{class_name}"] = "有文档"
                else:
                    self.details[f"doc_{class_name}"] = "文档不足"
                    self._add_suggestion(f"为 {class_name} 类添加更多文档")
            else:
                self.details[f"doc_{class_name}"] = "类不存在"
                
        documentation_rate = documented_classes / len(classes_to_check)
        self.details["documentation_rate"] = f"{documentation_rate*100:.0f}%"
        
        if documentation_rate >= 0.8:
            self.details["documentation_quality"] = "良好"
        elif documentation_rate >= 0.5:
            self.details["documentation_quality"] = "中等"
            self.score -= 1
        else:
            self.details["documentation_quality"] = "不足"
            self._add_suggestion("请为更多类和方法添加文档字符串")
            self.score -= 2
            
        # 检查函数签名
        try:
            import inspect
            # 检查Screen.__init__的签名
            if hasattr(jg, "Screen"):
                sig = inspect.signature(jg.Screen.__init__)
                params = len(sig.parameters)
                self.details["screen_init_params"] = params
                
                if params >= 5:  # 假设有多个参数
                    self.details["api_design"] = "详细"
                else:
                    self.details["api_design"] = "简单"
        except Exception:
            self.details["signature_check"] = "跳过"

# ===================== 检查管理器 =====================
class CheckManager:
    """检查管理器"""
    
    def __init__(self, config: CheckConfig):
        self.config = config
        self.results = []
        self.summary = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "total_score": 0,
            "weighted_score": 0,
            "start_time": None,
            "end_time": None,
            "duration": None
        }
        self.context = {
            "verbose": config.verbose,
            "interactive_mode": config.interactive_mode,
            "test_data_path": config.test_data_path,
            "jg_module": None
        }
        
    def run_all_checks(self):
        """运行所有检查"""
        print("="*80)
        print("JSNgame 库完整性检查系统")
        print(f"开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        self.summary["start_time"] = time.time()
        
        # 定义检查项
        checks = [
            ModuleImportCheck("模块导入", "core", 1.0),
            CoreFunctionsCheck("核心函数", "core", 1.0),
            ScreenClassCheck("屏幕渲染", "graphics", 1.5),
            EventSystemCheck("事件系统", "core", 1.0),
            AudioSystemCheck("音频系统", "audio", 1.2),
            AIClassCheck("AI寻路系统", "ai", 1.3),
            CollisionDetectionCheck("碰撞检测", "graphics", 1.0),
            EncryptionDecryptionCheck("加密解密", "core", 0.8),
            CompatibilityCheck("兼容性", "compatibility", 1.0),
            PerformanceCheck("性能", "performance", 1.0),
            DocumentationCheck("文档", "documentation", 0.8)
        ]
        
        self.summary["total_tests"] = len(checks)
        
        # 运行检查
        for i, check in enumerate(checks, 1):
            print(f"\n[{i}/{len(checks)}] 运行检查: {check.name}")
            print("-"*60)
            
            try:
                result = check.run(self.context)
                self.results.append(result)
                
                # 更新上下文中的模块引用
                if check.name == "模块导入" and result.get("details", {}).get("import_success"):
                    # 模块导入检查成功后，jg_module应该已经在上下文中
                    pass
                    
                # 更新统计
                if result["result"] == "PASS":
                    self.summary["passed"] += 1
                elif result["result"] == "FAIL":
                    self.summary["failed"] += 1
                else:
                    self.summary["errors"] += 1
                    
                self.summary["total_score"] += result["score"]
                
                # 显示结果
                print(f"结果: {result['result']}")
                print(f"分数: {result['score']}/10")
                print(f"耗时: {CheckUtils.format_duration(result['duration'])}")
                
                if result["errors"]:
                    print(f"错误: {len(result['errors'])} 个")
                    for error in result["errors"][:3]:  # 只显示前3个错误
                        print(f"  - {error}")
                        
                if result["warnings"]:
                    print(f"警告: {len(result['warnings'])} 个")
                    for warning in result["warnings"][:3]:
                        print(f"  - {warning}")
                        
            except KeyboardInterrupt:
                print("\n检查被用户中断")
                break
            except Exception as e:
                print(f"检查执行失败: {str(e)}")
                
        # 计算加权分数
        category_scores = {}
        category_weights = self.config.scoring_weights
        
        for result in self.results:
            category = result["category"]
            if category not in category_scores:
                category_scores[category] = []
            category_scores[category].append(result["score"])
            
        for category, scores in category_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                weight = category_weights.get(category, 1.0)
                self.summary["weighted_score"] += avg_score * weight
                
        # 完成时间
        self.summary["end_time"] = time.time()
        self.summary["duration"] = self.summary["end_time"] - self.summary["start_time"]
        
        # 生成报告
        self._generate_report()
        
    def _generate_report(self):
        """生成详细报告"""
        print("\n" + "="*80)
        print("检查完成")
        print("="*80)
        
        # 基本统计
        print(f"\n统计信息:")
        print(f"  总检查项: {self.summary['total_tests']}")
        print(f"  通过: {self.summary['passed']}")
        print(f"  失败: {self.summary['failed']}")
        print(f"  错误: {self.summary['errors']}")
        print(f"  总耗时: {CheckUtils.format_duration(self.summary['duration'])}")
        
        # 分数
        avg_score = self.summary['total_score'] / max(1, self.summary['total_tests'])
        print(f"  平均分数: {avg_score:.1f}/10")
        print(f"  加权分数: {self.summary['weighted_score']:.1f}/10")
        
        # 评级
        if avg_score >= 9:
            rating = "★★★★★ 优秀"
        elif avg_score >= 8:
            rating = "★★★★☆ 良好"
        elif avg_score >= 7:
            rating = "★★★☆☆ 中等"
        elif avg_score >= 6:
            rating = "★★☆☆☆ 及格"
        else:
            rating = "★☆☆☆☆ 需要改进"
            
        print(f"  总体评级: {rating}")
        
        # 详细结果
        print(f"\n详细结果:")
        for result in self.results:
            symbol = "✓" if result["result"] == "PASS" else "✗" if result["result"] == "FAIL" else "!"
            print(f"  {symbol} {result['name']}: {result['score']}/10 ({result['result']})")
            
        # 保存报告到文件
        self._save_report()
        
    def _save_report(self):
        """保存报告到文件"""
        report = {
            "metadata": {
                "tool": "JG.check",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now().isoformat(),
                "duration": self.summary["duration"],
                "system": CheckUtils.get_system_info()
            },
            "summary": self.summary,
            "results": self.results,
            "config": {
                "library_path": self.config.library_path,
                "test_data_path": self.config.test_data_path,
                "check_level": self.config.check_level
            }
        }
        
        try:
            with open(self.config.log_file, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n详细报告已保存到: {self.config.log_file}")
        except Exception as e:
            print(f"\n保存报告失败: {str(e)}")

# ===================== 主程序 =====================
def main():
    """主函数"""
    print("初始化JSNgame库检查系统...")
    
    # 创建配置
    config = CheckConfig()
    
    # 检查测试数据目录
    utils = CheckUtils()
    test_data_exists, test_data_status, _ = utils.check_file_exists(config.test_data_path)
    
    if not test_data_exists:
        print(f"警告: 测试数据目录 '{config.test_data_path}' 不存在")
        create_dir = input("是否创建目录? (y/n): ").lower()
        if create_dir == 'y':
            os.makedirs(config.test_data_path, exist_ok=True)
            print(f"已创建目录: {config.test_data_path}")
            print("请将测试文件放入该目录:")
            print("  - 图片: .png 文件")
            print("  - 加密图片: .jpt 文件")
            print("  - 音频: .mp3 文件")
            print("  - 加密音频: .jmus 文件")
            print("  - 视频: .mp4 文件")
            continue_check = input("是否继续检查? (y/n): ").lower()
            if continue_check != 'y':
                return
    
    # 显示系统信息
    system_info = utils.get_system_info()
    print(f"\n系统信息:")
    print(f"  操作系统: {system_info['platform']}")
    print(f"  Python版本: {system_info['python_version'].split()[0]}")
    print(f"  处理器: {system_info['processor']}")
    
    # 检查级别选择
    print(f"\n检查级别:")
    print("  1. 基本检查 (仅核心功能)")
    print("  2. 标准检查 (核心+主要功能)")
    print("  3. 全面检查 (所有功能 + 性能测试)")
    
    try:
        choice = int(input("请选择检查级别 (1-3): "))
        if choice == 1:
            config.check_level = "basic"
        elif choice == 2:
            config.check_level = "standard"
        else:
            config.check_level = "comprehensive"
    except:
        print("使用默认级别: 全面检查")
    
    # 交互模式确认
    interactive_choice = input("\n启用交互模式(需要用户评分)? (y/n): ").lower()
    config.interactive_mode = (interactive_choice == 'y')
    
    if not config.interactive_mode:
        print("注意: 非交互模式下将使用默认评分")
    
    # 开始检查
    input("\n按 Enter 键开始检查...")
    
    try:
        manager = CheckManager(config)
        manager.run_all_checks()
        
        # 显示完成信息
        print("\n" + "="*80)
        print("JSNgame 库检查完成!")
        print("="*80)
        
        # 建议
        print("\n建议:")
        
        # 分析结果给出建议
        errors_count = sum(len(r.get("errors", [])) for r in manager.results)
        warnings_count = sum(len(r.get("warnings", [])) for r in manager.results)
        
        if errors_count > 0:
            print(f"  - 发现 {errors_count} 个错误，请优先修复")
            
        if warnings_count > 0:
            print(f"  - 发现 {warnings_count} 个警告，建议处理")
            
        # 检查测试文件完整性
        print("\n测试文件检查:")
        for file_type, files in config.test_files.items():
            for file_name in files:
                file_path = os.path.join(config.test_data_path, file_name)
                exists, status, size = utils.check_file_exists(file_path)
                status_symbol = "✓" if exists else "✗"
                print(f"  {status_symbol} {file_name}: {status}")
        
        print(f"\n感谢使用 JG.check 系统!")
        
    except KeyboardInterrupt:
        print("\n\n检查被用户中断")
    except Exception as e:
        print(f"\n检查过程中发生错误: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
