# WINAPIMOVEMENT.PY START

# libraries
import ctypes
from ctypes import wintypes
import time
import threading
import struct
import zlib


# MOUSE FUNCTIONS START

# WinAPI CONSTANTS START
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP   = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP   = 0x0040
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP   = 0x0100
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x1000
# WinAPI CONSTANTS END

# STRUCTURES START
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MOUSEINPUT)
    ]
# STRUCTURES END

# FUNCTIONS START
def position():
    point = (ctypes.c_long * 2)()
    ctypes.windll.user32.GetCursorPos(point)
    return point[0], point[1]



def mouseUp(button='left'):
    data = 0
    if button == 'left':
        event = MOUSEEVENTF_LEFTUP
    elif button == 'right':
        event = MOUSEEVENTF_RIGHTUP
    elif button == 'middle':
        event = MOUSEEVENTF_MIDDLEUP
    elif button == 'x1':
        event = MOUSEEVENTF_XUP
        data = 0x0001
    elif button == 'x2':
        event = MOUSEEVENTF_XUP
        data = 0x0002
    else:
        raise TypeError("Invalid button")
    input_event = INPUT()
    input_event.type = INPUT_MOUSE
    input_event.mi = MOUSEINPUT(0, 0, data, event, 0, None)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))



def mouseDown(button='left'):
    data = 0
    if button == 'left':
        event = MOUSEEVENTF_LEFTDOWN
    elif button == 'right':
        event = MOUSEEVENTF_RIGHTDOWN
    elif button == 'middle':
        event = MOUSEEVENTF_MIDDLEDOWN
    elif button == 'x1':
        event = MOUSEEVENTF_XDOWN
        data = 0x0001
    elif button == 'x2':
        event = MOUSEEVENTF_XDOWN
        data = 0x0002
    else:
        raise TypeError("Invalid button")
    input_event = INPUT()
    input_event.type = INPUT_MOUSE
    input_event.mi = MOUSEINPUT(0, 0, data, event, 0, None)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))



def click(x=None, y=None, times=1,interval=0, button='left'):
    if x is not None and y is not None:
        ctypes.windll.user32.SetCursorPos(x, y)
    BATCH = 8
    data = 0
    while times > 0:
        n = min(times, BATCH)
        total = n * 2
        events = (INPUT * total)()
        idx = 0
        if button == 'left':
            down = MOUSEEVENTF_LEFTDOWN
            up = MOUSEEVENTF_LEFTUP
        elif button == 'right':
            down = MOUSEEVENTF_RIGHTDOWN
            up = MOUSEEVENTF_RIGHTUP
        elif button == 'middle':
            down = MOUSEEVENTF_MIDDLEDOWN
            up = MOUSEEVENTF_MIDDLEUP
        elif button == 'x1':
            down = MOUSEEVENTF_XDOWN
            up = MOUSEEVENTF_XUP
            data = 0x0001
        elif button == 'x2':
            down = MOUSEEVENTF_XDOWN
            up = MOUSEEVENTF_XUP
            data = 0x0002
        else:
            raise TypeError("Invalid button")
        for _ in range(n):
            # DOWN
            events[idx].type = INPUT_MOUSE
            events[idx].mi = MOUSEINPUT(0, 0, data, down, 0, None)
            idx += 1
            events[idx].type = INPUT_MOUSE
            events[idx].mi = MOUSEINPUT(0, 0, data, up, 0, None)
            idx += 1
        ctypes.windll.user32.SendInput(total, ctypes.byref(events), ctypes.sizeof(INPUT))
        times -= n
        time.sleep(interval)
        
        
        
def moveTo(x, y, steps=1, duration=0):
    start_x, start_y = position()
    delta_x = (x - start_x) / steps
    delta_y = (y - start_y) / steps
    for i in range(steps):
        new_x = int(start_x + delta_x * (i + 1))
        new_y = int(start_y + delta_y * (i + 1))
        ctypes.windll.user32.SetCursorPos(new_x, new_y)
        time.sleep(duration / steps)



def moveRel(dx, dy, steps=1, duration=0):
    start_x, start_y = position()
    target_x = start_x + dx
    target_y = start_y + dy
    moveTo(target_x, target_y, steps, duration)



def scroll(vertical=0, horizontal=0):
    if vertical != 0:
        data = vertical * 120
        event = MOUSEEVENTF_WHEEL
    elif horizontal != 0:
        data = horizontal * 120
        event = MOUSEEVENTF_HWHEEL
    else:
        return
    input_event = INPUT()
    input_event.type = INPUT_MOUSE
    input_event.mi = MOUSEINPUT(0, 0, data, event, 0, None)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))



def dragTo(x, y, steps=100, duration=1, button='left'):
    mouseDown(button)
    moveTo(x, y, steps, duration)
    mouseUp(button)



def dragRel(dx, dy, steps=100, duration=1, button='left'):
    start_x, start_y = position()
    target_x = start_x + dx
    target_y = start_y + dy
    dragTo(target_x, target_y, steps, duration, button)
# FUNCTIONS END

# MOUSE FUNCTIONS END



# KEYBOARD FUNCTIONS START

# WinAPI CONSTANTS START
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
WH_KEYBOARD_LL=13
WM_KEYDOWN=0x0100
RIDEV_INPUTSINK=0x00000100
RID_INPUT=0x10000003
WM_INPUT=0x00FF
KEYEVENTF_SCANCODE = 0x0008
special_keys = {
    "ctrl": 0x11,
    "control": 0x11,
    "shift": 0x10,
    "alt": 0x12,
    "menu": 0x12,
    "enter": 0x0D,
    "return": 0x0D,
    "space": 0x20,
    "tab": 0x09,
    "esc": 0x1B,
    "escape": 0x1B,
    "backspace": 0x08,
    "delete": 0x2E,
    "insert": 0x2D,
    "home": 0x24,
    "end": 0x23,
    "up": 0x26,
    "down": 0x28,
    "left": 0x25,
    "right": 0x27,
}
# WinAPI CONSTANTS END

# STRUCTURES START
HCURSOR = wintypes.HANDLE
HICON = wintypes.HANDLE
HBRUSH = wintypes.HANDLE
HINSTANCE = wintypes.HANDLE



class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [
            ("mi", MOUSEINPUT),
            ("ki", KEYBDINPUT)
        ]

    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("_input", _INPUT)
    ]

class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage", wintypes.USHORT),
        ("usUsage", wintypes.USHORT),
        ("dwFlags", wintypes.DWORD),
        ("hwndTarget", wintypes.HWND)
    ]

class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType", wintypes.DWORD),
        ("dwSize", wintypes.DWORD),
        ("hDevice", wintypes.HANDLE),
        ("wParam", wintypes.WPARAM)
    ]

class RAWKEYBOARD(ctypes.Structure):
    _fields_ = [
        ("MakeCode", wintypes.USHORT),
        ("Flags", wintypes.USHORT),
        ("Reserved", wintypes.USHORT),
        ("VKey", wintypes.USHORT),
        ("Message", wintypes.UINT),
        ("ExtraInformation", wintypes.ULONG)
    ]

class RAWINPUT(ctypes.Structure):
    _fields_ = [
        ("header", RAWINPUTHEADER),
        ("keyboard", RAWKEYBOARD)
    ]

class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]

callbacks=[]
key_state={}
hwnd=None
started=False
# STRUCTURES END

# FUNCTIONS START
def keyToVK(key:str)->int:
    key=key.lower()
    if key in special_keys:
        return special_keys[key]
    if len(key)==1:
        return ord(key.upper())
    raise TypeError("Unknown key")



def keyDown(key, type='vk'):
    event = INPUT()
    event.type = 1
    if type == 'vk':
        vk = keyToVK(key)
        event.ki = KEYBDINPUT(vk, 0, 0, 0, None)
    elif type == 'unicode':
        code = ord(key)
        event.ki = KEYBDINPUT(0, code, KEYEVENTF_UNICODE, 0, None)
    elif type == 'scan':
        vk = keyToVK(key)
        scan = ctypes.windll.user32.MapVirtualKeyW(vk, 0)
        event.ki = KEYBDINPUT(0, scan, KEYEVENTF_SCANCODE, 0, None)
    else:
        raise TypeError("type must be 'vk', 'unicode' or 'scan'")
    ctypes.windll.user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(INPUT))



def keyUp(key, type='vk'):
    event = INPUT()
    event.type = 1
    if type == 'vk':
        vk = keyToVK(key)
        event.ki = KEYBDINPUT(vk, 0, KEYEVENTF_KEYUP, 0, None)
    elif type == 'unicode':
        code = ord(key)
        event.ki = KEYBDINPUT(0, code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, None)
    elif type == 'scan':
        vk = keyToVK(key)
        scan = ctypes.windll.user32.MapVirtualKeyW(vk, 0)
        event.ki = KEYBDINPUT(0, scan, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, None)
    else:
        raise TypeError("type must be 'vk', 'unicode' or 'scan'")
    ctypes.windll.user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(INPUT))



def press(key, presses=1, interval=0, type='vk'):
    for _ in range(presses):
        keyDown(key, type=type)
        time.sleep(interval)
        keyUp(key, type=type)
        time.sleep(interval)



def write(text, interval=0, type='unicode'):
    for char in text:
        press(char, interval=interval, type=type)



def doHotkey(*keys, interval=0):
    for key in keys:
        keyDown(key)
        time.sleep(interval)
    for key in reversed(keys):
        keyUp(key)
        time.sleep(interval)



def addHotkey(key, callback):
    global started
    if len(key) != 1:
        raise TypeError("addHotkey only accepts one key, for combinations use addCombo")
    vk = ord(key.upper())
    callbacks.append((vk, callback))
    if started:
        return
    started = True
    threading.Thread(target=_raw_loop, daemon=True).start()




def addCombo(keys, callback):
    global started
    vk_tuple = tuple(keyToVK(k) for k in keys)
    callbacks.append((vk_tuple, callback))
    if not started:
        started = True
        threading.Thread(target=_raw_loop, daemon=True).start()



def removeHotkey(key, callback):
    vk = keyToVK(key)
    for i,(code,cb) in enumerate(list(callbacks)):
        if code == vk and cb is callback:
            callbacks.pop(i)
            key_state[vk] = False
            return True
    return False



def removeCombo(keys, callback):
    vk_tuple = tuple(keyToVK(k) for k in keys)
    for i,(code,cb) in enumerate(list(callbacks)):
        if code == vk_tuple and cb is callback:
            callbacks.pop(i)
            for v in vk_tuple:
                key_state[v] = False
            return True
    return False



def _wnd_proc(hWnd,msg,wParam,lParam):
    if msg==WM_INPUT:
        size=wintypes.UINT()
        ctypes.windll.user32.GetRawInputData(lParam,RID_INPUT,None,ctypes.byref(size),ctypes.sizeof(RAWINPUTHEADER))
        buf=ctypes.create_string_buffer(size.value)
        ctypes.windll.user32.GetRawInputData(lParam,RID_INPUT,buf,ctypes.byref(size),ctypes.sizeof(RAWINPUTHEADER))
        raw=ctypes.cast(buf,ctypes.POINTER(RAWINPUT)).contents
        vk = raw.keyboard.VKey
        m  = raw.keyboard.Message
        if m == 0x0100:
            key_state[vk] = True
        elif m == 0x0101:
            key_state[vk] = False
        for code,cb in callbacks:
            if isinstance(code, tuple):
                if all(key_state.get(v, False) for v in code):
                    cb()
            else:
                if m == 0x0100 and code == vk:
                    cb()
    return ctypes.windll.user32.DefWindowProcW(hWnd,msg,wParam,ctypes.c_void_p(lParam))



def _raw_loop():
    global hwnd
    WNDPROC=ctypes.WINFUNCTYPE(ctypes.c_long,wintypes.HWND,wintypes.UINT,wintypes.WPARAM,wintypes.LPARAM)
    proc=WNDPROC(_wnd_proc)
    wc=WNDCLASS()
    wc.lpfnWndProc=proc
    wc.lpszClassName="RawInputHiddenWindow"
    ctypes.windll.user32.RegisterClassW(ctypes.byref(wc))
    hwnd=ctypes.windll.user32.CreateWindowExW(0,wc.lpszClassName,"raw",0,0,0,0,0,None,None,None,None)
    rid=RAWINPUTDEVICE(1,6,RIDEV_INPUTSINK,hwnd)
    ctypes.windll.user32.RegisterRawInputDevices(ctypes.byref(rid),1,ctypes.sizeof(RAWINPUTDEVICE))
    msg=wintypes.MSG()
    while ctypes.windll.user32.GetMessageW(ctypes.byref(msg),None,0,0)!=0:
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
# FUNCTIONS END

# KEYBOARD FUNCTIONS END



# SCREEN FUNCTIONS START

# WinAPI CONSTANTS START
SRCCOPY = 0x00CC0020
CAPTUREBLT = 0x40000000
BI_RGB = 0
DIB_RGB_COLORS = 0
# WinAPI CONSTANTS END

# STRUCTURES START
class GdiplusStartupInput(ctypes.Structure):
    _fields_=[
        ("GdiplusVersion",ctypes.c_uint32),
        ("DebugEventCallback",ctypes.c_void_p),
        ("SuppressBackgroundThread",ctypes.c_bool),
        ("SuppressExternalCodecs",ctypes.c_bool),
    ]

class CLSID(ctypes.Structure):
    _fields_=[
        ("Data1",ctypes.c_uint32),
        ("Data2",ctypes.c_uint16),
        ("Data3",ctypes.c_uint16),
        ("Data4",ctypes.c_ubyte*8),
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_=[
        ("biSize",ctypes.c_uint32),
        ("biWidth",ctypes.c_int32),
        ("biHeight",ctypes.c_int32),
        ("biPlanes",ctypes.c_uint16),
        ("biBitCount",ctypes.c_uint16),
        ("biCompression",ctypes.c_uint32),
        ("biSizeImage",ctypes.c_uint32),
        ("biXPelsPerMeter",ctypes.c_int32),
        ("biYPelsPerMeter",ctypes.c_int32),
        ("biClrUsed",ctypes.c_uint32),
        ("biClrImportant",ctypes.c_uint32),
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_=[
        ("bmiHeader",BITMAPINFOHEADER),
        ("bmiColors",ctypes.c_uint32*1),
    ]
# STRUCTURES END

# FUNCTIONS START
def size():
    return ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1)



def onScreen(x,y):
    sw,sh=size()
    return 0<=x<sw and 0<=y<sh



def pixel(x,y):
    u=ctypes.windll.user32
    g=ctypes.windll.gdi32
    hdc=u.GetDC(0)
    c=g.GetPixel(hdc,x,y)
    u.ReleaseDC(0,hdc)
    r=c&0xFF
    g=(c>>8)&0xFF
    b=(c>>16)&0xFF
    return r,g,b



def pixelMatchesColor(x,y,expected_color,tolerance=0):
    r,g,b=pixel(x,y)
    er,eg,eb=expected_color
    return abs(r-er)<=tolerance and abs(g-eg)<=tolerance and abs(b-eb)<=tolerance



def _screenshot_raw(region=None):
    u=ctypes.windll.user32
    g=ctypes.windll.gdi32
    sw,sh=size()
    if region is None:
        x,y,w,h=0,0,sw,sh
    else:
        x,y,w,h=region
    if w<=0 or h<=0:
        return None
    hdc_screen=u.GetDC(0)
    hdc_mem=g.CreateCompatibleDC(hdc_screen)
    hbitmap=g.CreateCompatibleBitmap(hdc_screen,w,h)
    if not hbitmap:
        u.ReleaseDC(0,hdc_screen)
        g.DeleteDC(hdc_mem)
        return None
    g.SelectObject(hdc_mem,hbitmap)
    g.BitBlt(hdc_mem,0,0,w,h,hdc_screen,x,y,SRCCOPY|CAPTUREBLT)
    u.ReleaseDC(0,hdc_screen)
    bmi=BITMAPINFO()
    bmi.bmiHeader.biSize=ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth=w
    bmi.bmiHeader.biHeight=-h
    bmi.bmiHeader.biPlanes=1
    bmi.bmiHeader.biBitCount=32
    bmi.bmiHeader.biCompression=BI_RGB
    buf_size=w*h*4
    buf=(ctypes.c_ubyte*buf_size)()
    res=g.GetDIBits(hdc_mem,hbitmap,0,h,ctypes.byref(buf),ctypes.byref(bmi),DIB_RGB_COLORS)
    g.DeleteObject(hbitmap)
    g.DeleteDC(hdc_mem)
    if res==0:
        return None
    return w,h,bytes(buf)



def _png_chunk(t,d):
    return struct.pack("!I",len(d))+t+d+struct.pack("!I",zlib.crc32(t+d)&0xffffffff)



def _encode_png_bgra(w,h,data):
    fixed=bytearray(len(data))
    for i in range(0,len(data),4):
        b=data[i]
        g=data[i+1]
        r=data[i+2]
        a=data[i+3]
        fixed[i]=r
        fixed[i+1]=g
        fixed[i+2]=b
        fixed[i+3]=a
    sig=b"\x89PNG\r\n\x1a\n"
    ihdr=struct.pack("!IIBBBBB",w,h,8,6,0,0,0)
    out=sig+_png_chunk(b"IHDR",ihdr)
    stride=w*4
    raw=b""
    for y in range(h):
        row=fixed[y*stride:(y+1)*stride]
        raw+=b"\x00"+row
    comp=zlib.compress(raw,9)
    out+=_png_chunk(b"IDAT",comp)
    out+=_png_chunk(b"IEND",b"")
    return out



def screenshot(region=None):
    r=_screenshot_raw(region)
    if r is None:
        return None
    w,h,buf=r
    return _encode_png_bgra(w,h,buf)



def screenshot_to_file(path,region=None):
    data=screenshot(region)
    if data is None:
        return False
    with open(path,"wb") as f:
        f.write(data)
    return True



def load_image_raw(path):
    gdiplus=ctypes.windll.gdiplus
    g=ctypes.windll.gdi32
    u=ctypes.windll.user32
    token=ctypes.c_ulong()
    si=GdiplusStartupInput(1,None,False,False)
    gdiplus.GdiplusStartup(ctypes.byref(token),ctypes.byref(si),None)
    image_ptr=ctypes.c_void_p()
    gdiplus.GdipCreateBitmapFromFile(ctypes.c_wchar_p(path),ctypes.byref(image_ptr))
    width=ctypes.c_uint()
    height=ctypes.c_uint()
    gdiplus.GdipGetImageWidth(image_ptr,ctypes.byref(width))
    gdiplus.GdipGetImageHeight(image_ptr,ctypes.byref(height))
    w0=width.value
    h0=height.value
    hbitmap=ctypes.c_void_p()
    gdiplus.GdipCreateHBITMAPFromBitmap(image_ptr,ctypes.byref(hbitmap),0)
    bmi=BITMAPINFO()
    bmi.bmiHeader.biSize=ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth=w0
    bmi.bmiHeader.biHeight=-h0
    bmi.bmiHeader.biPlanes=1
    bmi.bmiHeader.biBitCount=32
    bmi.bmiHeader.biCompression=BI_RGB
    buf_size=w0*h0*4
    buffer=(ctypes.c_ubyte*buf_size)()
    hdc=u.GetDC(0)
    g.GetDIBits(hdc,hbitmap,0,h0,ctypes.byref(buffer),ctypes.byref(bmi),DIB_RGB_COLORS)
    u.ReleaseDC(0,hdc)
    g.DeleteObject(hbitmap)
    gdiplus.GdipDisposeImage(image_ptr)
    gdiplus.GdiplusShutdown(token)
    print("Loaded:", w0, h0, "bytes:", len(buffer))
    return w0,h0,bytes(buffer)



def hash_rows(buf, w, h):
    row_bytes = w * 4
    hashes = []
    for y in range(h):
        start = y * row_bytes
        row = buf[start:start+row_bytes]
        hashes.append(zlib.crc32(row))
    return hashes



def locateOnScreen(path, region=None, step=3):
    r = _screenshot_raw(region)
    if r is None:
        return None
    sw, sh, screen = r
    nw, nh, needle = load_image_raw(path)
    if nw * nh > 200 * 200:
        return None
    hay_mv = memoryview(screen)
    sw4 = sw * 4
    row_bytes = nw * 4
    needle_hashes = hash_rows(needle, nw, nh)
    first_hash = needle_hashes[0]
    max_y = sh - nh + 1
    max_x = sw - nw + 1
    for y in range(0, max_y, step):
        base_y = y * sw4
        for x in range(0, max_x, step):
            si = base_y + x * 4
            row = hay_mv[si:si+row_bytes]
            if zlib.crc32(row) != first_hash:
                continue
            ok = True
            for j in range(1, nh):
                si2 = (y + j) * sw4 + x * 4
                row2 = hay_mv[si2:si2+row_bytes]
                if zlib.crc32(row2) != needle_hashes[j]:
                    ok = False
                    break
            if ok:
                return x, y, nw, nh
    return None



def center(box):
    x,y,w,h=box
    return x+w//2,y+h//2



def locateCenterOnScreen(path, region=None, step=3):
    r = locateOnScreen(path, region, step)
    return None if r is None else (r[0] + r[2]//2, r[1] + r[3]//2)



def locateAllOnScreen(path, region=None, step=3):
    r = _screenshot_raw(region)
    if r is None:
        return []
    sw, sh, screen = r
    nw, nh, needle = load_image_raw(path)
    if nw * nh > 200 * 200:
        return []
    hay_mv = memoryview(screen)
    sw4 = sw * 4
    row_bytes = nw * 4
    needle_hashes = hash_rows(needle, nw, nh)
    first_hash = needle_hashes[0]
    max_y = sh - nh + 1
    max_x = sw - nw + 1
    results = []
    for y in range(0, max_y, step):
        base_y = y * sw4
        for x in range(0, max_x, step):
            si = base_y + x * 4
            row = hay_mv[si:si+row_bytes]
            if zlib.crc32(row) != first_hash:
                continue
            ok = True
            for j in range(1, nh):
                si2 = (y + j) * sw4 + x * 4
                row2 = hay_mv[si2:si2+row_bytes]
                if zlib.crc32(row2) != needle_hashes[j]:
                    ok = False
                    break
            if ok:
                results.append((x, y, nw, nh))
    return results



def locate(needle, haystack, nw, nh, sw, sh, step=3):
    hay_mv = memoryview(haystack)
    ned_mv = memoryview(needle)
    sw4 = sw * 4
    row_bytes = nw * 4
    # Хэши needle
    needle_hashes = hash_rows(needle, nw, nh)
    first_hash = needle_hashes[0]
    max_y = sh - nh + 1
    max_x = sw - nw + 1
    for y in range(0, max_y, step):
        base_y = y * sw4
        for x in range(0, max_x, step):
            si = base_y + x * 4
            row = hay_mv[si:si+row_bytes]
            if zlib.crc32(row) != first_hash:
                continue
            ok = True
            for j in range(1, nh):
                si2 = (y + j) * sw4 + x * 4
                row2 = hay_mv[si2:si2+row_bytes]
                if zlib.crc32(row2) != needle_hashes[j]:
                    ok = False
                    break
            if ok:
                return x, y, nw, nh
    return None



def pixelMatchesColor_raw(x,y,color,tolerance,screen_raw,sw):
    i=(y*sw+x)*4
    b=screen_raw[i]
    g=screen_raw[i+1]
    r=screen_raw[i+2]
    er,eg,eb=color
    return abs(r-er)<=tolerance and abs(g-eg)<=tolerance and abs
# FUNCTIONS END

# SCREEN FUNCTIONS END

# WINAPIMOVEMENT.PY END
