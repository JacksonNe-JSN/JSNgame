from PIL import Image
from PIL import Image, ImageDraw, ImageFont
import os

color = ['黑','白']
t = ['兵','车','象','马','后','王']
def tm(a,n, m):
    with Image.open("{}".format(a)) as img:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("zt.ttf", 40)
        except IOError:
            raise Exception("字体文件 zt.ttf 未找到")
        
        # 计算文字位置
        img_width, img_height = img.size
        text_bbox = draw.textbbox((0, 0), n, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # 计算居中坐标
        x = (img_width - text_width) / 2
        y = (img_height - text_height) / 2
        
        # 添加文字
        draw.text((x, y), n, fill=m, font=font)
        
        # 覆盖保存原图
        img.save("{}".format(a))
for i in t:
    for j in color:
        a = Image.open('{}bg.png'.format(j))
        a.save('{}{}.png'.format(j,i))
        if j=='黑':
            p = (0,0,0)
        else:
            p=(255,255,255)
        tm(('{}{}.png'.format(j,i)),i,p)
        print('succeed',j,i)
