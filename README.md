# WEP-attack Automation Script


This is a Python 3 script to automate WEP attacks using ARP replay, packet capture, and cracking with the `aircrack-ng` suite. It is designed to run on Kali Linux or similar Linux distributions with wireless cards supporting monitor mode and packet injection.

---

## Features

- Automatically puts your wireless interface into monitor mode
- Sets the wireless channel to target the access point
- Captures packets filtered by BSSID and channel using `airodump-ng`
- Performs ARP replay attack to generate traffic and IVs using `aireplay-ng`
- Monitors captured IVs and runs `aircrack-ng` to crack the WEP key once enough IVs are collected
- Cleans up and restores your wireless interface on exit

---

## Prerequisites

- Kali Linux or compatible Linux distribution
- Wireless card with monitor mode and packet injection support
- Installed tools: `aircrack-ng`, `python3`

Install required tools with:

```
sudo apt update
sudo apt install aircrack-ng python3 ```


``` bash
sudo ./wep_attack.py --interface wlan0 --bssid 00:11:22:33:44:55 --channel 6 --arpreplay
```


## Usage
1.Save the script as wep_attack.py and make it executable:

```bash
chmod +x wep_attack.py
```

2.Run the script with root privileges, specifying your wireless interface, target BSSID, and channel. Use --arpreplay to enable the ARP replay attack:

```bash
sudo ./wep_attack.py --interface wlan0 --bssid 00:11:22:33:44:55 --channel 6 --arpreplay
```


3.The script will:
• Enable monitor mode on your wireless interface
• Set the channel to the target AP's channel
• Start capturing packets for the target AP
• Perform ARP replay attack to generate IVs
• Monitor IV count and attempt to crack the WEP key      when enough IVs are captured
• Clean up and restore your interface on exit


4. To stop the script at any time, press Ctrl+C. The script will clean up automatically.


## Options

• `--interface`: Wireless interface to use (e.g.,   wlan0)
• `--bssid`: Target access point BSSID (MAC address)
• `--channel`: Target access point channel
• `--wepca`: Number of IVs to start cracking at (default: 10000)
• `--wept`: Timeout for capture in seconds (default: 300)
• `--arpreplay`: Enable ARP replay attack


## Legal and Ethical Notice
Use this script only on networks you own or have explicit permission to test. Unauthorized access to computer networks is illegal and unethical.

The author is not responsible for any misuse of this tool.


## License
This project is licensed under the MIT License. See the LICENSE file for details.


## Contributions
Contributions, issues, and feature requests are welcome! Feel free to open a pull request or issue.


## Contact
For questions or support, please open an issue on this repository.


