import sys
import os
import re
import subprocess
import serial.tools.list_ports
import ctypes

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_default_gateway():
    try:
        output = subprocess.check_output('ipconfig', text=True, stderr=subprocess.DEVNULL)
        gateways = re.findall(r'Default Gateway[ .]*: ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', output)
        for gw in gateways:
            if gw != '0.0.0.0':
                return gw
    except Exception:
        pass
    return '192.168.1.1'

def check_ftdi_available():
    try:
        d2xx = ctypes.windll.LoadLibrary('C:\\Windows\\System32\\ftd2xx.dll')
        num_devs = ctypes.c_ulong()
        d2xx.FT_CreateDeviceInfoList(ctypes.byref(num_devs))
        return num_devs.value > 0
    except Exception:
        return False

def main():
    clear_screen()
    print("=" * 72)
    print("  🛡️  WT32-ETH01 HARDWARE AD BLOCKER - INTERACTIVE SETUP WIZARD")
    print("=" * 72)
    print(" This wizard will configure your network settings, compile the firmware,")
    print(" and flash your WT32-ETH01 board automatically.\n")

    # 1. Detect Network
    detected_gw = get_default_gateway()
    gw_parts = detected_gw.split('.')
    suggested_ip = f"{gw_parts[0]}.{gw_parts[1]}.{gw_parts[2]}.95" if len(gw_parts) == 4 else "192.168.1.95"

    print("--- [1/4] Network Configuration ---")
    print(f" Detected Router Gateway: {detected_gw}\n")

    # Ask Board IP
    val_ip = input(f" 1. Enter Static IP for WT32-ETH01 Board [Default: {suggested_ip}]: ").strip()
    board_ip = val_ip if val_ip else suggested_ip

    # Ask Gateway
    val_gw = input(f" 2. Enter Router Gateway IP [Default: {detected_gw}]: ").strip()
    router_gw = val_gw if val_gw else detected_gw

    # Ask Subnet
    val_sub = input(f" 3. Enter Subnet Mask [Default: 255.255.255.0]: ").strip()
    subnet_mask = val_sub if val_sub else "255.255.255.0"

    print(f"\n >> Configured Network: IP={board_ip}, Gateway={router_gw}, Subnet={subnet_mask}\n")

    # 2. Select Port
    print("--- [2/4] Programmer / COM Port Selection ---")
    ports = list(serial.tools.list_ports.comports())

    options = [
        ("FTDI", "FTDI D2XX High-Speed Adapter (Direct USB / FT232R)")
    ]
    for p in ports:
        options.append((p.device, f"{p.device} - {p.description}"))
    options.append(("MANUAL", "Enter COM port manually (e.g. COM3, COM5)"))

    print(" Available connection options:")
    for idx, opt in enumerate(options, 1):
        print(f"   [{idx}] {opt[1]}")

    default_choice = 1
    choice = input(f"\n Select programmer option [1-{len(options)}] [Default: {default_choice}]: ").strip()
    try:
        choice_idx = int(choice) if choice else default_choice
        selected_opt = options[choice_idx - 1]
    except Exception:
        selected_opt = options[0]

    if selected_opt[0] == "MANUAL":
        target_port = input(" Enter COM port name (e.g. COM3): ").strip().upper()
    else:
        target_port = selected_opt[0]

    print(f" >> Selected programmer: {target_port}\n")

    # 3. Update Configuration Files
    print("--- [3/4] Updating Configuration & Compiling Firmware ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Update src/config_mgr.h
    cfg_path = os.path.join(base_dir, "src", "config_mgr.h")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg_content = f.read()

    cfg_content = re.sub(r'String staticIp\s*=\s*"[^"]*";', f'String staticIp = "{board_ip}";', cfg_content)
    cfg_content = re.sub(r'String staticGateway\s*=\s*"[^"]*";', f'String staticGateway = "{router_gw}";', cfg_content)
    cfg_content = re.sub(r'String staticSubnet\s*=\s*"[^"]*";', f'String staticSubnet = "{subnet_mask}";', cfg_content)

    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write(cfg_content)
    print(" [OK] Updated src/config_mgr.h")

    # Update build_web_ui.py banner & IP display
    ui_script = os.path.join(base_dir, "build_web_ui.py")
    with open(ui_script, "r", encoding="utf-8") as f:
        ui_content = f.read()

    ui_content = re.sub(r'IP:\s*[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', f'IP: {board_ip}', ui_content)
    ui_content = re.sub(r"API_BASE = \(window\.location\.protocol === 'file:'\) \? 'http://[^']*' : '';",
                        f"API_BASE = (window.location.protocol === 'file:') ? 'http://{board_ip}' : '';", ui_content)

    with open(ui_script, "w", encoding="utf-8") as f:
        f.write(ui_content)
    print(" [OK] Updated build_web_ui.py")

    # Regenerate web UI header
    print(" [..] Regenerating web UI header (src/web_ui.h)...")
    subprocess.check_call([sys.executable, ui_script])
    print(" [OK] Web UI regenerated.")

    # Compile firmware via PlatformIO
    print(" [..] Compiling firmware with PlatformIO (wt32-eth01)...")
    res = subprocess.run([sys.executable, "-m", "platformio", "run"], cwd=base_dir)
    if res.returncode != 0:
        print("\n [ERROR] PlatformIO compilation failed. Please check the logs above.")
        sys.exit(1)
    print(" [OK] Firmware compiled successfully!\n")

    # 4. Flashing Stage
    print("=" * 72)
    print("  --- [4/4] FLASHING THE WT32-ETH01 BOARD ---")
    print("=" * 72)
    print("  CRITICAL HARDWARE STEPS:")
    print("  1. Connect a jumper wire bridging IO0 to GND.")
    print("  2. Unplug and reconnect the USB power cable (or press EN/Reset).")
    print("     (This puts the ESP32 chip into ROM Bootloader Download Mode)")
    print("=" * 72)
    input("\n Press [ENTER] when IO0 is bridged to GND and power is connected...")

    import flash
    try:
        flash.flash_esp32(target_port)
    except Exception as e:
        print(f"\n [ERROR] Flashing failed: {e}")
        print("\n Troubleshooting Tips:")
        print(" - Verify that IO0 is firmly connected to GND.")
        print(" - Unplug and replug the USB cable, then run this setup again.")
        sys.exit(1)

    # 5. Success Instructions
    clear_screen()
    print("=" * 72)
    print("  🎉 ALL DONE! HARDWARE AD BLOCKER IS READY!")
    print("=" * 72)
    print(" NEXT STEPS TO SHIELD YOUR NETWORK:")
    print(" 1. REMOVE / DISCONNECT the wire between IO0 and GND.")
    print(" 2. Unplug and reconnect the power cable to boot the board normally.")
    print(" 3. Plug an Ethernet patch cable from the WT32-ETH01 to your router LAN port.")
    print("")
    print(f" 4. Open your router settings (http://{router_gw}) and go to DHCP Settings:")
    print(f"    Set Primary DNS to your board's IP:  👉  {board_ip}")
    print("")
    print(f" 5. Access your live Cyber Web Dashboard at:")
    print(f"    👉  http://{board_ip}")
    print("=" * 72)
    print("\n Setup complete! Every device on your network is now shielded.")

if __name__ == "__main__":
    main()
