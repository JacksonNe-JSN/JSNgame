import LIBbase.JSNgame as jg
import time
screen = jg.Screen([800,500],title='try_XNSB')
event = jg.event
sb = event.ShouBin(mode='XuNi',id='sb1')
sb.plc=[300,300]
plc = [0,0]
while 1:
    print(sb.test(),event.pos,sb.zt)
    screen.fill((255,255,255))
    for e in event.get():
        sb.load(e)
        if event.test(e,jg.Event['QUIT']):jg.exit()
        if event.key_down(e,jg.Event['K_a']):
            sb.big += 1
            print(sb.big)
        if event.key_down(e,jg.Event['K_d']):
            sb.big -= 1
            print(sb.big)
        if event.mouse_down(e,3):
            sb.plc = event.pos
    screen.blit('./icon.ico',plc)
    plc[0] += sb.test()[0]
    plc[1] += sb.test()[1]
    sb.show(screen)
    screen.load()
