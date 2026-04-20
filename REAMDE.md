WinApiMovement                                                                                                                               |
WinApiMovement is a minimalistic, high‑performance Windows automation library built directly on top of the WinAPI using pure ctypes.         |
No dependencies, no hidden layers, no overhead.                                                                                              |
Designed for speed, precision, and full control over mouse, keyboard, hotkeys, and screen operations.                                        |
                                                                                                                                             |
--------------------------------------------------------------------------------------------------------------------------------------------- 
                                                                                                                                              
This library provides:                                                                                                                        
Low‑level mouse control                                                                                                                       
Low‑level keyboard control                                                                                                                    
Global hotkeys via RAW INPUT                                                                                                                  
Fast screenshots using GDI and GDI+                                                                                                           
Image recognition on screen                                                                                                                   
Pixel‑level operations                                                                                                                        
All functionality is implemented manually through direct WinAPI calls.                                                                        
                                                                                                                                              
Features:                                          |----------------------------------------------------------------------------------------- 
                                                   |                                                                                          
Mouse                                              |                                     EXAMPLES                                             
                                                   |                                                                                          
Get cursor position                                |          pos = position()                                                                
Move cursor (absolute and relative)                |          moveTo(800, 400); moveRel(50, -20)                                              
Mouse button down/up                               |          mouseDown('left'); mouseUp('x1')                                                
High‑speed clicking (batched SendInput)            |          click(times=1000)                                                               
Vertical and horizontal scrolling                  |          scroll(vertical=5); scroll(horizontal=3)                                        
Drag and drop                                      |          dragTo(100, 100); dragRel(50, 0)                                                
                                                   |                                                                                          
Keyboard                                           |                                                                                          
                                                   |                                                                                          
Key down/up                                        |          keyDown('a'); keyUp('a')                                                        
Unicode input                                      |          press('Ж', unicode=True)                                                        
Key sequences                                      |          press('a', presses=5, interval=0.1)                                             
Hotkey combinations                                |          doHotkey('ctrl','s')                                                            
Special keys (Ctrl, Shift, Alt, arrows, etc.)      |          press('enter'); press('left')                                                   
RAW INPUT Global Hotkeys                           |          addHotkey('f6', callback)                                                       
Global hotkeys without window focus                |          addHotkey('a', lambda: print('A'))                                              
Multi‑key combinations                             |          addCombo(['ctrl','shift','a'], callback)                                        
Add and remove hotkeys dynamically                 |          removeHotkey('f6', callback)                                                    
Tracks real key states                             |          if key_state.get(vk): ...                                                       
No hooks, no delays, no blocking                   |          runs in background thread automatically                                         
Runs in a background message loop thread           |          started=True after first hotkey                                                 
                                                   |                                                                                          
Screen                                             |                                                                                          
                                                   |                                                                                          
Fast PNG screenshots via GDI+                      |          screenshot_to_file('screen.png')                                                
Raw screenshots via BitBlt                         |          w,h,buf = _screenshot_raw()                                                     
Load image as raw BGRA                             |          w0,h0,img = load_image_raw('img.png')                                           
Locate image on screen                             |          box = locateOnScreen('button.png')                                              
Locate center of image                             |          cx,cy = locateCenterOnScreen('button.png')                                      
Locate all matches                                 |          for b in locateAllOnScreen('icon.png'): print(b)                                
Low‑level locate (raw buffers)                     |          locate(needle, haystack, nw, nh, sw, sh)                                        
Pixel color reading                                |          r,g,b = pixel(100, 200)                                                         
Pixel color comparison with tolerance              |          pixelMatchesColor(100,200,(255,0,0),10)                                         
Raw pixel comparison                               |          pixelMatchesColor_raw(x,y,(r,g,b),10,raw,sw)                                    
                                                   |                                                                                          
SOUND                                              |                                                                                          
                                                   |                                                                                          
get all audio devices output/input                 |          getAudioOutputDevices(); getAudioInputDevices                                   
plays sound                                        |          playSound(sound.wav)                                                            
get/change system volume                           |          getVolume(); setVolume(50)                                                      
get mic volume/hz                                  |          getMicHZ(); getMicVolume()                                                      
                                                   |                                                                                          
AUTHOR: Rostik.                                    |                                                                                          
version: 1.0.2                                     |                                                                                          
Creating time: 15 days                             |                                                                                          
Created: 20 April 2026                             |                                                                                          
                                                   |                                                                                          
                                                   |                                                                                          
Why WinApiMovement?
WinApiMovement exists for one reason: to provide direct, predictable, low‑level Windows automation without the overhead, dependencies, and abstraction layers found in typical Python libraries.

Most automation tools (PyAutoGUI, pynput, pillow‑based screenshotters) rely on heavy stacks of Python wrappers, slow image processing, and indirect OS calls.
WinApiMovement removes all of that.

Direct WinAPI Access
Every function is implemented manually through:
SendInput, SetCursorPos, BitBit, GetDIBits, Raw INPUT, GDI+

ctypes structures mapped 1:1 to C

No wrappers. No hidden logic. No latency.

Zero Dependencies
The entire library is a single file, ~22–55 KB in size.
No Pillow, no numpy, no pyscreeze, no mouseinfo, no hooks, no DLL injections.

This makes WinApiMovement:
-faster
-safer
-portable
-predictable
-easy to embed into any project

-Performance‑Focused
-Every part of the library is optimized for speed:
-batched SendInput for ultra‑fast clicking
-raw BGRA screenshot capture
-custom PNG encoder
-memoryview‑based image matching
-early‑pixel rejection for fast locateOnScreen
-zero Python overhead where possible

The result: performance that beats PyAutoGUI by orders of magnitude.

Full Control
WinApiMovement exposes the real Windows API directly.
You control:
-mouse
-keyboard
-global hotkeys
-raw input
-screen buffers
-pixel data
-image recognition

Nothing is abstracted away.
Nothing is hidden.

Minimalistic by Design
The library follows strict principles:
-no empty lines
-no comments
-no unnecessary abstractions
-no magic
-no bloat
-Just pure functionality.

Built for Developers Who Want Real Power
WinApiMovement is not a “beginner‑friendly wrapper”.
It is a toolbox for people who want full control over Windows automation, without compromises, without overhead, and without depending on giant third‑party libraries.
