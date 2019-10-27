import os
import random
from PIL import Image


def draw_pic(bg_image, place_posit, pic_path, place_size):
    """
    :param bg_image: 背景图片
    :param place_posit: 要贴照片的位置
    :param pic_path: 照片路径
    :param place_size: 照片尺寸
    :return:
    """
    pic = Image.open(pic_path)        # 打开要粘贴上去的照片
    pic = pic.resize(place_size)      # 重定义照片宽高比，即变小
    bg_image.paste(pic, place_posit)  # 将照片贴到背景图片下的指定位置

if __name__ == '__main__':
    show_figure = [        # 最终形状 520 GF
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # 背景图，色彩模式为真彩色RGBA，大小(1700, 2000)，粉色(255, 192, 203)
    img = Image.new("RGBA", (1700, 2000), (255, 192, 203))
    # 照片大小
    PIC_WIDTH = 80
    PIC_HEIGHT = 120
    # 开始绘图
    row_num, column_num = len(show_figure), len(show_figure[0])
    for row in range(row_num):
        for column in range(column_num):
            if show_figure[row][column]:   # 在1的位置贴上随机照片
                images = os.listdir("D:")   # 照片列表，存放照片的文件夹
                show_image_path = os.path.join("D:", images[random.randint(0, len(images) - 1)])  # 从照片列表中随机提取一个照片
                draw_pic(img, (PIC_WIDTH * column, PIC_HEIGHT * row), show_image_path, (PIC_WIDTH, PIC_HEIGHT))  # 画图

    img.save("520.png")