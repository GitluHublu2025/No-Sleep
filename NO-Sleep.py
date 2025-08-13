import ctypes
import threading
import time
from PIL import Image, ImageDraw
import pystray

# Windows API constants
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001

# State flag
keep_awake = False
stop_event = threading.Event()

def set_awake_mode(enable=True):
    """Enable or disable keep-awake mode."""
    if enable:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED
        )
    else:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

def awake_loop():
    """Thread to keep refreshing awake state."""
    while not stop_event.is_set():
        if keep_awake:
            set_awake_mode(True)
        time.sleep(30)  # refresh interval

def toggle_awake(icon, item):
    """Menu toggle."""
    global keep_awake
    keep_awake = not keep_awake
    if not keep_awake:
        set_awake_mode(False)
    icon.update_menu()

def create_image(color):
    """Create tray icon image."""
    img = Image.new('RGB', (64, 64), color)
    d = ImageDraw.Draw(img)
    d.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return img

def exit_program(icon, item):
    stop_event.set()
    set_awake_mode(False)
    icon.stop()

if __name__ == "__main__":
    threading.Thread(target=awake_loop, daemon=True).start()
    
    icon = pystray.Icon(
        "KeepAwake",
        create_image("green"),
        menu=pystray.Menu(
            pystray.MenuItem(lambda item: f"Keep Awake: {'ON' if keep_awake else 'OFF'}", toggle_awake),
            pystray.MenuItem("Exit", exit_program)
        )
    )
    icon.run()
