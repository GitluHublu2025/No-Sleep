import ctypes
import time

# Windows API constant flags
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001

def keep_screen_on():
    # Prevent the display and system from turning off
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED
    )

def main():
    print("Keeping the screen on. Press Ctrl+C to stop.")
    try:
        while True:
            keep_screen_on()
            time.sleep(30)  # refresh every 30 seconds
    except KeyboardInterrupt:
        # Revert to normal power settings
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        print("\nScreen-on prevention stopped.")

if __name__ == "__main__":
    main()


