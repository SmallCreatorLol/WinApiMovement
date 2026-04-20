# WINAPIMOVEMENT.PY START

# libraries
import ctypes
from ctypes import wintypes
import time
import threading
import struct
import zlib
import random
import math


# FOR WORK START
libc = ctypes.cdll.msvcrt
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
ole32 = ctypes.windll.ole32
winmm = ctypes.windll.winmm
# FOR WORK END

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
    """
    Returns the current mouse cursor position.

    Returns:
        tuple[int, int]: (x, y) coordinates of the cursor.
    """
    
    # CODE START
    point = (ctypes.c_long * 2)()
    user32.GetCursorPos(point)
    return point[0], point[1]
    # CODE END



def mouseUp(button='left'):
    """
    Releases a mouse button (button up event).

    Args:
        button (str): Which button to release.
            'left', 'right', 'middle', 'x1', or 'x2'.

    Returns:
        None
    """
    
    # CODE START
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
    user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))
    # CODE END



def mouseDown(button='left'):
    """
    Presses and holds a mouse button (button down event).

    Args:
        button (str): Which button to press.
            'left', 'right', 'middle', 'x1', or 'x2'.

    Returns:
        None
    """
    
    # CODE START
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
    user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))
    # CODE END



def click(x=None, y=None, times=1,interval=0, button='left'):
    """
    Performs one or multiple mouse clicks.

    Args:
        x (int|None): X coordinate to click at. If None, uses current position.
        y (int|None): Y coordinate to click at.
        times (int): Number of clicks.
        interval (float): Delay between clicks.
        button (str): Mouse button to use.

    Returns:
        None
    """
    
    # CODE START
    if x is not None and y is not None:
        user32.SetCursorPos(x, y)
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
        user32.SendInput(total, ctypes.byref(events), ctypes.sizeof(INPUT))
        times -= n
        time.sleep(interval)
    # CODE END
        
        
        
def moveTo(x, y, steps=1, duration=0):
    """
    Moves the mouse cursor smoothly to (x, y).

    Args:
        x (int): Target X coordinate.
        y (int): Target Y coordinate.
        steps (int): Number of interpolation steps.
        duration (float): Total movement time in seconds.

    Returns:
        None
    """
    
    # CODE START
    start_x, start_y = position()
    delta_x = (x - start_x) / steps
    delta_y = (y - start_y) / steps
    for i in range(steps):
        new_x = int(start_x + delta_x * (i + 1))
        new_y = int(start_y + delta_y * (i + 1))
        user32.SetCursorPos(new_x, new_y)
        time.sleep(duration / steps)
    # CODE END



def moveRel(dx, dy, steps=1, duration=0):
    """
    Moves the mouse cursor relative to its current position.

    Args:
        dx (int): Horizontal offset (positive = right, negative = left).
        dy (int): Vertical offset (positive = down, negative = up).
        steps (int): Number of interpolation steps.
        duration (float): Total movement time in seconds.

    Returns:
        None
    """
    
    # CODE START
    start_x, start_y = position()
    target_x = start_x + dx
    target_y = start_y + dy
    moveTo(target_x, target_y, steps, duration)
    # CODE END



def scroll(vertical=0, horizontal=0):
    """
    Scrolls the mouse wheel vertically or horizontally.

    Args:
        vertical (int): Number of vertical scroll steps (positive = up, negative = down).
        horizontal (int): Number of horizontal scroll steps (positive = right, negative = left).

    Returns:
        None
    """
    
    # CODE START
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
    user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))
    # CODE END



def dragTo(x, y, steps=100, duration=1, button='left'):
    """
    Holds a mouse button and drags the cursor to an absolute position.

    Args:
        x (int): Target X coordinate.
        y (int): Target Y coordinate.
        steps (int): Number of interpolation steps during movement.
        duration (float): Total drag time in seconds.
        button (str): Mouse button to hold during drag.

    Returns:
        None
    """
    
    # CODE START
    mouseDown(button)
    moveTo(x, y, steps, duration)
    mouseUp(button)
    # CODE END



def dragRel(dx, dy, steps=100, duration=1, button='left'):
    """
    Holds a mouse button and drags the cursor relative to its current position.

    Args:
        dx (int): Horizontal offset.
        dy (int): Vertical offset.
        steps (int): Number of interpolation steps.
        duration (float): Total drag time in seconds.
        button (str): Mouse button to hold during drag.

    Returns:
        None
    """
    
    # CODE START
    start_x, start_y = position()
    target_x = start_x + dx
    target_y = start_y + dy
    dragTo(target_x, target_y, steps, duration, button)
    # CODE END



def humanityMoveTo(x, y, duration=0.4, roughness=1.0):
    """
    Moves the cursor to an absolute position using a human‑like motion model
    with angle shifts, inertia, micro‑pauses, speed variation and final stabilization.

    Args:
        x (int): Target X coordinate.
        y (int): Target Y coordinate.
        duration (float): Total movement time in seconds.
        roughness (float): Strength of angle changes, micro‑jerks and micro‑pauses.

    Returns:
        None
    """
    
    # CODE START
    x1, y1 = position()
    dist = math.hypot(x - x1, y - y1)
    steps = int(dist / 4) + 25
    cx, cy = x1, y1
    if random.random() < 0.25:
        time.sleep(random.uniform(0.02, 0.05))
    start = time.perf_counter()
    angle_offset = 0.0
    angle_inertia = 0
    base_step = dist / steps
    speed_multiplier = 1.0
    for i in range(steps):
        if steps - i <= 6:
            for _ in range(6):
                dx = x - cx
                dy = y - cy
                dist_left = math.hypot(dx, dy)
                if dist_left < 0.5:
                    cx, cy = x, y
                    moveTo(int(cx), int(cy))
                    return
                dx /= dist_left
                dy /= dist_left
                step = min(2.0, dist_left) * 0.40
                cx += dx * step + random.uniform(-0.12, 0.12)
                cy += dy * step + random.uniform(-0.12, 0.12)
                moveTo(int(cx), int(cy))
                time.sleep(0.004)
            moveTo(x, y)
            return
        t = i / (steps - 1)
        dx = x - cx
        dy = y - cy
        base_angle = math.atan2(dy, dx)
        if angle_inertia > 0:
            angle_inertia -= 1
        else:
            angle_offset += random.uniform(-0.05, 0.05) * roughness
            angle_offset = max(min(angle_offset, 0.12), -0.12)
        if random.random() < 0.05 * roughness:
            angle_offset += random.uniform(-0.08, 0.08) * roughness
            angle_inertia = random.randint(3, 7)
            speed_multiplier *= random.uniform(1.07, 1.15)
        if random.random() < 0.04:
            time.sleep(random.uniform(0.015, 0.04))
            angle_offset += random.uniform(-0.07, 0.07) * roughness
            angle_inertia = random.randint(2, 5)
            speed_multiplier *= random.uniform(0.85, 0.93)
        speed_multiplier += (1.0 - speed_multiplier) * 0.1
        final_angle = base_angle + angle_offset
        step = base_step * speed_multiplier
        cx += math.cos(final_angle) * step
        cy += math.sin(final_angle) * step
        if random.random() < 0.02 * roughness:
            cx += random.uniform(-1.2, 1.2)
            cy += random.uniform(-1.2, 1.2)
        if t > 0.85:
            cx += random.uniform(-0.2, 0.2)
            cy += random.uniform(-0.2, 0.2)
        moveTo(int(cx), int(cy))
        elapsed = time.perf_counter() - start
        remaining = duration - elapsed
        left = steps - i - 1
        if left > 0 and remaining > 0:
            time.sleep(remaining / left)
    # CODE END



def humanityMoveRel(dx, dy, duration=0.4, roughness=1.0):
    """
    Moves the cursor to a relative position using the same human‑like motion model
    as humanityMoveTo, including angle shifts, inertia and final stabilization.

    Args:
        dx (int): Horizontal offset from the current cursor position.
        dy (int): Vertical offset from the current cursor position.
        duration (float): Total movement time in seconds.
        roughness (float): Strength of human‑like irregularities.

    Returns:
        None
    """
    
    # CODE START
    start_x, start_y = position()
    target_x = start_x + dx
    target_y = start_y + dy
    humanityMoveTo(target_x, target_y, duration=duration, roughness=roughness)
    # CODE END



def humanityDragTo(x, y, duration=0.4, roughness=1.0, button='left'):
    """
    Holds a mouse button and drags the cursor to an absolute position
    using the humanityMoveTo motion model with angle shifts, inertia,
    micro‑pauses and final stabilization.

    Args:
        x (int): Target X coordinate.
        y (int): Target Y coordinate.
        duration (float): Total drag time in seconds.
        roughness (float): Strength of human‑like irregularities.
        button (str): Mouse button to hold during the drag.

    Returns:
        None
    """
    
    # CODE START
    mouseDown(button=button)
    humanityMoveTo(x=x,y=y,duration=duration,roughness=roughness)
    mouseUp(button=button)
    # CODE END



def humanityDragRel(dx, dy, duration=0.4, roughness=1.0, button='left'):
    """
    Holds a mouse button and drags the cursor to a relative position
    using the humanityMoveTo motion model with angle shifts, inertia,
    micro‑pauses and final stabilization.

    Args:
        dx (int): Horizontal offset from the current cursor position.
        dy (int): Vertical offset from the current cursor position.
        duration (float): Total drag time in seconds.
        roughness (float): Strength of human‑like irregularities.
        button (str): Mouse button to hold during the drag.

    Returns:
        None
    """
    
    # CODE START
    start_x, start_y = position()
    target_x = start_x + dx
    target_y = start_y + dy
    humanityDragTo(target_x, target_y, duration=duration, roughness=roughness, button=button)
    # CODE END

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
    """
    Converts a key name into a virtual-key (VK) code.

    Args:
        key (str): Key name. Supports:
            - special keys from `special_keys`
            - single characters (letters, digits, symbols)

    Returns:
        int: Virtual-key code.

    Raises:
        TypeError: If the key is unknown.
    """
    
    # CODE START
    key=key.lower()
    if key in special_keys:
        return special_keys[key]
    if len(key)==1:
        return ord(key.upper())
    raise TypeError("Unknown key")
    # CODE END



def keyDown(key, type='vk'):
    """
    Sends a key-down event.

    Args:
        key (str): Key to press.
        type (str): Input mode:
            'vk'      – virtual-key code
            'unicode' – direct Unicode input
            'scan'    – hardware scancode

    Returns:
        None
    """
    
    # CODE START
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
        scan = user32.MapVirtualKeyW(vk, 0)
        event.ki = KEYBDINPUT(0, scan, KEYEVENTF_SCANCODE, 0, None)
    else:
        raise TypeError("type must be 'vk', 'unicode' or 'scan'")
    user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(INPUT))
    # CODE END



def keyUp(key, type='vk'):
    """
    Sends a key-up event.

    Args:
        key (str): Key to release.
        type (str): Input mode:
            'vk', 'unicode', or 'scan'.

    Returns:
        None
    """
    
    # CODE START
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
        scan = user32.MapVirtualKeyW(vk, 0)
        event.ki = KEYBDINPUT(0, scan, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, None)
    else:
        raise TypeError("type must be 'vk', 'unicode' or 'scan'")
    user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(INPUT))
    # CODE END



def press(key, presses=1, interval=0, type='vk'):
    """
    Presses and releases a key one or multiple times.

    Args:
        key (str): Key to press.
        presses (int): Number of repetitions.
        interval (float): Delay between presses.
        type (str): Input mode ('vk', 'unicode', 'scan').

    Returns:
        None
    """
    
    # CODE START
    for _ in range(presses):
        keyDown(key, type=type)
        time.sleep(interval)
        keyUp(key, type=type)
        time.sleep(interval)
    # CODE END



def write(text, interval=0, type='unicode'):
    """
    Types a string character-by-character.

    Args:
        text (str): Text to type.
        interval (float): Delay between characters.
        type (str): Input mode ('unicode' recommended).

    Returns:
        None
    """
    
    # CODE START
    for char in text:
        press(char, interval=interval, type=type)
    # CODE END



def doHotkey(*keys, interval=0):
    """
    Presses a key combination (e.g., ctrl+shift+esc).

    Args:
        *keys (str): Keys to press in order.
        interval (float): Delay between presses.

    Returns:
        None
    """
    
    # CODE START
    for key in keys:
        keyDown(key)
        time.sleep(interval)
    for key in reversed(keys):
        keyUp(key)
        time.sleep(interval)
    # CODE END



def addHotkey(key, callback):
    """
    Registers a single-key hotkey using RAWINPUT.

    Args:
        key (str): Single key (one character).
        callback (callable): Function to call on key press.

    Returns:
        None
    Raises:
        TypeError: If key is not a single character.
    """
    
    # CODE START
    global started
    if len(key) != 1:
        raise TypeError("addHotkey only accepts one key, for combinations use addCombo")
    vk = ord(key.upper())
    callbacks.append((vk, callback))
    if started:
        return
    started = True
    threading.Thread(target=_raw_loop, daemon=True).start()
    # CODE END




def addCombo(keys, callback):
    """
    Registers a multi-key combination hotkey.

    Args:
        keys (list[str] | tuple[str]): Keys forming the combo.
        callback (callable): Function to call when all keys are held.

    Returns:
        None
    """
    
    # CODE START
    global started
    vk_tuple = tuple(keyToVK(k) for k in keys)
    callbacks.append((vk_tuple, callback))
    if not started:
        started = True
        threading.Thread(target=_raw_loop, daemon=True).start()
    # CODE END



def removeHotkey(key, callback):
    """
    Removes a previously registered single-key hotkey.

    Args:
        key (str): Key to remove.
        callback (callable): Callback associated with this hotkey.

    Returns:
        bool: True if removed, False if not found.
    """
    
    # CODE START
    vk = keyToVK(key)
    for i,(code,cb) in enumerate(list(callbacks)):
        if code == vk and cb is callback:
            callbacks.pop(i)
            key_state[vk] = False
            return True
    return False
    # CODE END



def removeCombo(keys, callback):
    """
    Removes a previously registered key-combination hotkey.

    Args:
        keys (list[str] | tuple[str]): Combination to remove.
        callback (callable): Callback associated with this combo.

    Returns:
        bool: True if removed, False if not found.
    """
    
    # CODE START
    vk_tuple = tuple(keyToVK(k) for k in keys)
    for i,(code,cb) in enumerate(list(callbacks)):
        if code == vk_tuple and cb is callback:
            callbacks.pop(i)
            for v in vk_tuple:
                key_state[v] = False
            return True
    return False
    # CODE END



def _wnd_proc(hWnd,msg,wParam,lParam):
    """
    Internal RAWINPUT window procedure.

    Handles:
        - WM_INPUT events
        - Key state tracking
        - Hotkey and combo detection

    Args:
        hWnd: Window handle.
        msg: Message ID.
        wParam: WPARAM.
        lParam: LPARAM.

    Returns:
        LRESULT: Result of DefWindowProcW.
    """
    
    # CODE START
    if msg==WM_INPUT:
        size=wintypes.UINT()
        user32.GetRawInputData(lParam,RID_INPUT,None,ctypes.byref(size),ctypes.sizeof(RAWINPUTHEADER))
        buf=ctypes.create_string_buffer(size.value)
        user32.GetRawInputData(lParam,RID_INPUT,buf,ctypes.byref(size),ctypes.sizeof(RAWINPUTHEADER))
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
    return user32.DefWindowProcW(hWnd,msg,wParam,ctypes.c_void_p(lParam))
    # CODE END



def _raw_loop():
    """
    Internal message loop for RAWINPUT hotkey processing.

    Creates:
        - Hidden window
        - RAWINPUT device registration
        - Infinite GetMessageW loop

    Runs in a background thread.

    Returns:
        None
    """
    
    # CODE START
    global hwnd
    WNDPROC=ctypes.WINFUNCTYPE(ctypes.c_long,wintypes.HWND,wintypes.UINT,wintypes.WPARAM,wintypes.LPARAM)
    proc=WNDPROC(_wnd_proc)
    wc=WNDCLASS()
    wc.lpfnWndProc=proc
    wc.lpszClassName="RawInputHiddenWindow"
    user32.RegisterClassW(ctypes.byref(wc))
    hwnd=user32.CreateWindowExW(0,wc.lpszClassName,"raw",0,0,0,0,0,None,None,None,None)
    rid=RAWINPUTDEVICE(1,6,RIDEV_INPUTSINK,hwnd)
    user32.RegisterRawInputDevices(ctypes.byref(rid),1,ctypes.sizeof(RAWINPUTDEVICE))
    msg=wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg),None,0,0)!=0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
    # CODE END

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
    """
    Returns the current screen resolution.

    Returns:
        tuple[int, int]: (width, height) of the primary display.
    """
    
    # CODE START
    return user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
    # CODE END



def onScreen(x,y):
    """
    Checks whether a coordinate is inside the screen bounds.

    Args:
        x (int): X coordinate.
        y (int): Y coordinate.

    Returns:
        bool: True if (x, y) is within the screen.
    """
    
    # CODE START
    sw,sh=size()
    return 0<=x<sw and 0<=y<sh
    # CODE END



def pixel(x,y):
    """
    Reads the RGB color of a screen pixel.

    Args:
        x (int): X coordinate.
        y (int): Y coordinate.

    Returns:
        tuple[int, int, int]: (R, G, B) color.
    """
    
    # CODE START
    hdc=user32.GetDC(0)
    c=gdi32.GetPixel(hdc,x,y)
    user32.ReleaseDC(0,hdc)
    r=c&0xFF
    g=(c>>8)&0xFF
    b=(c>>16)&0xFF
    return r,g,b
    # CODE END



def pixelMatchesColor(x,y,expected_color,tolerance=0):
    """
    Compares a pixel color with tolerance.

    Args:
        x (int): X coordinate.
        y (int): Y coordinate.
        expected_color (tuple[int, int, int]): (R, G, B).
        tolerance (int): Allowed deviation per channel.

    Returns:
        bool: True if colors match within tolerance.
    """
    
    # CODE START
    r,g,b=pixel(x,y)
    er,eg,eb=expected_color
    return abs(r-er)<=tolerance and abs(g-eg)<=tolerance and abs(b-eb)<=tolerance
    # CODE END



def _getScreenRAW(region=None):
    """
    Captures a raw BGRA screenshot.

    Args:
        region (tuple[int, int, int, int] | None):
            (x, y, width, height). If None, captures full screen.

    Returns:
        tuple[int, int, bytes]: (width, height, raw BGRA buffer)
    """
    
    # CODE START
    if region:
        x, y, w, h = region
    else:
        x, y = 0, 0
        w = user32.GetSystemMetrics(0)
        h = user32.GetSystemMetrics(1)
    hdc_screen = user32.GetDC(0)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    hbmp = gdi32.CreateCompatibleBitmap(hdc_screen, w, h)
    gdi32.SelectObject(hdc_mem, hbmp)
    gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc_screen, x, y, 0x00CC0020)
    total_bytes = w * h * 4
    buffer = (ctypes.c_ubyte * total_bytes)()
    gdi32.GetBitmapBits(hbmp, total_bytes, buffer)
    gdi32.DeleteObject(hbmp)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(0, hdc_screen)
    return w, h, buffer
    # CODE END



def _png_chunk(t,d):
    """
    Builds a PNG chunk.

    Args:
        t (bytes): Chunk type (e.g., b'IHDR').
        d (bytes): Chunk data.

    Returns:
        bytes: Complete PNG chunk with CRC.
    """
    
    # CODE START
    return struct.pack("!I",len(d))+t+d+struct.pack("!I",zlib.crc32(t+d)&0xffffffff)
    # CODE END



def _encodePngBGRA(w,h,data):
    """
    Encodes raw BGRA pixel data into a PNG image.

    Args:
        w (int): Width.
        h (int): Height.
        data (bytes): Raw BGRA buffer.

    Returns:
        bytes: PNG-encoded image.
    """
    
    # CODE START
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
    # CODE END



def screenshot(region=None):
    """
    Captures a screenshot and returns PNG bytes.

    Args:
        region (tuple[int, int, int, int] | None):
            (x, y, width, height). If None, captures full screen.

    Returns:
        bytes | None: PNG image data or None on failure.
    """
    
    # CODE START
    r=_getScreenRAW(region)
    if r is None:
        return None
    w,h,buf=r
    return _encodePngBGRA(w,h,buf)
    # CODE END



def screenshotToFile(path,region=None):
    """
    Saves a screenshot to a file.

    Args:
        path (str): Output file path.
        region (tuple[int, int, int, int] | None): Capture region.

    Returns:
        bool: True on success, False on failure.
    """
    
    # CODE START
    data=screenshot(region)
    if data is None:
        return False
    with open(path,"wb") as f:
        f.write(data)
    return True
    # CODE END



def loadImageRAW(path):
    """
    Loads a BMP file and extracts raw pixel data.

    Args:
        path (str): Path to BMP file.

    Returns:
        tuple[int, int, bytes]: (width, height, raw BGRA buffer)
    """
    
    # CODE START
    with open(path, 'rb') as f:
        data = f.read()
        w, h = struct.unpack('<ii', data[18:26])
        offset = struct.unpack('<I', data[10:14])
        raw_pixels = data[offset:]
        nw4 = w * 4
        return w, abs(h), raw_pixels
    # CODE END



def hashRows(buf, w, h):
    """
    Computes CRC32 hashes for each row of a BGRA image.

    Args:
        buf (bytes): Raw BGRA buffer.
        w (int): Width.
        h (int): Height.

    Returns:
        list[int]: CRC32 hash per row.
    """
    
    # CODE START
    row_bytes = w * 4
    hashes = []
    for y in range(h):
        start = y * row_bytes
        row = buf[start:start+row_bytes]
        hashes.append(zlib.crc32(row))
    return hashes
    # CODE END



def locateOnScreen(path, confidence=0.9, region=None, minSearchTime=0):
    """
    Searches for an image on the screen using multi-stage filtering.

    Args:
        path (str): Path to BMP template.
        confidence (float): Required match ratio (0..1).
        region (tuple[int, int, int, int] | None): Search region.
        minSearchTime (float): Minimum search duration.

    Returns:
        tuple[(x, y, w, h), float] | None:
            Found box and confidence percentage, or None.
    """
    
    # CODE START
    with open(path, 'rb') as f:
        data = f.read()
        nw, nh = struct.unpack('<ii', data[18:26])
        # Измени эти строки в WinApiMovement.py
        nw, nh = struct.unpack('<ii', data[18:26])
        offset = struct.unpack('<I', data[10:14])[0]
        raw = data[offset:]
        nh = abs(nh)
        needle_pixels = []
        stride = (nw * 3 + 3) & ~3
        for y in range(nh - 1, -1, -1):
            row_start = y * stride
            for x in range(0, nw * 3, 3):
                b, g, r = raw[row_start + x : row_start + x + 3]
                needle_pixels.append((r, g, b))
    while True:
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        sw = user32.GetSystemMetrics(0)
        sh = user32.GetSystemMetrics(1)
        hdc = user32.GetDC(0)
        mdc = gdi32.CreateCompatibleDC(hdc)
        hbmp = gdi32.CreateCompatibleBitmap(hdc, sw, sh)
        gdi32.SelectObject(mdc, hbmp)
        gdi32.BitBlt(mdc, 0, 0, sw, sh, hdc, 0, 0, 0x00CC0020)
        buf = (ctypes.c_ubyte * (sw * sh * 4))()
        gdi32.GetBitmapBits(hbmp, sw * sh * 4, buf)
        gdi32.DeleteObject(hbmp)
        gdi32.DeleteDC(mdc)
        user32.ReleaseDC(0, hdc)
        for y in range(0, sh - nh + 1, 3):
            for x in range(0, sw - nw + 1, 3):
                # 1. БЫСТРЫЙ ФИЛЬТР (те самые 3 точки)
                points_to_check = [(0,0), (nw//2, nh//2), (nw-1, nh-1)]
                found_points = 0
                for px, py in points_to_check:
                    s_idx = ((y + py) * sw + (x + px)) * 4
                    if (buf[s_idx+2], buf[s_idx+1], buf[s_idx]) == needle_pixels[py * nw + px]:
                        found_points += 1
                if found_points == len(points_to_check):
                    matched_pixels = 0
                    sample_step = 5
                    total_sampled = 0
                    for py in range(0, nh, sample_step):
                        for px in range(0, nw, sample_step):
                            total_sampled += 1
                            s_idx = ((y + py) * sw + (x + px)) * 4
                            if (buf[s_idx+2], buf[s_idx+1], buf[s_idx]) == needle_pixels[py * nw + px]:
                                matched_pixels += 1
                    current_confidence = matched_pixels / total_sampled
                    if current_confidence >= confidence:
                        return (x, y, nw, nh), current_confidence*100
    # CODE END



def center(box):
    """
    Returns the center point of a bounding box.

    Args:
        box (tuple[int, int, int, int]): (x, y, w, h).

    Returns:
        tuple[int, int]: (center_x, center_y).
    """
    
    # CODE START
    x,y,w,h=box
    return x+w//2,y+h//2
    # CODE END



def locateCenterOnScreen(path, confidence=0.9, region=[0,0,1920,1080], minSearchTime=0):
    """
    Finds an image on the screen and returns its center.

    Args:
        path (str): Path to BMP template.
        confidence (float): Required match ratio.
        region (tuple[int, int, int, int]): Search region.
        minSearchTime (float): Minimum search duration.

    Returns:
        tuple[int, int] | None: Center coordinates or None.
    """
    
    # CODE START
    r = locateOnScreen(path, confidence, region, minSearchTime)
    return None if r is None else (r[0] + r[2]//2, r[1] + r[3]//2)
    # CODE END



def locateAllOnScreen(path, region=None, step=3):
    """
    Finds all occurrences of an image on the screen.

    Args:
        path (str): Path to BMP template.
        region (tuple[int, int, int, int] | None): Search region.
        step (int): Pixel step for scanning.

    Returns:
        list[tuple[int, int, int, int]]: List of bounding boxes.
    """
    
    # CODE START
    r = _getScreenRAW(region)
    if r is None:
        return []
    sw, sh, screen = r
    nw, nh, needle = loadImageRAW(path)
    if nw * nh > 200 * 200:
        return []
    hay_mv = memoryview(screen)
    sw4 = sw * 4
    row_bytes = nw * 4
    needle_hashes = hashRows(needle, nw, nh)
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
    # CODE END



def locate(needle, haystack, nw, nh, sw, sh, step=3):
    """
    Searches for a raw BGRA image inside another raw BGRA buffer.

    Args:
        needle (bytes): Template BGRA buffer.
        haystack (bytes): Screen BGRA buffer.
        nw (int): Template width.
        nh (int): Template height.
        sw (int): Screen width.
        sh (int): Screen height.
        step (int): Pixel step.

    Returns:
        tuple[int, int, int, int] | None: Found box or None.
    """
    
    # CODE START
    hay_mv = memoryview(haystack)
    ned_mv = memoryview(needle)
    sw4 = sw * 4
    row_bytes = nw * 4
    needle_hashes = hashRows(needle, nw, nh)
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
    # CODE END



def pixelMatchesColorRaw(x,y,color,tolerance,screen_raw,sw):
    """
    Compares a pixel color inside a raw BGRA buffer.

    Args:
        x (int): X coordinate.
        y (int): Y coordinate.
        color (tuple[int, int, int]): Expected (R, G, B).
        tolerance (int): Allowed deviation.
        screen_raw (bytes): Raw BGRA buffer.
        sw (int): Screen width.

    Returns:
        bool: True if pixel matches within tolerance.
    """
    
    # CODE START
    i=(y*sw+x)*4
    b=screen_raw[i]
    g=screen_raw[i+1]
    r=screen_raw[i+2]
    er,eg,eb=color
    return abs(r-er)<=tolerance and abs(g-eg)<=tolerance and abs
    # CODE END

# FUNCTIONS END

# SCREEN FUNCTIONS END



# SOUND FUNCTIONS START

# WinAPI CONSTANTS START
SND_NODEFAULT  = 0x0002
SND_FILENAME   = 0x00020000
# WinAPi CONSTANTS END

# STRUCTURES START
class GUID(ctypes.Structure):
    _fields_ = [("Data1", ctypes.c_ulong), ("Data2", ctypes.c_ushort),
                ("Data3", ctypes.c_ushort), ("Data4", ctypes.c_ubyte * 8)]

class WAVEFORMATEX(ctypes.Structure):
    _fields_ = [("wFormatTag", ctypes.c_ushort), ("nChannels", ctypes.c_ushort),
                ("nSamplesPerSec", ctypes.c_uint), ("nAvgBytesPerSec", ctypes.c_uint),
                ("nBlockAlign", ctypes.c_ushort), ("wBitsPerSample", ctypes.c_ushort),
                ("cbSize", ctypes.c_ushort)]

class WAVEHDR(ctypes.Structure):
    _fields_ = [("lpData", ctypes.c_void_p), ("dwBufferLength", ctypes.c_uint),
                ("dwBytesRecorded", ctypes.c_uint), ("dwUser", ctypes.c_void_p),
                ("dwFlags", ctypes.c_uint), ("dwLoops", ctypes.c_uint),
                ("lpNext", ctypes.c_void_p), ("reserved", ctypes.c_void_p)]

class WAVEOUTCAPSW(ctypes.Structure):
    _fields_ = [
        ("wMid", ctypes.c_ushort),
        ("wPid", ctypes.c_ushort),
        ("vDriverVersion", ctypes.c_uint),
        ("szPname", ctypes.c_wchar * 32),
        ("dwFormats", ctypes.c_uint),
        ("wChannels", ctypes.c_ushort),
        ("wReserved1", ctypes.c_ushort),
        ("dwSupport", ctypes.c_uint)
    ]

class WAVEINCAPSW(ctypes.Structure):
    _fields_ = [
        ("wMid", ctypes.c_ushort),
        ("wPid", ctypes.c_ushort),
        ("vDriverVersion", ctypes.c_uint),
        ("szPname", ctypes.c_wchar * 32),
        ("dwFormats", ctypes.c_uint),
        ("wChannels", ctypes.c_ushort),
        ("wReserved1", ctypes.c_ushort),
        ("dwSupport", ctypes.c_uint)
    ]

ole32.CoInitialize(None)
# SCTUCTURES END

# FUNCTIONS START
def _guid(s):
    """
    Converts a GUID string into a GUID structure.

    Args:
        s (str): GUID in string form, e.g. "{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}".

    Returns:
        GUID: Parsed GUID structure.
    """
    
    # CODE START
    g = GUID()
    ole32.CLSIDFromString(s, ctypes.byref(g))
    return g
    # CODE END



def getAudioOutputDevices():
    """
    Returns a list of available audio output devices.

    Uses WinMM waveOutGetDevCapsW to enumerate devices.

    Returns:
        list[str]: Names of output devices.
    """
    
    # CODE START
    count = ctypes.windll.winmm.waveOutGetNumDevs()
    devices = []
    caps = WAVEOUTCAPSW()
    for i in range(count):
        # 32 - это размер структуры на x64
        if ctypes.windll.winmm.waveOutGetDevCapsW(i, ctypes.byref(caps), ctypes.sizeof(caps)) == 0:
            devices.append(caps.szPname)
    return devices
    # CODE END



def getAudioInputDevices():
    """
    Returns a list of available audio input devices (microphones).

    Uses WinMM waveInGetDevCapsW to enumerate devices.

    Returns:
        list[str]: Names of input devices.
    """
    
    # CODE START
    count = ctypes.windll.winmm.waveInGetNumDevs()
    devices = []
    caps = WAVEINCAPSW()
    for i in range(count):
        if ctypes.windll.winmm.waveInGetDevCapsW(i, ctypes.byref(caps), ctypes.sizeof(caps)) == 0:
            devices.append(caps.szPname)
    return devices
    # CODE END



def playSound(path):
    """
    Plays a sound file using WinMM PlaySoundW.

    Args:
        path (str): Path to WAV file.

    Returns:
        None
    """
    
    # CODE START
    ctypes.windll.winmm.PlaySoundW(path, None, 0x00020000 | 0x0002)
    # CODE END



def getVolume():
    """
    Gets the system master volume level (0–100%).

    Uses:
        - MMDeviceEnumerator
        - IAudioEndpointVolume

    Returns:
        int: Volume percentage (0–100), or -1 on failure.
    """
    
    # CODE START
    CLSID_MMDeviceEnumerator = "{BCDE0395-E52F-467C-8E3D-C4579291692E}"
    IID_IMMDeviceEnumerator = "{A95664D2-9614-4F35-A746-DE8DB63617E6}"
    IID_IAudioEndpointVolume = "{5CDF2C82-841E-4546-9722-0CF74078229A}"
    class GUID(ctypes.Structure):
        _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD), ("Data4", ctypes.c_byte * 8)]
    def _guid(s):
        g = GUID()
        ole32.CLSIDFromString(s, ctypes.byref(g))
        return g
    try:
        enum = ctypes.c_void_p()
        ole32.CoCreateInstance(ctypes.byref(_guid(CLSID_MMDeviceEnumerator)), None, 1, ctypes.byref(_guid(IID_IMMDeviceEnumerator)), ctypes.byref(enum))
        device = ctypes.c_void_p()
        vt_enum = ctypes.cast(enum, ctypes.POINTER(ctypes.c_void_p))
        # Метод GetDefaultAudioEndpoint (eRender=0, eConsole=0)
        ctypes.CFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))(
            ctypes.cast(vt_enum.contents, ctypes.POINTER(ctypes.c_void_p))[4])(enum, 0, 0, ctypes.byref(device))
        volume = ctypes.c_void_p()
        vt_device = ctypes.cast(device, ctypes.POINTER(ctypes.c_void_p))
        ctypes.CFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p, ctypes.POINTER(GUID), ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))(
            ctypes.cast(vt_device.contents, ctypes.POINTER(ctypes.c_void_p))[3])(device, ctypes.byref(_guid(IID_IAudioEndpointVolume)), 7, None, ctypes.byref(volume))
        level = ctypes.c_float(0)
        vt_volume = ctypes.cast(volume, ctypes.POINTER(ctypes.c_void_p))
        ctypes.CFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p, ctypes.POINTER(ctypes.c_float))(
            ctypes.cast(vt_volume.contents, ctypes.POINTER(ctypes.c_void_p))[9])(volume, ctypes.byref(level))
        return round(level.value * 100)
    except:
        return -1
    # CODE END



def setVolume(level_percent):
    """
    Sets the system master volume level.

    Args:
        level_percent (int): Volume 0–100.

    Returns:
        bool: True on success, False on failure.
    """
    
    # CODE START
    if level_percent > 100: level_percent = 100
    if level_percent < 0: level_percent = 0
    level_float = level_percent / 100.0
    CLSID_MMDeviceEnumerator = "{BCDE0395-E52F-467C-8E3D-C4579291692E}"
    IID_IMMDeviceEnumerator = "{A95664D2-9614-4F35-A746-DE8DB63617E6}"
    IID_IAudioEndpointVolume = "{5CDF2C82-841E-4546-9722-0CF74078229A}"
    try:
        enum = ctypes.c_void_p()
        ole32.CoCreateInstance(ctypes.byref(_guid(CLSID_MMDeviceEnumerator)), None, 1, ctypes.byref(_guid(IID_IMMDeviceEnumerator)), ctypes.byref(enum))
        device = ctypes.c_void_p()
        vt_enum = ctypes.cast(enum, ctypes.POINTER(ctypes.c_void_p))
        ctypes.CFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))(
            ctypes.cast(vt_enum.contents, ctypes.POINTER(ctypes.c_void_p))[4])(enum, 0, 0, ctypes.byref(device))
        volume = ctypes.c_void_p()
        vt_device = ctypes.cast(device, ctypes.POINTER(ctypes.c_void_p))
        ctypes.CFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p, ctypes.POINTER(GUID), ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))(
            ctypes.cast(vt_device.contents, ctypes.POINTER(ctypes.c_void_p))[3])(device, ctypes.byref(_guid(IID_IAudioEndpointVolume)), 7, None, ctypes.byref(volume))
        vt_volume = ctypes.cast(volume, ctypes.POINTER(ctypes.c_void_p))
        ctypes.CFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p, ctypes.c_float, ctypes.c_void_p)(
            ctypes.cast(vt_volume.contents, ctypes.POINTER(ctypes.c_void_p))[7])(volume, level_float, None)
        return True
    except:
        return False
    # CODE END



def getMicHZ(duration=0.1):
    """
    Measures the dominant frequency of microphone input using zero-crossings.

    Args:
        duration (float): Recording duration in seconds.

    Returns:
        float: Estimated frequency in Hz.
    """
    
    # CODE START
    wfx = WAVEFORMATEX(1, 1, 44100, 88200, 2, 16, 0)
    hIn = ctypes.c_void_p()
    if winmm.waveInOpen(ctypes.byref(hIn), -1, ctypes.byref(wfx), 0, 0, 0) != 0:
        return 0
    size = int(44100 * duration * 2) 
    buf = (ctypes.c_byte * size)()
    hdr = WAVEHDR(ctypes.cast(buf, ctypes.c_void_p), size, 0, 0, 0, 0, 0, 0)
    winmm.waveInPrepareHeader(hIn, ctypes.byref(hdr), ctypes.sizeof(WAVEHDR))
    winmm.waveInAddBuffer(hIn, ctypes.byref(hdr), ctypes.sizeof(WAVEHDR))
    winmm.waveInStart(hIn)
    while not (hdr.dwFlags & 0x01):
        pass
    winmm.waveInStop(hIn)
    samples = ctypes.cast(buf, ctypes.POINTER(ctypes.c_short))
    num_samples = hdr.dwBytesRecorded // 2
    crossings = 0
    for i in range(1, num_samples):
        if (samples[i-1] < 0 and samples[i] >= 0):
            crossings += 1      
    hz = crossings / duration
    winmm.waveInUnprepareHeader(hIn, ctypes.byref(hdr), ctypes.sizeof(WAVEHDR))
    winmm.waveInClose(hIn)
    return hz
    # CODE END



def getMicVolume(duration=0.1):
    """
    Measures microphone volume using peak amplitude.

    Args:
        duration (float): Recording duration in seconds.

    Returns:
        int: Volume level (0–100).
    """
    
    # CODE START
    wfx = WAVEFORMATEX(1, 1, 44100, 88200, 2, 16, 0)
    hIn = ctypes.c_void_p()
    if winmm.waveInOpen(ctypes.byref(hIn), -1, ctypes.byref(wfx), 0, 0, 0) != 0:
        return 0
    size = int(44100 * duration * 2)
    buf = (ctypes.c_byte * size)()
    hdr = WAVEHDR(ctypes.cast(buf, ctypes.c_void_p), size, 0, 0, 0, 0, 0, 0)
    winmm.waveInPrepareHeader(hIn, ctypes.byref(hdr), ctypes.sizeof(WAVEHDR))
    winmm.waveInAddBuffer(hIn, ctypes.byref(hdr), ctypes.sizeof(WAVEHDR))
    winmm.waveInStart(hIn)
    while not (hdr.dwFlags & 0x01): pass
    winmm.waveInStop(hIn)
    samples = ctypes.cast(buf, ctypes.POINTER(ctypes.c_short))
    num_samples = hdr.dwBytesRecorded // 2
    max_amp = 0
    for i in range(num_samples):
        val = abs(samples[i])
        if val > max_amp:
            max_amp = val
    volume = (max_amp / 32767) * 100
    winmm.waveInUnprepareHeader(hIn, ctypes.byref(hdr), ctypes.sizeof(WAVEHDR))
    winmm.waveInClose(hIn)
    return round(volume)
    # CODE END

# FUNCTIONS END

# SOUND FUNCTIONS END

# WINAPIMOVEMENT.PY END
