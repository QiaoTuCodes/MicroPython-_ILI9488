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

    display.draw_text(0, 0, 'This''s a small test!', arcadepix, color565(0, 0, 255))
    display.draw_text(0, 22, 'Bally 7x9', bally, color565(0, 255, 0))
    for i in range(480):
        display.draw_pixel(160, i, color565(255, 0, 0))
test()
