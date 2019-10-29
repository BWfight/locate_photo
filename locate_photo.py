import exifread
import re
from selenium import  webdriver
from selenium.webdriver.chrome.options import Options 
import time                        
import os

'''
author: BW
vision: 1.1
'''

 
def latitude_and_longitude_convert_to_decimal_system(*arg):
    """
    经纬度转为小数
    :param arg:
    :return: 十进制小数
    """
    return float(arg[0]) + ((float(arg[1]) + (float(arg[2].split('/')[0]) / float(arg[2].split('/')[-1]) / 60)) / 60)    # 例子：北纬N39°34′14.95″ ：39+34÷60+14.95÷3600=39.5708181173
 
 
def find_GPS_image(pic_path):
    '''
    各类信息
    return: Info
    '''
    Device = {}
    Photo = {}
    GPS = {}
    date = ''
    with open(pic_path, 'rb') as f: 
        tags = exifread.process_file(f)                      
        # print(tags)
        for tag, value in tags.items():                             
            if re.match('Image Make', tag):                 
                Device['品牌信息'] = str(value)         
            if re.match('Image Model', tag):               
                Device['具体型号'] = str(value)  
            if re.match('EXIF LensModel', tag):              
                Device['摄像头信息'] = str(value) 
            if re.match('EXIF ExifImageWidth', tag):     # 照片像素信息           
                Photo['宽'] = str(value)
            if re.match('EXIF ExifImageLength', tag):             
                Photo['长'] = str(value)
            if re.match('GPS GPSLatitudeRef', tag):          
                GPS['GPSLatitudeRef'] = str(value)           # N/S = 北/南纬 
            elif re.match('GPS GPSLongitudeRef', tag):                      # 这里用elif，否则匹配出问题
                GPS['GPSLongitudeRef'] = str(value)          # E/W = 东/西经 
            elif re.match('GPS GPSAltitudeRef', tag):        
                GPS['GPSAltitudeRef'] = str(value)           # 海拔   
            elif re.match('GPS GPSLatitude', tag):           
                deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]     # 先用[1:-1]切片操作，左起第二个元素到最后一个元素，去掉 [ 和 ]。再用split取度分秒
                GPS['GPSLatitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)  # 纬度
            elif re.match('GPS GPSLongitude', tag):      
                deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                GPS['GPSLongitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)  # 经度
            elif re.match('GPS GPSAltitude', tag):
                GPS['GPSAltitude'] = str(value)     
            elif re.match('.*Date.*', tag):
                date = str(value)                  # 日期              
    return {'GPS_information': GPS, 'date_information': date, 'Device_information': Device, 'Photo_information': Photo}
 
def find_address_from_GPS(Info):
    """
    使用Geocoding API把经纬度坐标转换为结构化地址。
    :param: Info
    :return: location
    """
    chrome_options = Options() 
    chrome_options.add_argument('--headless') # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options = chrome_options)   # 设置引擎为Chrome，真实地打开一个Chrome浏览器，赋值给变量driver，在后台默默运行

    driver.get('http://api.map.baidu.com/lbsapi/getpoint/index.html') # 百度地图拾取坐标系统
    time.sleep(2)    # 让网页全加载完。  # 用selenium把网页打开，所有信息就都加载到了Elements那里，之后，就可以把动态网页用静态网页的方法爬取了

    driver.find_element_by_class_name('pointLabel').click()   # 找到，点击‘坐标反查’按钮
    time.sleep(.5)   

    driver.find_element_by_id('localvalue').send_keys(str(Info['GPS_information']['GPSLongitude'])+','+str(Info['GPS_information']['GPSLatitude'])) 
    time.sleep(.5) 

    driver.find_element_by_id('localsearch').click()   
    time.sleep(1) 

    # address = driver.find_elements_by_id('txtPanel') 
    # print(address)           

    from bs4 import BeautifulSoup
    pageSource = driver.page_source # 获取Elements中渲染完成的网页源代码  
    soup = BeautifulSoup(pageSource,'html.parser')  # 使用bs解析网页
    location = soup.find('div',id='txtPanel').text

    driver.quit() # 关闭浏览器   
    return(location)

if __name__ == '__main__':
    Info = find_GPS_image(pic_path='D:/照片.jpg') 
    try:
        address = find_address_from_GPS(Info=Info)
        print(address)
        print("GPS：", Info['GPS_information'])
        print('拍摄时间：', Info['date_information'])
        print('设备信息：', Info['Device_information'])
        print('照片信息：', Info['Photo_information'])
    except:
        print('没有位置信息。以下为可获取的信息：')
        print("GPS：", Info['GPS_information'])
        print('拍摄时间：', Info['date_information'])
        print('设备信息：', Info['Device_information'])
        print('照片信息：', Info['Photo_information'])   # 12M: 4000*3000左右   7M: 3000*2300左右 区分是否自拍
    
    
