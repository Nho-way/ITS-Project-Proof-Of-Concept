#import tkinter as tk
#from tkinter import messagebox
import subprocess
import speedtest as sp

def speed_test():
    tester = sp.Speedtest()
    server = tester.get_best_server()

    print("Testing download speed...")
    download = tester.download()
    print(download/1000000, "Mbps download \n")

    print("Testing upload speed...")
    upload = tester.upload()
    print(upload/1000000, "Mbps upload \n")

def mac_address():
    print("Getting Mac Address...")
    mac = "failure"
    output = subprocess.check_output(["/sbin/ifconfig"])
    lines = output.decode('utf-8').splitlines()
    for line in lines:
        if "ether" in line:
            mac = line.split(" ")[1]
            break
    if mac == "failure":
        raise Exception("Uh Oh Stinky Poopy")
    return mac


def main():
    speed_test()
    #mac = mac_address()

if __name__ == "__main__":
    main()
