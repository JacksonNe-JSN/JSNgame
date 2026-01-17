
act = {
    'screen':1,
    'event':0,
    'mixer':1,
    'word':0,
    'time':1,
    'it':1,
    'random':1

}












import time
import os

#工作地点#
try:
    current_dir = os.getcwd()
    
    # 构造父目录路径
    parent_dir = os.path.dirname(current_dir)
    
    # 如果已经在根目录，则无法切换（返回当前目录）
    if parent_dir == current_dir:
        print("已在根目录，无法继续向上切换")
    
    # 切换工作目录
    os.chdir(parent_dir)
    print(f'当前工作地点:{os.getcwd()}')
except Exception as e:
    print(f'工作地点出错:{e}')
    
from LIBbase import JSNgame as jg






#-----自动检查模块-----#
try:
    screen = jg.Screen([700,500])
except Exception as e:
    print(f'Screen模块不正常,无法完成测试:{e}')
    jg.exit()

try:
    mixer = jg.mixer()
except Exception as e:
    print(f'mixer模块不正常,无法完成测试:{e}')
    jg.exit()

try:
    event = jg.event
except Exception as e:
    print(f'event模块不正常,无法完成测试:{e}')
    jg.exit()

try:
    Time = jg.Time()
except Exception as e:
    print(f'Time模块不正常:{e}')

try:
    Random = jg.Random()
except Exception as e:
    print(f'Random模块不正常:{e}')

try:
    IT = jg.IT()
except Exception as e:
    print(f'IT模块不正常:{e}')

try:
    word = jg.Word()
except Exception as e:
    print(f'Word模块不正常:{e}')
    


def event_bed():
    for e in event.get():
        if event.test(e,jg.Event['QUIT']) or event.test_key(e,jg.Event['K_ESCAPE']):
            print('测试中断')
            jg.Exit()
            print('llllllllllllll')


        

'''Screen'''
try:
    if act['screen']:
        screen = jg.Screen((700,500))
        #设置大小
        print('  设置大小')
        time.sleep(0.1)
        y = 1
        for x  in range(1,1500,10):
            y += 1
            screen = jg.Screen((x,y))
        del x,y
        screen = jg.Screen((700,500))

        
        #填充颜色
        print('  填充颜色')
        g=0
        b=0
        for r in range(0,256,20):
            for g in range(0,256,20):
                for b in range(0,256,20):
                    screen.fill((r,g,b))
                    screen.load()
                    for e in jg.event.get():
                        if event.test_key(e,jg.Event['K_SPACE']):
                            break
        del r,g,b

        
        #打印图片
        print('  打印图片')
        print('        普通打印')
        for x in range(0,700,50):
            for y in range(-7000,7000,50):
                Time.FPS(120000)
                screen.fill((255,255,255))
                screen.blit('./JSNgame/try_img/python_logo.png',(x,y/10))
                screen.word(str(Time.get_FPS()*5000),rgb=(0,0,0))
                screen.load()
                for e in jg.event.get():
                    if event.test_key(e,jg.Event['K_SPACE']):
                        break
        print(f"平均帧率{str(Time.get_FPS())}")

                        
        print('        加密打印')
        for x in range(0,700,1):
            for y in range(-700,700,900000):
                Time.FPS(1200000000)
                screen.blit('./JSNgame/try_img/python_logo.png',(x,y))
                screen.fill((255,255,255))
                screen.blit('./JSNgame/try_img//j1.jpt',(x,y))
                screen.word(str(Time.get_FPS()),rgb=(0,0,0))
                screen.load()
                for e in jg.event.get():
                    if event.test_key(e,jg.Event['K_SPACE']):
                        break
        print(f"平均帧率{str(Time.get_FPS())}")

        
        
        #旋转、缩放图片
        print('        旋转、缩放图片')
        for jd in range(0,900):
            screen.fill((255,255,255))
            screen.blit('./JSNgame/try_img/python_logo.png',(150,50),jd=jd/10*2)
            screen.load()
            for e in jg.event.get():
                if event.test_key(e,jg.Event['K_SPACE']):
                    break
        for big in range(0,100):
            screen.fill((255,255,255))
            big = big*2
            screen.blit('./JSNgame/try_img/python_logo.png',(-big*10,-big*10),big=big/10,mode='big')
            screen.load()
            for e in jg.event.get():
                if event.test_key(e,jg.Event['K_SPACE']):
                    break
        del jd,big
        

        #透明通道
        print('    透明通道')
        r = 0
        g = 0
        b = 0
        '''fill普通填充'''
        for glass in range(0,256,50):
            for r in range(0,256,50):
                for g in range(0,256,50):
                    for b in range(0,256,50):
                        screen.fill((255,255,255))
                        screen.blit('./JSNgame/try_img/python_logo.png',(150,50))
                        screen.fill((r,g,b),mode='glass',glass=glass)
                        screen.load()
                        for e in jg.event.get():
                            if event.test_key(e,jg.Event['K_SPACE']):
                                break


        '''vfill滤镜模式'''
        print('      vfill滤镜模式')
        for mode in ['normal','glass']:
            for glass in range(0,256,50):
                for r in range(0,256,50):
                    for g in range(0,256,50):
                        for b in range(0,256,50):
                            screen.fill((255,255,255))
                            screen.blit('./JSNgame/try_img/python_logo.png',(150,50))
                            screen.vfill((r,g,b),mode=mode,glass=glass)
                            screen.load()
                            for e in jg.event.get():
                                if event.test_key(e,jg.Event['K_SPACE']):
                                    break
        del glass,r,g,b,mode

        
        #特效TeXiao
        print('  特效TeXiao')
        screen.blit('./JSNgame/try_img/python_logo.png',(0,0))
        screen.load()
        for i in ['MoHu','GuangJiao','SeCha','BoWenSeCha','ZhenDong']:
            print(f'      {i}')
            for j in range(100):
                screen.fill((255,255,255))
                screen.blit('./JSNgame/try_img/python_logo.png',(180,70))
                screen.TeXiao(i,j,jd=round(j*0.12,1))
                screen.load()
                time.sleep(0.01)
                for e in jg.event.get():
                    if event.test_key(e,jg.Event['K_SPACE']):
                        break

                    
        #视频流movie
        print('  视频流movie')
        st= time.time()
        while 1:
            event.updata()
            if time.time()-st > 10:
                break
            if event.key_down(key=jg.Event['K_q']):
                break
            screen.fill((255,0,0))
            screen.movie('./JSNgame/try_img/mp4.mp4',speed=100,blit=event.key_down(key=jg.Event['K_SPACE']),plc=[0,0],rgb=[0,255,0,100])
            screen.load()


        #画画函数draw
        print('  画画函数draw')
        for mode in ["Xian","Yuan","Fang","Xin","Dian"]:
            print('    ',mode)
            for big in range(0,20000):
                screen.fill((255,255,255))
                screen.draw(mode,(180,70),size=[big/1000,big/500],rgb=[[0,0,0],[0,0,0]])
                screen.load()
                for e in jg.event.get():
                    if event.test_key(e,jg.Event['K_SPACE']):
                        break


        #文字函数
        print('  文字函数')
        words = 'abcdefghijklmnopqrstuvwxyz'
        for mode in ['small','big']:
            r=0
            g=0
            b=0
            for i in words:
                screen.fill((255,255,255))
                if mode == 'small':     
                    screen.word(i,(350,250),rgb=(0,0,0))
                else:
                    screen.word(i.upper(),(350,250),rgb=(0,0,0))
                screen.load()
                time.sleep(0.1)
                for e in jg.event.get():
                    pass


        
            
        
        print('{}模块成分完整'.format('Screen'))
except Exception as e:
    print('{}模块成分缺失:{}'.format('Screen',e))
    jg.wrong(e)

'''event'''
try:
    if act['event']:
        event2 = jg.event2()
        Event = jg.Event
        event = jg.event
        print('{}模块成分完整'.format('event'))
except Exception as e:
    print('{}模块成分缺失:{}'.format('event',e))

'''mixer'''
try:
    if act[ 'mixer']:
        print('测试中...:mixer')
        def yl_ct(b=None): # YinLiang_ctrl
            screen.fill([255,255,255])
            a=screen.TuoDongTiao(plc=[200,100],size=[300,30],id='a')
            screen.word(f'音量:{round(a*100,1)}',plc=[0,100],rgb=(0,0,0))
            if b:
                c=screen.TuoDongTiao(plc=[200,250],size=[300,30],id='c')
                c = (c-0.5)*(90/50)*100
                print(c)
                screen.word(f'左右声道:{round(c,1)}',plc=[0,250],rgb=(0,0,0))
                b.yinliang(a)
                b.set_plc(c)
            else:
                mixer.yinliang(a)
            screen.load()
            
        mixer = jg.mixer()
        
        # == 播放 == #
        print('    播放:')
        print('      背景音乐开始:')
        mixer.bgm('./JSNgame/try_img/j1.mp3',-1)
        st = time.time()
        while time.time()-st < 10:
            for e in event.get():
                event_bed()
                if event.test(e,Event['KEYDOWN']):st = time.time()-10
            yl_ct()
        mixer.stop_all()
        print('      背景音乐结束;\n')

        print('      mp3音效开始:')
        j1 = mixer.sound('./JSNgame/try_img/j1.mp3',50)
        st = time.time()
        while time.time()-st < 10:
            event_bed()
            yl_ct(j1)
        j1.stop()
        j1.clean()
        print('      mp3音效结束;\n')

        print('      加密音效开始:')
        j1 = mixer.sound('./JSNgame/try_img/j1.jmus')
        st = time.time()
        while time.time()-st < 10:
            event_bed()
            yl_ct(j1)
        j1.stop()
        j1.clean()
        print('      加密音效结束;')

            
        # == / 麦克风 / == #
        print('  麦克风:')
        a = 1
        mixer.open_mkf()
        while a:
            for e in event.get():
                if event.key_down(e,jg.Event['K_e']):
                    a=0
            m = mixer.get_mkf()
            screen.fill((255,255,255))
            screen.word(f"音量:{round(m['YinLiang']*100,2)} db",plc=(0,200),rgb=(0,0,0))
            screen.draw(plc=(100,200),mode='Xian',big=m['YinLiang']*100,rgb=(255,0,0))
            screen.word(f"音调:{round(1000-m['YinDiao'],20)/10 if m['YinDiao'] != 0 else 0.0}",plc=(0,350),rgb=(0,0,0))
            screen.draw(plc=(100,350),mode='Xian',big=round(1000-m['YinDiao'],10)/20 if m['YinDiao'] != 0 else 0,rgb=(255,0,0))
            
            screen.load()
        mixer.close_mkf()
        print('{}模块成分完整'.format('mixer'))
except Exception as e:
    print('{}模块成分缺失:{}'.format('mixer',e))

'''Word'''
try:
    if act['word']:
        Word = jg.Word()
        print('{}模块成分完整'.format('Word'))
except Exception as e:
    print('{}模块成分缺失:{}'.format('Word',e))

'''Time'''
try:
    if act['time']:
        Time = jg.Time()
        print('{}模块成分完整'.format('Time'))
except Exception as e:
    print('{}模块成分缺失:{}'.format('Time',e))

'''Random'''
try:
    if act['random']:
        Random = jg.Random
        print('{}模块成分完整'.format('Random'))
except Exception as e:
    print('{}模块成分缺失:{}'.format('Random',e))

'''IT'''
try:
    if act['it']:
        IT = jg.IT()
        print('{}模块成分完整'.format('IT'))
except Exception as e:
    print('{}模块成分缺失:{}'.format('IT',e))


    
'''  
__all__ = [
    'Screen', 'Event', 'event2', 'event', 'Xbox', 'mixer', 
    'Word', 'Time', 'Random', 'IT', 'Exit', 'exit', 'wrong',
    'init', 'Key', 'Log'
]
'''
input()
jg.Exit()
