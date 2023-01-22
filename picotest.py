##
## ILI9488 demos on RPi Pico with Waveshare Pico-ResTouch-LCD-3.5.
##

from ili9488 import Display, color565, bswap16
from machine import Pin, SPI
from xglcd_font import XglcdFont
import framebuf
import array
import time

def test_1():
    """Original main.py test with xglcd fonts + some rectangles."""
    # Baud rate of 60000000 seems about the max
    spi = SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
    display = Display(spi, dc=Pin(8), cs=Pin(9), rst=Pin(15),
                      width=480, height=320, rotation=90)

    display.clear(color565(255,0,0))
    print('wrote clear RED')
    time.sleep(1)
    display.draw_rectangle(100, 100, 100, 100, 0xffff)
    print('wrote outline WHITE')
    display.fill_hrect(200, 150, 100, 100, color565(0,255,0))
    print('wrote hrect GREEN')
    time.sleep(1)

    print('Loading fonts...')
    print('Loading arcadepix')
    arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
    print('Loading bally')
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)

    display.draw_text(0, 10, "This's a small test!", arcadepix, 
                      color565(255, 255, 255))
    display.draw_text(0, 100, 'Bally 7x9', bally, color565(0, 255, 0))
    display.draw_text8x8(0, 150, 'Built-in 8x8', color565(0, 255, 255))
    display.draw_line(160, 0, 160, 319, color565(0, 0, 255))


def test_2():
    """Test a portrait-style orientation."""
    spi = SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
    display = Display(spi, dc=Pin(8), cs=Pin(9), rst=Pin(15),
                      width=320, height=480, rotation=0)

    display.clear()
    display.draw_rectangle(70, 0, 50, 50, 0xffff)
    display.fill_rectangle(0, 0, 50, 50, color565(255, 0, 0))
    display.draw_text8x8(0, 80, 'Waveshare Test!', color565(255, 255, 0))
    display.draw_hline(0, 90, 240, color565(0, 255, 0))
    display.draw_vline(60, 90, 70, color565(0, 0, 255))


def test_3():
    """This (mostly) replicates the pattern in main_3inch5.py from Waveshare."""
    spi = SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
    display = Display(spi, dc=Pin(8), cs=Pin(9), rst=Pin(15),
                      width=480, height=320, rotation=90)

    display.clear(0xffff)
    display.fill_rectangle(140, 5, 200, 30, color565(255, 0, 0))
    display.draw_text8x8(170, 17, "Raspberry Pi Pico", 0xffff,
                         background=0xf800)
    display.draw_text8x8(170, 57, "3.5' IPS LCD TEST", 0x0, background=0xffff)
    disp_color = 0x001F
    for i in range(0,12):
        display.fill_rectangle(i*30+60, 100, 30, 50, disp_color)
        disp_color = disp_color << 1
    display.fill_rectangle(0, 220, 120, 100, color565(255, 0, 255))
    display.fill_rectangle(120, 220, 120, 100, color565(255, 255, 0))
    display.fill_rectangle(240, 220, 120, 100, color565(0, 255, 0))
    display.fill_rectangle(360, 220, 120, 100, color565(0, 255, 255))


def test_4():
    """Left half draws native, while right half draws to FB and block()."""
    spi = SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
    disp = Display(spi, dc=Pin(8), cs=Pin(9), rst=Pin(15),
                      width=480, height=320, rotation=90)

    buf = bytearray(240*80*2)
    fb = framebuf.FrameBuffer(buf, 240, 80, framebuf.RGB565)

    # std colors
    white = 0xffff
    black = 0
    red = color565(255, 0, 0)
    green = color565(0, 255, 0)
    magenta = color565(255, 0, 255)
    cyan = color565(0, 255, 255)
    yellow = color565(255, 255, 0)

    ## compare native calls on left to FrameBuffer blit on right
    # 1st quarter
    disp.fill_rectangle(0, 0, 240, 80, white)
    disp.fill_rectangle(50, 10, 100, 50, cyan)
    disp.draw_text8x8(70, 30, 'rect', magenta, background=cyan)

    fb.fill(white)
    fb.rect(50, 10, 100, 50, bswap16(cyan), True)
    fb.text('rect', 70, 30, bswap16(magenta))
    disp.block(240, 0, 479, 79, buf)

    # 2nd quarter
    disp.draw_ellipse(120, 120, 80, 30, red)
    disp.draw_text8x8(100, 120, 'ellipse', white)

    fb.fill(black)
    fb.ellipse(120, 40, 80, 30, bswap16(red))
    fb.text('ellipse', 100, 40, white)
    disp.block(240, 80, 479, 159, buf)

    # 3rd quarter
    disp.fill_rectangle(0, 160, 240, 80, white)
    disp.fill_polygon(6, 120, 200, 30, green)
    disp.draw_text8x8(100, 200, 'polygon', black, background=green)

    fb.fill(white)
    verts = array.array('h', [-20, -25, 20, -25, 30, 0, 20, 25, -20, 25, -30, 0])
    fb.poly(120, 40, verts, bswap16(green), True)
    fb.text('polygon', 100, 40, black)
    disp.block(240, 160, 479, 239, buf)

    # 4th quarter
    disp.draw_line(0, 240, 239, 319, yellow)
    disp.draw_line(239, 240, 0, 319, yellow)
    disp.draw_text8x8(100, 280, 'lines', white)

    fb.fill(black)
    fb.line(0, 0, 239, 79, bswap16(yellow))
    fb.line(239, 0, 0, 79, bswap16(yellow))
    fb.text('lines', 100, 40, white)
    disp.block(240, 240, 479, 319, buf)


if __name__ == '__main__':
    # spin through all tests (or comment out and just pick one)
    test_1()
    time.sleep(5)
    test_2()
    time.sleep(5)
    test_3()
    time.sleep(5)
    test_4()
