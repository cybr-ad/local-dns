import sys
import os
import glob
import ctypes
import time
import serial
from esptool.cmds import detect_chip, write_flash

def get_boot_app0_path():
    candidates = [
        os.path.expanduser("~/.platformio/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "boot_app0.bin")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    matches = glob.glob(os.path.expanduser("~/.platformio/**/boot_app0.bin"), recursive=True)
    if matches:
        return matches[0]
    return "boot_app0.bin"

class FTDIPort(serial.SerialBase):
    def __init__(self, dev_index=0, baud=115200):
        super().__init__()
        self.d2xx = ctypes.windll.LoadLibrary('C:\\Windows\\System32\\ftd2xx.dll')
        self._dev_index = dev_index
        self._baudrate = baud
        self.handle = None
        self.port = 'FTDI:0'
        self.name = 'FTDI:0'
        self.is_open = False
        self._dtr = False
        self._rts = False
        self.open()

    def open(self):
        if not self.is_open or not self.handle:
            self.handle = ctypes.c_void_p()
            res = self.d2xx.FT_Open(self._dev_index, ctypes.byref(self.handle))
            if res != 0:
                raise RuntimeError(f'FT_Open failed with code {res}. Make sure FTDI adapter is connected.')
            self.d2xx.FT_SetBaudRate(self.handle, self._baudrate)
            self.d2xx.FT_SetDataCharacteristics(self.handle, 8, 0, 0) # 8N1
            self.d2xx.FT_SetTimeouts(self.handle, 2000, 2000)
            self.is_open = True

    def _reconfigure_port(self):
        if hasattr(self, 'handle') and self.handle:
            self.d2xx.FT_SetBaudRate(self.handle, self._baudrate)

    @property
    def dtr(self):
        return self._dtr

    @dtr.setter
    def dtr(self, val):
        self._dtr = val
        if val:
            self.d2xx.FT_SetDtr(self.handle)
        else:
            self.d2xx.FT_ClrDtr(self.handle)

    @property
    def rts(self):
        return self._rts

    @rts.setter
    def rts(self, val):
        self._rts = val
        if val:
            self.d2xx.FT_SetRts(self.handle)
        else:
            self.d2xx.FT_ClrRts(self.handle)

    def write(self, data):
        written = ctypes.c_ulong()
        self.d2xx.FT_Write(self.handle, bytes(data), len(data), ctypes.byref(written))
        return written.value

    def read(self, size=1):
        buf = ctypes.create_string_buffer(size)
        read_bytes = ctypes.c_ulong()
        self.d2xx.FT_Read(self.handle, buf, size, ctypes.byref(read_bytes))
        return bytes(buf.raw[:read_bytes.value])

    @property
    def in_waiting(self):
        rx_q = ctypes.c_ulong()
        tx_q = ctypes.c_ulong()
        event = ctypes.c_ulong()
        self.d2xx.FT_GetStatus(self.handle, ctypes.byref(rx_q), ctypes.byref(tx_q), ctypes.byref(event))
        return rx_q.value

    def reset_input_buffer(self):
        self.d2xx.FT_Purge(self.handle, 1) # FT_PURGE_RX

    def reset_output_buffer(self):
        self.d2xx.FT_Purge(self.handle, 2) # FT_PURGE_TX

    def close(self):
        if getattr(self, 'handle', None):
            self.d2xx.FT_Close(self.handle)
            self.handle = None
        self.is_open = False

def flash_esp32(target_port=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bootloader_path = os.path.join(base_dir, r".pio\build\wt32-eth01\bootloader.bin")
    partitions_path = os.path.join(base_dir, r".pio\build\wt32-eth01\partitions.bin")
    boot_app0_path = get_boot_app0_path()
    firmware_path = os.path.join(base_dir, r".pio\build\wt32-eth01\firmware.bin")

    for p in [bootloader_path, partitions_path, boot_app0_path, firmware_path]:
        if not os.path.exists(p):
            print(f"Error: binary file not found: {p}")
            sys.exit(1)

    print("=" * 60)
    print("  ESP32 WT32-ETH01 FIRMWARE FLASHER")
    print("  1. IO0 must be bridged to GND!")
    print("  2. Unplug & reconnect USB power now to enter Bootloader mode.")
    print("=" * 60)

    is_ftdi = (target_port is None or target_port.upper() == 'FTDI')
    if is_ftdi:
        print("Opening direct FTDI D2XX USB interface...")
        port = FTDIPort(baud=115200)
    else:
        print(f"Opening Serial port {target_port} at 115200 baud...")
        port = serial.Serial(target_port, 115200, timeout=3)

    try:
        chip = None
        for mode in ["no-reset", "default-reset"]:
            try:
                print(f"Connecting to ESP32 (mode: {mode})...")
                chip = detect_chip(port, connect_mode=mode, connect_attempts=25)
                if chip:
                    break
            except Exception as e:
                print(f"  Mode {mode} failed: {e}")

        if not chip:
            raise RuntimeError("Could not connect to ESP32 in any mode. Ensure IO0 is connected to GND and you power-cycled.")

        print(f"\nCONNECTED! Target: {chip.CHIP_NAME}")
        
        stub = chip.run_stub()
        print(f"Stub loader running. Flash ID: {hex(stub.flash_id())}")
        
        # Change baud rate to 460800 for high-speed flashing
        try:
            print("Changing baud rate to 460800...")
            stub.change_baud(460800)
            print("High-speed baud rate active.")
        except Exception as e:
            print(f"Continuing at current baud rate: {e}")

        files_to_flash = [
            (0x1000, open(bootloader_path, "rb")),
            (0x8000, open(partitions_path, "rb")),
            (0xe000, open(boot_app0_path, "rb")),
            (0x10000, open(firmware_path, "rb"))
        ]

        print("Flashing bootloader, partition table, boot_app0, and upgraded firmware...")
        write_flash(stub, files_to_flash, compress=True, erase_all=False)
        print("\nSUCCESS! Flashing fully completed and verified.")

        try:
            stub.hard_reset()
        except Exception:
            pass
        print("\n>>> ALL DONE! Now REMOVE IO0-GND bridge and reboot your board! <<<")

    finally:
        port.close()

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else None
    flash_esp32(p)
