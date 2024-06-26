import ctypes
import random
import time
from ctypes import wintypes

# Windows API tanımları
user32 = ctypes.WinDLL('user32')
gdi32 = ctypes.WinDLL('gdi32')

# Sabitler ve yapılar
HDC = wintypes.HDC
COLORREF = wintypes.COLORREF

# GDI fonksiyon prototipleri
user32.GetDC.argtypes = [HDC]
user32.ReleaseDC.argtypes = [HDC, HDC]
gdi32.CreateCompatibleDC.argtypes = [HDC]
gdi32.CreateCompatibleBitmap.argtypes = [HDC, ctypes.c_int, ctypes.c_int]
gdi32.SelectObject.argtypes = [HDC, ctypes.c_void_p]
gdi32.DeleteDC.argtypes = [HDC]
gdi32.DeleteObject.argtypes = [ctypes.c_void_p]
gdi32.SetBkColor.argtypes = [HDC, COLORREF]
gdi32.SetTextColor.argtypes = [HDC, COLORREF]
gdi32.TextOutW.argtypes = [HDC, ctypes.c_int, ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int]
gdi32.CreateSolidBrush.argtypes = [COLORREF]

# Sabitler
SRCCOPY = 0xCC0020

# Ekran genişliği ve yüksekliği
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Rastgele renkler
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]

# "Downloading..." penceresi gösteren ve ardından GDI efekti çizen fonksiyon
def fake_downloading_window():
    # Simüle edilen indirme işlemi
    print("Downloading...")  # Burada gerçek bir indirme işlemi yerine sadece mesaj basıyoruz.
    time.sleep(3)  # 3 saniye bekletiyoruz.

    # GDI efekti
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)
    bitmap = gdi32.CreateCompatibleBitmap(hdc, screen_width, screen_height)
    gdi32.SelectObject(memdc, bitmap)

    # Rastgele şekiller çiz
    for _ in range(100):
        draw_random_shape(memdc)

    # Ekranı güncelle
    gdi32.BitBlt(hdc, 0, 0, screen_width, screen_height, memdc, 0, 0, SRCCOPY)

    # Belleği temizle
    gdi32.DeleteObject(bitmap)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)

# Rastgele şekiller çizen fonksiyon
def draw_random_shape(hdc):
    shape_type = random.choice(['rectangle', 'ellipse', 'line'])
    color = random.choice(colors)
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

# Ana döngü
while True:
    fake_downloading_window()
