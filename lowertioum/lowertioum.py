import random
import time
import ctypes
from ctypes import wintypes
import math

# Define necessary Windows API functions and constants
user32 = ctypes.WinDLL('user32')
gdi32 = ctypes.WinDLL('gdi32')

# Constants and structures
HDC = wintypes.HDC
COLORREF = wintypes.COLORREF

# Function prototypes
user32.GetDC.argtypes = [HDC]
user32.ReleaseDC.argtypes = [HDC, HDC]
gdi32.CreateCompatibleDC.argtypes = [HDC]
gdi32.CreateCompatibleBitmap.argtypes = [HDC, ctypes.c_int, ctypes.c_int]
gdi32.SelectObject.argtypes = [HDC, ctypes.c_void_p]
gdi32.DeleteDC.argtypes = [HDC]
gdi32.DeleteObject.argtypes = [ctypes.c_void_p]
gdi32.SetBkColor.argtypes = [HDC, COLORREF]
gdi32.PatBlt.argtypes = [HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
gdi32.CreateSolidBrush.argtypes = [COLORREF]
gdi32.LineTo.argtypes = [HDC, ctypes.c_int, ctypes.c_int]
gdi32.MoveToEx.argtypes = [HDC, ctypes.c_int, ctypes.c_int, ctypes.POINTER(wintypes.POINT)]
gdi32.TextOutW.argtypes = [HDC, ctypes.c_int, ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int]
gdi32.CreateFontW.restype = wintypes.HFONT

# Constants
SRCCOPY = 0xCC0020
PATINVERT = 0x005A0049

# Get primary screen dimensions
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Array of random colors
rndclr = [0xFF0000, 0xFF00BC, 0x00FF33, 0xFFF700, 0x00FFEF, 0x0000FF, 0x00FFFF, 0xFFFF00, 0xFF00FF]

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

# Function to draw random shapes
def draw_random_shapes(hdc):
    shape_type = random.choice(['rectangle', 'ellipse', 'line'])
    color = rndclr[random.randint(0, len(rndclr)-1)]
    brush = gdi32.CreateSolidBrush(color)
    gdi32.SelectObject(hdc, brush)
    
    left = random.randint(0, screen_width)
    top = random.randint(0, screen_height)
    right = random.randint(left, screen_width)
    bottom = random.randint(top, screen_height)
    
    if shape_type == 'rectangle':
        gdi32.Rectangle(hdc, left, top, right, bottom)
    elif shape_type == 'ellipse':
        gdi32.Ellipse(hdc, left, top, right, bottom)
    elif shape_type == 'line':
        gdi32.MoveToEx(hdc, left, top, None)
        gdi32.LineTo(hdc, right, bottom)
    
    gdi32.DeleteObject(brush)

# Function to fill the screen with random colors
def fill_screen_random_colors(hdc):
    for _ in range(100):
        left = random.randint(0, screen_width)
        top = random.randint(0, screen_height)
        right = left + random.randint(50, 200)
        bottom = top + random.randint(50, 200)
        color = rndclr[random.randint(0, len(rndclr)-1)]
        brush = gdi32.CreateSolidBrush(color)
        gdi32.SelectObject(hdc, brush)
        gdi32.Rectangle(hdc, left, top, right, bottom)
        gdi32.DeleteObject(brush)

# Function to draw a tunnel effect
def draw_tunnel_effect(hdc):
    center_x = screen_width // 2
    center_y = screen_height // 2
    max_radius = min(screen_width, screen_height) // 2
    step = 10
    for radius in range(0, max_radius, step):
        color = rndclr[random.randint(0, len(rndclr)-1)]
        brush = gdi32.CreateSolidBrush(color)
        gdi32.SelectObject(hdc, brush)
        gdi32.Ellipse(hdc, center_x - radius, center_y - radius, center_x + radius, center_y + radius)
        gdi32.DeleteObject(brush)

# Function to draw text
def draw_text(hdc, text, x, y):
    font = gdi32.CreateFontW(48, 0, 0, 0, 700, False, False, False, 0, 0, 0, 0, 0, "Arial")
    gdi32.SelectObject(hdc, font)
    gdi32.TextOutW(hdc, x, y, text, len(text))
    gdi32.DeleteObject(font)

# Function to draw bouncing balls
def draw_bouncing_balls(hdc):
    num_balls = 10
    balls = [{'x': random.randint(0, screen_width),
              'y': random.randint(0, screen_height),
              'dx': random.choice([-10, -5, 5, 10]),
              'dy': random.choice([-10, -5, 5, 10]),
              'color': rndclr[random.randint(0, len(rndclr)-1)]}
             for _ in range(num_balls)]
    
    for _ in range(50):
        for ball in balls:
            brush = gdi32.CreateSolidBrush(ball['color'])
            gdi32.SelectObject(hdc, brush)
            gdi32.Ellipse(hdc, ball['x'], ball['y'], ball['x']+20, ball['y']+20)
            gdi32.DeleteObject(brush)
            
            ball['x'] += ball['dx']
            ball['y'] += ball['dy']
            
            if ball['x'] < 0 or ball['x'] > screen_width:
                ball['dx'] = -ball['dx']
            if ball['y'] < 0 or ball['y'] > screen_height:
                ball['dy'] = -ball['dy']
        time.sleep(0.1)
        gdi32.PatBlt(hdc, 0, 0, screen_width, screen_height, PATINVERT)

# Main loop
while True:
    hdc = user32.GetDC(0)
    mhdc = gdi32.CreateCompatibleDC(hdc)
    hbit = gdi32.CreateCompatibleBitmap(hdc, screen_width, screen_height)
    holdbit = gdi32.SelectObject(mhdc, hbit)
    
    # Random background color
    gdi32.SetBkColor(hdc, rndclr[random.randint(0, len(rndclr)-1)])
    
    # Random hatch brush style
    hatch_style = random.randint(0, 5)
    brush = gdi32.CreateHatchBrush(hatch_style, rndclr[random.randint(0, len(rndclr)-1)])
    gdi32.SelectObject(hdc, brush)
    
    # Randomly choose between PatBlt, drawing shapes, filling random colors, tunnel effect, text, or bouncing balls
    effect_choice = random.choice(['patblt', 'shapes', 'fill_colors', 'tunnel', 'text', 'bouncing_balls'])
    if effect_choice == 'patblt':
        gdi32.PatBlt(hdc, 0, 0, screen_width, screen_height, PATINVERT)
    elif effect_choice == 'shapes':
        for _ in range(random.randint(5, 20)):
            draw_random_shapes(hdc)
    elif effect_choice == 'fill_colors':
        fill_screen_random_colors(hdc)
    elif effect_choice == 'tunnel':
        draw_tunnel_effect(hdc)
    elif effect_choice == 'text':
        draw_text(hdc, "lowertioum.exe", screen_width//2 - 100, screen_height//2 - 24)
    elif effect_choice == 'bouncing_balls':
        draw_bouncing_balls(hdc)
    
    gdi32.DeleteObject(brush)
    gdi32.DeleteDC(hdc)
    user32.ReleaseDC(0, hdc)
    
    time.sleep(1)