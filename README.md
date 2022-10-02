The ILI9488 TFT Driver for [MicroPython Ports]

The driver has been tested on 01Studio Series Open Board. but It should work on whatever other micropython ports, if anyone find problems in other boards, please open an issue and We'll see.

##Motivation
In 01Studio series open board that does not currently use any ILI9488-based TFT liquid crystal display , but here will complement complete that.

##References:
The ILI9488 Driver has transplant from ILI9431. So you We'll see codes of here.
* [LCD Codes](https://github.com/adafruit/Adafruit_Python_ILI9341/blob/master/Adafruit_ILI9341/ILI9341.py)
* [LCD Datasheet](http://www.lcdwiki.com/zh/3.5inch_SPI_Module_ILI9488_SKU:MSP3520) from LCDs manufacturer

##Usage Example:

###1.1 display colorful text：
<img src="https://github.com/QiaoTuCodes/MicroPython-_ILI9488/blob/main/src/img/screen.jpg" alt="ILI9488 Logo" width="304" height="228"/>


```python
#!/usr/bin/python
# -*-coding:utf-8 -*-
"""
-------------- Description: ------------------
   FileName : main.py
   Author : 绒毛宝贝
   ProjectName : PyBoard
   IDE Version : PyCharm
   Date:2022/10/2 3:06
   QQ:287000822 E-mail: gomehome@qq.com
------------------- END ----------------------
"""
__author__ = 'Isaac'

"""ILI9488 demo (fonts)."""
from time import sleep
from ili9488 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont
import random

def test():
    """Test code."""
    # Baud rate of 60000000 seems about the max
    spi = SPI(1, baudrate=60000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(21), cs=Pin(15), rst=Pin(33))

    print('Loading fonts...')
    print('Loading arcadepix')
    arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
    print('Loading bally')
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)
    
    for i in range(0,60):
        
        display.draw_text(random.randint(0,320), random.randint(0,480), 'This''s a small test!', arcadepix, color565(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        display.draw_text(random.randint(0,320), random.randint(0,480), 'Bally 7x9', bally, color565(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    for i in range(480):
        display.draw_pixel(160, i, color565(255, 0, 0))
test()

```

[PDF DataSheet](src/chip_docs/ILI9488-DataSheet_100.pdf) for further info about ILI Series Driver Relevant reference information.
