import ctypes
import time
import sys

def run_monitor():
    print("=" * 60)
    print("  ESP32-ETH01 Ad Blocker Serial Monitor (115200 Baud)")
    print("  Press Ctrl+C to exit")
    print("=" * 60)

    try:
        d2xx = ctypes.windll.LoadLibrary('C:\\Windows\\System32\\ftd2xx.dll')
    except Exception as e:
        print(f"Error loading ftd2xx.dll: {e}")
        return

    handle = ctypes.c_void_p()
    res = d2xx.FT_Open(0, ctypes.byref(handle))
    if res != 0:
        print(f"Error opening FTDI device (code {res}). Is the USB adapter plugged in?")
        return

    d2xx.FT_SetBaudRate(handle, 115200)
    d2xx.FT_SetDataCharacteristics(handle, 8, 0, 0)
    d2xx.FT_SetTimeouts(handle, 500, 500)

    try:
        while True:
            rx_q = ctypes.c_ulong()
            tx_q = ctypes.c_ulong()
            event = ctypes.c_ulong()
            d2xx.FT_GetStatus(handle, ctypes.byref(rx_q), ctypes.byref(tx_q), ctypes.byref(event))
            if rx_q.value > 0:
                buf = ctypes.create_string_buffer(rx_q.value)
                read = ctypes.c_ulong()
                d2xx.FT_Read(handle, buf, rx_q.value, ctypes.byref(read))
                text = buf.raw[:read.value].decode('utf-8', errors='replace')
                sys.stdout.write(text)
                sys.stdout.flush()
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
    finally:
        d2xx.FT_Close(handle)

if __name__ == "__main__":
    run_monitor()

