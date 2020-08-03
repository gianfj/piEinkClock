#!/usr/bin/python3

import epd2in7
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from gpiozero import Button
import subprocess
import urllib.request
import datetime
import time
import re
import string
import calendar
def clock():
    global epd 
    temphum = []
    try:
        data=urllib.request.urlopen('http://192.168.88.10/humidity.log')
        for line in data:
            lastline=line.decode('utf-8')
        lastline=lastline.split(' -> ')
        temphum=lastline[1].split(' - ')
    except:
        temphum = ['Nul','Nul']
    IP = subprocess.run(['hostname', '-I'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
    uptime = subprocess.run(['uptime', '-p'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
    uptime = re.sub('up ','Up:',uptime.stdout)
    uptime = re.sub(' days,','d',uptime)
    uptime = re.sub(' day,','d',uptime)
    uptime = re.sub(' hours,','h',uptime)
    uptime = re.sub(' hour,','h',uptime)
    uptime = re.sub(' minutes','m',uptime)
    uptime = re.sub(' minute','m',uptime)
    LA = subprocess.run(['uptime'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
    LA = re.sub('.* load average: ','LA: ',LA.stdout)
    #12:09:33 up 1 day,  4:43,  2 users,  load average: 0.24, 0.22, 0.19
    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 80)
    draw.text((1,0), 'IP: %s' %(IP.stdout), font = font, fill = 0)
    draw.text((1,20), 'Temp:%s°C  Hum:%s%%' %(temphum[0],temphum[1].rstrip()), font = font, fill = 0)
    draw.text((35,40),datetime.datetime.now().strftime("%H:%M") , font = font2, fill = 0)
    draw.text((1,124),uptime , font = font, fill = 0)
    draw.text((1,144),LA , font = font, fill = 0)
    image = image.rotate(90,expand=True)

    epd.display_frame(epd.get_frame_buffer(image))

    # display images
    #epd.display_frame(epd.get_frame_buffer(Image.open('monocolor.bmp')))
def cal():
    global epd 
    today=int(datetime.datetime.now().strftime("%d"))
    cal=(calendar.month(int(datetime.datetime.now().strftime("%y")),int(datetime.datetime.now().strftime("%m"))))
    cal = re.sub('$',' ',cal)
    cal = re.sub('\n','\n ',cal)
    cal = re.sub(' ','  ',cal)
    cal = re.sub(' %s ' %today,'(%s)' %today,cal)
    cal = re.sub('  ',' ',cal)
    cal = re.sub(' \(','(',cal)
    cal = re.sub('\) ',')',cal)
    cal = re.sub('\n ','\n',cal)
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 22)
    draw.text((1,0), '%s' %cal , font = font, fill = 0)
    image = image.rotate(90,expand=True)
    epd.display_frame(epd.get_frame_buffer(image))

def temp():
    global epd 
    data=urllib.request.urlopen('http://192.168.88.10/humidity.log')
    for line in data:
        lastline=line.decode('utf-8')
    lastline=lastline.split(' -> ')
    temphum=lastline[1].split(' - ')
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 80)
    draw.text((1,20), '%s°\n%s%%' %(temphum[0],temphum[1].rstrip()), font = font, fill = 0)
    image = image.rotate(90,expand=True)
    epd.display_frame(epd.get_frame_buffer(image))

def error():
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 80)
    draw.text((1,20), 'ERROR' , font = font, fill = 0)
    image = image.rotate(90,expand=True)
    epd.display_frame(epd.get_frame_buffer(image))

def wifi():
    im = Image.open(r"wifi.png")
    size = int(im.width*1.8), int(im.height*1.8)
    im = im.resize (size)
    #im=im.resize(size, Image.ANTIALIAS)
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white
    image.paste(im)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
    draw.text((175,20), 'wem127a' , font = font, fill = 0)
    draw.text((175,40), 'RUyQvFw6' , font = font, fill = 0)
    image = image.rotate(90,expand=True)
    epd.display_frame(epd.get_frame_buffer(image))

def handleBtn1Press():
    global mode
    mode="clock"
    clock()

def handleBtn2Press():
    global mode
    mode="cal"
    cal()

def handleBtn3Press():
    global mode
    mode="temp"
    temp()

def handleBtn4Press():
    global mode
    mode="wifi"
    wifi()

if __name__ == '__main__':
    epd = epd2in7.EPD()
    epd.init()
    btn1 = Button(5)
    btn2 = Button(6)
    btn3 = Button(13)
    btn4 = Button(19)
    mode = "clock"
    min="a"
    while True:
        try:
            btn1.when_pressed = handleBtn1Press
            btn2.when_pressed = handleBtn2Press
            btn3.when_pressed = handleBtn3Press
            btn4.when_pressed = handleBtn4Press
            if (datetime.datetime.now().strftime("%M") != min):
                min = datetime.datetime.now().strftime("%M")
                if mode == "clock": clock()
                if mode == "cal": cal()
                if mode == "temp": temp()
            time.sleep(1)
        except:
            error()





    



