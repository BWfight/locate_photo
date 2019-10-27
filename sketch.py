import cv2
import os


def AT_style(image):
    '''
    二值化素描  
    核心：阈值化，基于图像中物体与背景之间的灰度差异，进行的像素级别的分割
    步骤：先对原图进行模糊化，过滤去过多的细节，再对图片进行二值化   
    :param image
    '''
    # 打开图片    # bgr格式，不是常见的rgb
    img_bgr = cv2.imread(image)
    # 转化为灰度图
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    # 模糊化，cv2.medianBlur()中值滤波函数
    img_gray = cv2.medianBlur(img_gray, 5)   
    # 二值化，cv2.adaptiveThreshold()自适应二值化，根据图像不同区域亮度分布进行局部自动调节
    img_edge = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=3, C=2) 
    # 保存图片
    name = image[:-4]
    file_name = name + 'a.jpg'
    cv2.imwrite(file_name, img_edge)


def GB_style(image):
    '''
    高斯滤波素描  
    核心：同上，再加入底片融合的方式，获取原图中一些比较重要的线条
    :param image
    ''' 
    img_bgr = cv2.imread(image)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    # 模糊化，cv2.GaussianBlur()高斯滤波函数    # cv2.medianBlur()中值滤波函数效果不好
        # # 调参：ksize: 高斯核的大小，大于0且为奇数。sigmaX 和 sigmaY 分别表示高斯核在 X 和 Y 方向上的标准差。
    img_blur = cv2.GaussianBlur(img_gray, ksize=(21, 21), sigmaX=0, sigmaY=0)     
    # 将原图和模糊图像进行融合，cv2.divide()本质上进行的是两幅图像素级别的除法操作，得到两幅图之间有明显差异的部分
    img_blend = cv2.divide(img_gray, img_blur, scale=255)
    name = image[:-4]
    file_name = name + 'b.jpg'
    cv2.imwrite(file_name, img_blend)


def patch_images(file_fold_path):
    '''
    批量处理
    '''
    # 获取文件夹下所有文件
    iamge_List = os.listdir(file_fold_path)
    for image in iamge_List:
        os.chdir(file_fold_path)  # 必须转到图片所在文件夹下才能读取
        GB_style(image)


if __name__ == '__main__':
    file_fold_path = 'D:'
    patch_images(file_fold_path)
    image_path = 'sketch_example.jpg'
    GB_style(image_path)