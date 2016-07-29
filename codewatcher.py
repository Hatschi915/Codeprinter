#!/usr/bin/python
import time
import serial
import os
import Image
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import ImageFile

###Variabeln###
jpg=".jpg"
xml=".xml"
temp="temp.jpg"
Breeze="Breeze Kiosk"
max_retries = 99999999
###############

###Settings###
photoResize = 384, 256
ImageFile.LOAD_TRUNCATED_IMAGES = False
ser=serial.Serial('/dev/ttyS0', 19200)
ser.flush()
#time.sleep(1)
WaitBeforePrinting=6 # delay in seconds / change if printed picture is not complete
feedAfterPrint=4 # in lines / lines are added after print is complete
###############

################Print Layout###################
            #---------------------------------#
line1=      ("     Zum Download mit WLAN"     )
line2=      ("          PHOTOBOOTH"           )
line3=      (" verbinden und Browser starten" )
lineFotoPin=("      Fotopin = "               )
line4=      ("  bilder.photobooth-archiv.de"  )
             #################################
             #################################
             #############Picture#############
             #################################
             #################################
             #################################
line5=      (" Download jetzt aus der Fotobox")
line6=      ("       oder online bis zu"      )
line7=      ("           4 Wochen"            )
line8=      ("    nach Veranstaltungsdatum"   )
            #---------------------------------#
###############################################

###Startup Cleaning Routine###
subprocess.call("sudo rm /home/pi/codeprinter/*", shell=True)
##############################



class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        
        size2 = -1
        asd = event.src_path
        print "Image added"+asd
        fileType = asd[-4:]
        kioskMode = asd[21:33]
        asd1 = asd[:-4]
        print fileType
        if fileType == jpg and kioskMode != Breeze:
            num = len(asd1)
            asd3 = num-8
            asd1 = asd1[asd3:num]
            print ("STAND ALONE JPG")
            print asd1
            ser.write("--------------------------------")
            ser.write("\n")        
            ser.write(line1+"\n")
            ser.write(line2+"\n")
            ser.write(line3+"\n")
            ser.write(lineFotoPin+asd1+"\n")
            ser.write(line4+"\n")
            while True:
                try:
                    temp = Image.open(asd).resize(photoResize)
                    temp.save('temp.jpg')
                except IOError:
                   print "transfer not complete"
                   continue                   
                break     
            os.system("lp temp.jpg")  
            time.sleep(8)#wait for CUPS to complete the print
            ser.write(line5+"\n")
            ser.write(line6+"\n")
            ser.write(line7+"\n")
            ser.write(line8+"\n")
            ser.write("--------------------------------")
            for feed in range (feedAfterPrint):
                ser.write("\n")
            os.remove(asd)
            os.remove("temp.jpg")
        elif fileType == jpg and kioskMode == Breeze:
            print ("STAND ALONE KIOSK")
            num = len(asd1)
            asd3 = num-8
            asd1 = asd1[asd3:num]
            print asd1
            ser.write("--------------------------------")
            ser.write("\n")        
            ser.write(line1+"\n")
            ser.write(line2+"\n")
            ser.write(line3+"\n")
            ser.write(lineFotoPin+asd1+"\n")
            ser.write(line4+"\n")
            ser.write("--------------------------------")
            ser.write(line5+"\n")
            ser.write(line6+"\n")
            ser.write(line7+"\n")
            ser.write(line8+"\n")
            ser.write("--------------------------------")
            for feed in range (feedAfterPrint):
                ser.write("\n")
            os.remove(asd)
        elif fileType == xml:
            print("STAND ALONE XML")
            num = len(asd1)
            asd3 = num-8
            asd1 = asd1[asd3:num]
            print asd1
            ser.write("--------------------------------")
            ser.write("\n")        
            ser.write(line1+"\n")
            ser.write(line2+"\n")
            ser.write(line3+"\n")
            ser.write(lineFotoPin+asd1+"\n")
            ser.write(line4+"\n")
            ser.write("--------------------------------")
            ser.write(line5+"\n")
            ser.write(line6+"\n")
            ser.write(line7+"\n")
            ser.write(line8+"\n")
            ser.write("--------------------------------")
            for feed in range (feedAfterPrint):
                ser.write("\n")
            os.remove(asd)
       # else:            
            #ser.write ("\n\n\n\n--------------------------------\nFalsches Dateiformat\nuse .jpg or .xml\n--------------------------------\n\n\n\n")
            #os.remove(asd)       
        print("---end---")

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/home/pi/codeprinter', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
