from PIL import Image as im

a = im.open('bgp.png')
b = a.size
c = a.load()
n = 0
for i in range(b[0]):
    if i%75 == 0:
        if n == 0:
            n = 1
        elif n == 1:
            n = 0
    for j in range(b[1]):
        if j%75 == 0:
            if n == 0:
                n = 1
            elif n == 1:
                n = 0
        if n == 0:
            a.load()[i,j] = (100,0,100,255)
        else:
            a.load()[i,j] = (200,200,0,255)
a.save('b2.png')
print('succeed')
#劳大配色似乎更好看QAQ
