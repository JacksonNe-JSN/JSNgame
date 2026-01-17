from LIBbase import JSNgame as jg
import time
screen = jg.Screen([800,500],title='碰撞箱test')
event = jg.event
mixer = jg.mixer()
pzx = jg.PengZhuangXiang(screen)

def event_bed(e):
    global plc
    if event.test(e,jg.Event['QUIT']):
        jg.exit()
    plc = event.pos
    if event.mouse_down(e):
        pzx1.size[0] += 1
        pzx1.size[1] += 1
    if event.mouse_down(e,3):
        pzx1.size[0] -= 1
        pzx1.size[1] -= 1
    if event.mouse_down(e,2):
        pzxs.append([pzx.add(plc=[event.pos[0]-pzx1.size[0]-10,event.pos[1]-pzx1.size[1]-10],size=[50,50],mode='round'),[0,0]])
    if event.key_down(e,jg.Event['K_s']):time.sleep(1)
    pzx1.size[0] = max([pzx1.size[0],10])
    pzx1.size[1] = max([pzx1.size[1],10])


pzx1 = pzx.add(mode='round')
pzx1.plc = [0,0]
pzx1.size = [300,300]
pzx2 = pzx.add(plc=[-5,0],size=[10,500])
pzx3 = pzx.add(plc=[805,0],size=[10,500])
pzx4 = pzx.add(plc=[0,-5],size=[800,10])
pzx5 = pzx.add(plc=[0,505],size=[800,10])

pzxs = []
PP = [pzx2,pzx3,pzx4,pzx5]

while 1:
    screen.fill([255,255,255])
    for e in event.get():
        event_bed(e)
    n = 0
    for p in pzxs:
        b = pzx1.test(p[0])
        for c in range(0,4):
            b = [b[0]+PP[c].test(p[0])[0]/20,b[1]+PP[c].test(p[0])[1]/20]
        p[1] = [p[1][0]+b[0],p[1][1]+b[1]]
        p[0].plc = [p[0].plc[0]-p[1][0],p[0].plc[1]-p[1][1]]
        for i in range(2):
            if p[1][i] > 0.01:
                p[1][i] = round(p[1][i]-0.01, 3)
            elif p[1][i] < -0.01:
                p[1][i] = round(p[1][i]+0.01,3)
            else:
                p[1][i] = 0
        if p[0].plc[0] > 810 or p[0].plc[0] < -10 or p[0].plc[1] > 500 or p[0].plc[1] < -10:
            p[0].remove()
            pzxs.remove(p)
        n += 1
    print(len(pzxs), len(pzx._boxes))
    pzx1.plc = plc
    for i in pzx._boxes:
        i.show()
    screen.load()
    



