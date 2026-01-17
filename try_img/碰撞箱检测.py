from LIBbase import JSNgame as jg
screen = jg.Screen([800,600],title='PZXtest25_8_21')
pzx = jg.PengZhuangXiang(screen)
event = jg.event

pzx1 = pzx.add(plc=[0,0],size=[50,50])
pzxs = []
print(pzxs)
plc = [0,0]
while 1:
    screen.fill((255,255,255))
    for e in event.get():
        if event.test(e,jg.Event['QUIT']):
            jg.exit()
        if event.mouse_down(e):
            pzxs.append(pzx.add(plc=event.pos,size=[100,100]))
        if event.mouse_down(e,3):
            pzxs.append(pzx.add(plc=event.pos,size=[100,100],mode='round'))
        plc = event.pos
        pzx1.plc = [plc[0]-50,plc[1]-50]
    for pzx2 in pzxs:
        a = pzx.test(pzx1, pzx2)
        print(a if a else '')
    pzx.show()
    screen.load()
[[[['left'], ['right']], []]]






