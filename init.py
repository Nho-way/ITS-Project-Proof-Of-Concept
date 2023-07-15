import tkinter as tk
from tkinter import messagebox
import subprocess
import speedtest as sp
import platform
import requests
from getpass import getpass
import os
import platform

"""
Runs a speedtest using the speedtest library
Gets a mac address by running /sbin/ifconfig
Then parses the output
Gets the Operating System (either unix based or Mac)
Get public IP by going to ipinfo.io/ip
"""
def get_info():
    #Run Speed Test
    try:
        tester = sp.Speedtest()
        server = tester.get_best_server()
        print("Testing download speed...")
        download = tester.download()
        print(download/1000000, "Mbps download \n")
        print("Testing upload speed...")
        upload = tester.upload()
        print(upload/1000000, "Mbps upload \n")
    except Exception as E:
        print("Error running speedtest", E)
    
    #Get Mac Address
    try:
        print("Getting Mac Address...")
        mac = "failure"
        output = subprocess.check_output(["/sbin/ifconfig"])
        lines = output.decode('utf-8').splitlines()
        for line in lines:
            if "ether" in line:
                mac = line.split(" ")[1]
                break
        if mac == "failure":
            raise Exception("Didn't Find Mac Address")
        print(mac, "\n")
    except Exception as E:
        print("Error getting Mac Address: ", E)

    #Get MacOS Version
    try:
        ops = platform.mac_ver()
        print("macOS version:", ops[0], "\n") 
        numbers = ops[0].split(".")
        if numbers[0] == 13 and numbers[1] == 0:
            print("Consider updating your laptop as this version of OS has outdated AirDrop settings") 
    except Exception as E:
        print("Error getting MacOS Version: ", E)
    
    try:
        response = requests.get('https://ipinfo.io/ip')
        print("Getting Public IP...")
        public_ip = response.text.strip()
        print(public_ip, "\n")    
    except Exception as e:
        print("Error getting public IP: ", e)

    try:
        chip = platform.processor()
        if chip == "arm":
            app_path = "/Applications/Cisco"
            if os.path.exists(app_path):
                print("You are using an ARM Processor: Try Uninstalling AnyConnect and downloading the App Store Version")
    except Exception as E:
        print("Error getting processor: ", E)

   

"""
Forgets all networks with the networksetup command
"""
def forget_networks():
    try:
        subprocess.run(["networksetup", "-removeallpreferredwirelessnetworks", "en0"])
        print("All networks forgotten.\n")
    except Exception as e:
        print("Error in forgetting networks: ", e)



"""
Sets IPv4 to dhcp
Resets DHCP
Sets IPv6 to automatic
"""
def network_configuration():
    try:
        result = subprocess.run(["networksetup", "-listnetworkserviceorder"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("Error: " + result.stderr.strip())
        output_lines = result.stdout.splitlines()
        vpn_lines = [line for line in output_lines if "VPN" in line]
        vpns = []
        for line in vpn_lines:
            parts = line.split("(")
            vpn_name = parts[0].strip()
            vpns.append(vpn_name)
        if len(vpns) == 0:
            print("No VPNs actively running\n")
        else:
            for i in vpns:
                print(i)
    except Exception as E:
        print("Error getting VPNs: ", E) 

    network_service = "Wi-Fi"
    try: 
        subprocess.run(["networksetup", "-setdhcp", network_service])
        print("Set IPv4 to Using DHCP\n")
    except Exception as E:
        print("Error setting IPv4: ", E)

    try:
        repeat = True
        while repeat:
            password = getpass("Please Enter Password to Renew DHCP: ")
            command = ["ipconfig", "set", "en0", "dhcp"]
            result = subprocess.run(["sudo", "-S"] + command, input=password+'\n', capture_output=True, text=True)
            if result.returncode == 0:
                print("Renewed DHCP\n")
                repeat = False
    except Exception as E:
        print("Error setting DHCP: ", E)

    try:
        subprocess.run(["networksetup", "-setv6automatic", network_service])
        print("Set IPv6 to Automatically\n")
    except Exception as E:
        print("Error setting IPv6: ", E)

    try:
        command = ["defaults", "write", "gwp", "AutoProxyDiscoveryEnabled", "-bool", "false"]
        result = subprocess.run(command)
        command = ["networksetup", "-setproxyautodiscovery", network_service, "off"]
        result = subprocess.run(command, capture_output=True, text=True)
        command = ["networksetup", "-setwebproxystate", network_service, "off"]
        result = subprocess.run(command)
        command = ["networksetup", "-setsecurewebproxystate", network_service, "off"]
        result = subprocess.run(command)
        command = ["networksetup", "-setsocksfirewallproxystate", network_service, "off"]
        result = subprocess.run(command)
        """command = ["networksetup", "-setproxybypassdomains", network_service, "off"]
        result = subprocess.run(command)"""
        print("Set Proxies to Off.\n")
    except Exception as e:
        print("Error in configuring proxy protocols: ", e)



"""
Deletes auth.ucsd.edu certificate
"""
def del_certificate():
    try: 
        command = ['security', 'delete-certificate', '-c', 'auth.ucsd.edu']
        subprocess.run(command, check=True)
        print("Removed Auth Certificate")
    except Exception as e:
        print(" ")
    


"""
Deletes P-lists
"""
def del_plist():
    try:
        os.remove("/Library/Preferences/SystemConfiguration/CaptiveNetworkSupport")
    except:
        print()
    try:
        os.remove("/Library/Preferences/SystemConfiguration/com.apple.network.eapolclient.configuration")
    except:
        print()
    try:
        os.remove("/Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist")
    except:
        print()
    try:
        os.remove("/Library/Preferences/SystemConfiguration/preferences.plist")
    except:
        print()
    try:
        os.remove("/Library/Preferences/SystemConfiguration/NetworkInterfaces.plist")
    except:
        print()
    print("Removed P-Lists")



"""
Set MacOS to roam to strongest Wi-Fi signal
"""
def roam():
    try:
        repeat = True
        while repeat:
            password = getpass("Please Enter Password to make MacOS roam to strongest Wi-Fi signal: ")
            print("\n")
            command = [
                'sudo',
                '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport',
                'prefs',
                'joinMode=Strongest'
            ]
            result = subprocess.run(command, input=password+'\n', capture_output=True, text=True)
            if result.returncode == 0:
                print("Made MacOS roam to strongest Wi-Fi signal\n")
                repeat = False
    except Exception as E:
        print("Error setting macOS to roam: ", E)


def main():
    print("Note: You will have to manually check to see if they are blocked at https://netapps-web2.ucsd.edu/secure/blocked-hosts/search.pl.\n\n\n")
    repeat = True
    while repeat:
        message = "1) Get Info \n2) Forget Networks\n3) Configure Network\n4) Delete Certificates\n5) Delete P-Lists\n6) Make MacOS Roam\nWhat would you like to accomplish today? (Press Enter for All) "
        choice = input(message)

        print("####################################################################################")
        if choice == "":         
            get_info()
            forget_networks()
            network_configuration()
            del_certificate()
            del_plist()   
           
        elif choice == "1":         
            get_info()
            
        elif choice == "2":         
            forget_networks()
            
        elif choice == "3":           
            network_configuration()
            
        elif choice == "4":          
            del_certificate()

        elif choice == "5": 
            del_plist()

        else:
            print("Please enter a number 1 through 5 or press enter. ")
        print("\n")
        
        next = input("Would you like to do more? (Y/N) ")
        if next == "N" or next == "n":
            repeat = False
        print("####################################################################################")
        print("\n \n")
        


def create_button(root, text, command):
    button = tk.Button(root, text=text, command=command)
    button.pack(pady=5)

root = tk.Tk()
root.title("Network Utility")

# Create buttons for each option
create_button(root, "Get Info", get_info)
create_button(root, "Forget Networks", forget_networks)
create_button(root, "Configure Network", network_configuration)
create_button(root, "Delete Certificates", del_certificate)
create_button(root, "Delete P-Lists", del_plist)
create_button(root, "Make MacOS Roam", roam)

root.mainloop()


#if __name__ == "__main__":
#    main()
