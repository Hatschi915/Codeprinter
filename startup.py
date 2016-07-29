import socket 
import fcntl 
import struct 
import subprocess
import serial
import time
import sys
ser=serial.Serial('/dev/ttyS0', 19200)
ser.flush()
time.sleep(2)
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, # SIOCGIFADDR
        struct.pack('256s', ifname[:15]))[20:24]) 

for attempt in range (3):
    try:
        ip = get_ip_address('wlan0')
        ser.write("--------------------------------")
        ser.write("\n")        
        ser.write("STAND ALONE\nOffline Galerie Code Printer\nV 0.1 - 25.07.2016\n")
        ser.write ("IP:")
        ser.write (ip)
        ser.write("\nHotfolder gestartet\n--------------------------------")
        ser.write ("\n\n\n\n\n")
        subprocess.call("sudo python /home/pi/code/codewatcher.py", shell=True)

    except (KeyboardInterrupt):
        exit()
        
    except (IOError):    
        
        try:
            subprocess.call("sudo cp /media/usb0/PASSPHRASE.txt /home/pi/code", shell=True)
            subprocess.call("sudo cp /media/usb0/ENCRYPTION.txt /home/pi/code", shell=True)
            subprocess.call("sudo cp /media/usb0/SSID.txt /home/pi/code", shell=True)
            subprocess.call(["/boot/w.sh"])
            subprocess.call("sudo rm /home/pi/code/PASSPHRASE.txt", shell=True)
            subprocess.call("sudo rm /home/pi/code/ENCRYPTION.txt", shell=True)
            subprocess.call("sudo rm /home/pi/code/SSID.txt", shell=True)
            print "copy Wifi Configuration"
            ser.write("--------------------------------\nNetzwerkfehler\nlade Konfiguration\nIP-Check in 15s\n--------------------------------\n\n\n")
            time.sleep(15)
        except:
            print ("Setup Wifi Configuration USB-Stick")
    else:
        break
    
else:
    ser.write ("\n--------------------------------\nBitte USB-Stick\nkonfigurieren mit\nSSID.txt\nPASSPHRASE.txt\nENCRYPTION.txt\nPrinter SHUTDOWN\n--------------------------------\n--------------------------------\n\n\n\n")
